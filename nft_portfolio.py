import os
import requests
import csv
import json
import argparse
from web3 import Web3
from dotenv import load_dotenv
from pathlib import Path
from time import sleep
from tqdm import tqdm

load_dotenv()

# Default values from .env
default_wallet = os.getenv("WALLET_ADDRESS")
etherscan_api = os.getenv("ETHERSCAN_API_KEY")
polygon_api = os.getenv("POLYGONSCAN_API_KEY")
bsc_api = os.getenv("BSCSCAN_API_KEY")

# Default RPC endpoints
RPCS = {
    "eth": os.getenv("ETHEREUM_RPC", "https://mainnet.infura.io/v3/YOUR_PROJECT_ID"),
    "polygon": os.getenv("POLYGON_RPC", "https://polygon-rpc.com"),
    "bsc": os.getenv("BSC_RPC", "https://bsc-dataseed.binance.org/"),
}

# Minimal ERC-721 ABI
ERC721_ABI = [
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

# CLI setup
parser = argparse.ArgumentParser(description="Multi-chain NFT Portfolio Tracker")
parser.add_argument("--wallet", help="Wallet address")
parser.add_argument("--chains", default="eth", help="Comma-separated chains: eth,polygon,bsc")
parser.add_argument("--contract", help="Restrict results to one NFT contract")
parser.add_argument("--json", action="store_true", help="Export portfolio to JSON")
parser.add_argument("--csv", action="store_true", help="Export portfolio to CSV")
parser.add_argument("--all", action="store_true", help="Export portfolio to JSON and CSV")
parser.add_argument("--save-images", action="store_true", help="Download NFT images")
parser.add_argument("--folder", default="images", help="Folder to save images")
parser.add_argument("--limit", type=int, default=0, help="Limit number of NFTs per chain (0=no limit)")
args = parser.parse_args()

wallet_raw = args.wallet if args.wallet else default_wallet
if not wallet_raw:
    raise SystemExit("❌ Missing wallet address.")

try:
    wallet = Web3.to_checksum_address(wallet_raw)
except Exception:
    raise SystemExit("❌ Invalid wallet address format.")

# Ensure image folder exists
Path(args.folder).mkdir(parents=True, exist_ok=True)

# Utility functions
def resolve_ipfs(uri: str) -> str:
    if uri.startswith("ipfs://"):
        return uri.replace("ipfs://", "https://ipfs.io/ipfs/")
    return uri

def download_image(url: str, folder: str, token_id: str, contract: str):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        ext = os.path.splitext(url)[-1].split("?")[0] or ".png"
        filename = os.path.join(folder, f"{token_id}_{contract[:6]}{ext}")
        with open(filename, "wb") as f:
            f.write(resp.content)
        print(f"✅ Image saved: {filename}")
    except Exception as e:
        print(f"❌ Failed to download image {url}: {e}")

def fetch_nfts(chain: str):
    """Fetch NFT transfers from API"""
    api_key = {"eth": etherscan_api, "polygon": polygon_api, "bsc": bsc_api}.get(chain)
    if not api_key:
        print(f"⚠️ No API key for {chain}, skipping.")
        return []

    base_url = {"eth": "https://api.etherscan.io/api",
                "polygon": "https://api.polygonscan.com/api",
                "bsc": "https://api.bscscan.com/api"}[chain]

    url = f"{base_url}?module=account&action=tokennfttx&address={wallet}&page=1&offset=1000&sort=desc&apikey={api_key}"
    try:
        resp = requests.get(url, timeout=15).json()
        if resp.get("status") != "1":
            return []
        result = resp.get("result", [])
        if args.limit > 0:
            result = result[:args.limit]
        return result
    except Exception as e:
        print(f"❌ Error fetching NFTs from {chain}: {e}")
        return []

def build_portfolio(transactions, chain: str):
    portfolio = {}
    w3 = Web3(Web3.HTTPProvider(RPCS[chain]))
    for tx in transactions:
        try:
            contract_addr = Web3.to_checksum_address(tx["contractAddress"])
        except Exception:
            continue

        # Skip if --contract is set and this is not the one
        if args.contract and contract_addr.lower() != args.contract.lower():
            continue

        token_id = tx["tokenID"]
        name = tx.get("tokenName", "UnknownNFT")
        symbol = tx.get("tokenSymbol", "")
        if contract_addr not in portfolio:
            portfolio[contract_addr] = {"name": name, "symbol": symbol, "tokens": []}
        if token_id not in portfolio[contract_addr]["tokens"]:
            portfolio[contract_addr]["tokens"].append(token_id)
    return portfolio, w3

def fetch_metadata(w3, contract_addr, token_id):
    contract = w3.eth.contract(address=contract_addr, abi=ERC721_ABI)
    try:
        token_uri = contract.functions.tokenURI(int(token_id)).call()
        return resolve_ipfs(token_uri)
    except Exception:
        return None

def show_portfolio(portfolio):
    print(f"\n👛 NFT Portfolio for {wallet}")
    if not portfolio:
        print("⚠️ No NFTs found.")
    for contract, data in portfolio.items():
        print(f"\n📦 {data['name']} ({data['symbol']})")
        print(f"   Contract: {contract}")
        print(f"   Tokens: {', '.join(data['tokens'])}")

def export_to_json(portfolio, filename="nft_portfolio.json"):
    with open(filename, "w") as f:
        json.dump(portfolio, f, indent=4)
    print(f"✅ Exported portfolio to {filename}")

def export_to_csv(portfolio, filename="nft_portfolio.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Contract", "Name", "Symbol", "TokenID", "MetadataURI"])
        for contract, data in portfolio.items():
            for token in data["tokens"]:
                writer.writerow([contract, data["name"], data["symbol"], token, data.get("metadata_uris", {}).get(token, "")])
    print(f"✅ Exported portfolio to {filename}")

# Main execution
all_portfolio = {}

for chain in args.chains.split(","):
    chain = chain.strip().lower()
    print(f"\n⛓️ Fetching NFTs from {chain}...")
    txs = fetch_nfts(chain)
    portfolio, w3 = build_portfolio(txs, chain)

    # Fetch metadata and download images if requested, with progress bars
    for contract, data in tqdm(portfolio.items(), desc=f"{chain.upper()} Contracts"):
        for token in tqdm(data["tokens"], desc="Tokens", leave=False):
            metadata_uri = fetch_metadata(w3, contract, token)
            data.setdefault("metadata_uris", {})[token] = metadata_uri
            if args.save_images and metadata_uri:
                try:
                    meta = requests.get(metadata_uri, timeout=10).json()
                    image_url = resolve_ipfs(meta.get("image", ""))
                    if image_url:
                        download_image(image_url, args.folder, token, contract)
                except Exception as e:
                    print(f"⚠️ Failed fetching metadata for token {token}: {e}")

    all_portfolio.update(portfolio)
    sleep(1)  # avoid rate limiting

show_portfolio(all_portfolio)

if args.json:
    export_to_json(all_portfolio)
if args.csv:
    export_to_csv(all_portfolio)
if args.all:
    export_to_json(all_portfolio)
    export_to_csv(all_portfolio)
