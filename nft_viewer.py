import os
import requests
import argparse
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

provider = os.getenv("WEB3_PROVIDER")
default_wallet = os.getenv("WALLET_ADDRESS")
default_contract = os.getenv("NFT_CONTRACT")
default_token = os.getenv("TOKEN_ID")

# CLI setup
parser = argparse.ArgumentParser(description="NFT Viewer")
parser.add_argument("--wallet", help="Override wallet address")
parser.add_argument("--contract", help="Override NFT contract address")
parser.add_argument("--token", help="Override NFT token ID")
args = parser.parse_args()

wallet_address = args.wallet if args.wallet else default_wallet
raw_contract = args.contract if args.contract else default_contract
token_id = args.token if args.token else default_token

# Validate required values
if not provider or not wallet_address or not raw_contract or not token_id:
    raise SystemExit("❌ Missing required values (WEB3_PROVIDER, WALLET_ADDRESS, NFT_CONTRACT, TOKEN_ID)")

w3 = Web3(Web3.HTTPProvider(provider))

try:
    wallet_address = Web3.to_checksum_address(wallet_address)
    nft_contract_address = Web3.to_checksum_address(raw_contract)
except Exception:
    raise SystemExit("❌ Invalid wallet or contract address format")

# Minimal ERC-721 ABI
erc721_abi = [
    {
        "constant": True,
        "inputs": [{"name": "_tokenId", "type": "uint256"}],
        "name": "tokenURI",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"name": "_tokenId", "type": "uint256"}],
        "name": "ownerOf",
        "outputs": [{"name": "owner", "type": "address"}],
        "type": "function",
    },
]

contract = w3.eth.contract(address=nft_contract_address, abi=erc721_abi)

print(f"\n🔎 Checking NFT {token_id} in contract {nft_contract_address} for wallet {wallet_address}...")

try:
    token_uri = contract.functions.tokenURI(int(token_id)).call()
    print(f"🌐 Token URI: {token_uri}")

    metadata = requests.get(token_uri, timeout=10).json()
    print(f"📜 NFT Metadata:")
    for k, v in metadata.items():
        print(f"   {k}: {v}")

    if "image" in metadata:
        print(f"🖼️ NFT Image: {metadata['image']}")

except Exception as e:
    print(f"❌ Error fetching NFT metadata: {e}")
