# NFT Metadata & Portfolio Viewer 🎨  

A Python tool to explore NFTs:  
- Fetch **metadata + images** for a single NFT (ERC-721)  
- List **all NFTs owned by a wallet** in a given collection  
- Fetch **NFT portfolio across all collections** using the Etherscan API  
- Export portfolio to **JSON or CSV** with simple CLI flags  

---

## ✨ Features
- ✅ Fetch single NFT metadata by **Token ID**  
- ✅ List all NFTs in a collection owned by a wallet  
- ✅ Fetch NFT portfolio across **all contracts** via Etherscan API  
- ✅ Export portfolio to **JSON**  
- ✅ Export portfolio to **CSV**  
- ✅ CLI support (`--json`, `--csv`, `--all`)  

---

## 📂 Project Structure

web3_nft_viewer/

├── nft_viewer.py # Single NFT & collection explorer

├── nft_portfolio.py # Wallet NFT portfolio tracker

├── requirements.txt # Dependencies

├── README.md # Documentation
 
└── .env # Local environment variables (ignored by Git)

---

▶️ Usage
🔹 View a Single NFT

Fetch metadata + image for TOKEN_ID:

python nft_viewer.py

---

Example Output:

🔎 Checking NFT 1 in contract 0xbc4c...
🌐 Token URI: https://ipfs.io/ipfs/Qm12345...
📜 NFT Metadata:
   name: Bored Ape #1
   description: A unique ape NFT
   attributes: [{ "trait_type": "Background", "value": "Orange" }]
🖼️ NFT Image: https://ipfs.io/ipfs/Qm67890...


---

🔹 View All NFTs in a Collection

Lists every token owned by your wallet in the given NFT_CONTRACT:

python nft_viewer.py


Example Output:

📦 Wallet 0x123... owns 2 NFTs in this collection.

🔎 Token ID: 1
   name: Bored Ape #1
   description: A unique ape NFT
   attributes: [...]
🖼️ NFT Image: https://ipfs.io/ipfs/Qm67890...

🔎 Token ID: 27
   name: Bored Ape #27
   description: Another unique ape
   attributes: [...]
🖼️ NFT Image: https://ipfs.io/ipfs/Qm13579...


---

🔹 NFT Portfolio (All Contracts)

Fetches all NFT collections your wallet owns using Etherscan API:

python nft_portfolio.py


Example Output:

👛 NFT Portfolio for 0x123...

📦 BoredApeYachtClub (BAYC)
   Contract: 0xbc4c...
   Tokens: 1, 14, 27

📦 PudgyPenguins (PPG)
   Contract: 0xbd35...
   Tokens: 998

---

🔹 Export Portfolio (CLI Flags)

Choose export formats:

python nft_portfolio.py --json    # Export to JSON
python nft_portfolio.py --csv     # Export to CSV
python nft_portfolio.py --all     # Export both

---

Example Exported Files

nft_portfolio.json

nft_portfolio.csv

---

📸 Demo

Console output (NFT metadata & portfolio)

Example JSON/CSV exports

---

🛠 Roadmap

Add support for ERC-1155 (multi-token standard)

Add NFT image auto-downloader

Export directly to Google Sheets

Build a simple FastAPI dashboard

---

📬 About Me

I’m Mamo (GitHub: mamoje09
I'm a backend engineer expanding into Web3.
This is my fourth Web3 project, showcasing skills in ERC-721 smart contracts, IPFS metadata and Etherscan API integration.
