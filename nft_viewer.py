import os
import requests
from dotenv import load_dotenv
from web3 import Web3

# Load env variables
load_dotenv()

provider = os.getenv("WEB3_PROVIDER")
wallet = os.getenv("WALLET_ADDRESS")
nft_contract_address = os.getenv("NFT_CONTRACT")
token_id = int(os.getenv("TOKEN_ID", 1))

w3 = Web3(Web3.HTTPProvider(provider))

if not w3.is_connected():
    raise SystemExit("❌ Web3 provider not connected")

# Extended ERC-721 ABI
erc721_abi = [
    {"constant": True, "inputs": [{"name": "_owner", "type": "address"}],
     "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}],
     "type": "function"},
    {"constant": True, "inputs": [{"name": "_owner", "type": "address"}, {"name": "_index", "type": "uint256"}],
     "name": "tokenOfOwnerByIndex", "outputs": [{"name": "tokenId", "type": "uint256"}],
     "type": "function"},
    {"constant": True, "inputs": [{"name": "_tokenId", "type": "uint256"}],
     "name": "ownerOf", "outputs": [{"name": "owner", "type": "address"}],
     "type": "function"},
    {"constant": True, "inputs": [{"name": "_tokenId", "type": "uint256"}],
     "name": "tokenURI", "outputs": [{"name": "uri", "type": "string"}],
     "type": "function"}
]

contract = w3.eth.contract(address=nft_contract_address, abi=erc721_abi)

def fetch_metadata(token_id: int):
    """Fetch NFT metadata by tokenId"""
    try:
        uri = contract.functions.tokenURI(token_id).call()
        if uri.startswith("ipfs://"):
            uri = uri.replace("ipfs://", "https://ipfs.io/ipfs/")
        response = requests.get(uri)
        metadata = response.json()
        return metadata
    except Exception as e:
        print(f"❌ Error fetching metadata for Token {token_id}: {e}")
        return None

def show_metadata(token_id: int, metadata: dict):
    """Pretty-print NFT metadata"""
    print(f"\n🔎 Token ID: {token_id}")
    if metadata:
        for key, value in metadata.items():
            print(f"   {key}: {value}")
        if "image" in metadata:
            img_url = metadata["image"]
            if img_url.startswith("ipfs://"):
                img_url = img_url.replace("ipfs://", "https://ipfs.io/ipfs/")
            print(f"🖼️ NFT Image: {img_url}")
    else:
        print("   ❌ No metadata found.")

def get_all_nfts(owner: str):
    """List all NFTs owned by a wallet"""
    balance = contract.functions.balanceOf(owner).call()
    print(f"\n📦 Wallet {owner} owns {balance} NFTs in this collection.")

    if balance == 0:
        return

    for i in range(balance):
        token_id = contract.functions.tokenOfOwnerByIndex(owner, i).call()
        metadata = fetch_metadata(token_id)
        show_metadata(token_id, metadata)

if __name__ == "__main__":
    print(f"🔎 Checking NFT {token_id} in contract {nft_contract_address}")
    single = fetch_metadata(token_id)
    show_metadata(token_id, single)

    print("\n==============================")
    print("👛 Fetching all NFTs for wallet")
    get_all_nfts(wallet)
