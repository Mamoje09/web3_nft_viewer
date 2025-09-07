import os
import requests
import csv
import json
import argparse
from dotenv import load_dotenv

load_dotenv()

etherscan_api = os.getenv("ETHERSCAN_API_KEY")
wallet = os.getenv("WALLET_ADDRESS")

if not etherscan_api or not wallet:
    raise SystemExit("❌ Please set ETHERSCAN_API_KEY and WALLET_ADDRESS in .env")

BASE_URL = "https://api.etherscan.io/api"

def get_wallet_nfts(wallet: str):
    """Fetch NFT transfer history for a wallet"""
    url = f"{BASE_URL}?module=account&action=tokennfttx&address={wallet}&page=1&offset=100&sort=desc&apikey={etherscan_api}"
    resp = requests.get(url).json()

    if resp["status"] != "1":
        print("❌ No NFTs found or API error.")
        return []

    return resp["result"]

def build_portfolio(transactions):
    """Group NFTs by contract and return dict"""
    portfolio = {}

    for tx in transactions:
        contract = tx["contractAddress"]
        token_id = tx["tokenID"]
        name = tx.get("tokenName", "UnknownNFT")
        symbol = tx.get("tokenSymbol", "")

        if contract not in portfolio:
            portfolio[contract] = {"name": name, "symbol": symbol, "tokens": []}
        if token_id not in portfolio[contract]["tokens"]:
            portfolio[contract]["tokens"].append(token_id)

    return portfolio

def show_portfolio(portfolio):
    """Print portfolio summary"""
    print(f"\n👛 NFT Portfolio for {wallet}")
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
        writer.writerow(["Contract", "Name", "Symbol", "TokenID"])
        for contract, data in portfolio.items():
            for token in data["tokens"]:
                writer.writerow([contract, data["name"], data["symbol"], token])
    print(f"✅ Exported portfolio to {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NFT Portfolio Tracker")
    parser.add_argument("--json", action="store_true", help="Export portfolio to JSON")
    parser.add_argument("--csv", action="store_true", help="Export portfolio to CSV")
    parser.add_argument("--all", action="store_true", help="Export portfolio to JSON and CSV")
    args = parser.parse_args()

    txs = get_wallet_nfts(wallet)
    portfolio = build_portfolio(txs)
    show_portfolio(portfolio)

    if args.json:
        export_to_json(portfolio)
    if args.csv:
        export_to_csv(portfolio)
    if args.all:
        export_to_json(portfolio)
        export_to_csv(portfolio)
