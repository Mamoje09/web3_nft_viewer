# NFT Metadata & Portfolio Viewer 🎨  

A Python toolkit to explore NFTs:  
- Fetch **metadata + images** for a single NFT (ERC-721)  
- List **all NFTs owned by a wallet** in a given collection  
- Fetch **multi-chain NFT portfolio** (Ethereum, Polygon, BSC)  
- Export portfolio to **JSON/CSV**  
- Optionally **download NFT images** locally  

---

## ✨ Features
- ✅ Single NFT lookup with `--contract` and `--token`  
- ✅ Full wallet portfolio across **Ethereum, Polygon, BSC**  
- ✅ Restrict portfolio by **contract**  
- ✅ Export to **JSON** / **CSV**  
- ✅ Save NFT images (`--save-images`)  
- ✅ CLI flags for flexibility  


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


🔹 Single NFT Viewer

Fetch metadata + image:

python nft_viewer.py


Override Defaults:

python nft_viewer.py --wallet 0x123... --contract 0xABC... --token 42


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

🔹 Wallet NFTs in a Collection

python nft_viewer.py


Example output:

📦 Wallet 0x123... owns 2 NFTs in this collection.

🔎 Token ID: 1

🔎 Token ID: 27



🔹 Multi-Chain NFT Portfolio

Ethereum only (default):

python nft_portfolio.py


Multiple chains:

python nft_portfolio.py --chains eth,polygon,bsc


Restrict by contract:

python nft_portfolio.py --contract 0xBC4CA0e...


Export:

python nft_portfolio.py --json

python nft_portfolio.py --csv

python nft_portfolio.py --all


Save images:

python nft_portfolio.py --save-images --folder nft_images


Limit results:

python nft_portfolio.py --limit 10


---

📸 Demo


Console output (metadata & portfolio)

Example JSON/CSV export files

Sample NFT images saved locally

---

🛠 Roadmap


Add ERC-1155 support

Google Sheets export

Simple FastAPI dashboard

---

📬 About Me

I’m Mamo (GitHub: mamoje09)

I'm a backend engineer expanding into Web3.

This is my fourth Web3 project showcasing:

ERC-721 smart contracts

IPFS metadata

Multi-chain RPC + API integration
