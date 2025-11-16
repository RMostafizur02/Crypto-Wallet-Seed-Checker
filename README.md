# 🔐 Crypto Wallet Seed Checker

> ⚠️ **SECURITY DISCLAIMER**: This tool is for **EDUCATIONAL AND RESEARCH purposes ONLY**. Unauthorized use for accessing wallets you don't own is **STRICTLY FORBIDDEN and ILLEGAL**.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

A high-performance tool designed to generate and analyze BIP-39 mnemonic phrases, automatically derive wallet addresses, and check for any existing balances across multiple blockchain networks.

---

## 🚀 Features

### ✅ BIP-39 Mnemonic Generator
- Generates standard-compliant mnemonic phrases using the official 2048-word English list
- Supports 12, 15, 18, 21, and 24-word phrases
- Custom wordlist and phrase filtering support

### ✅ Hierarchical Deterministic Wallet Derivation
- **Bitcoin**: `m/44'/0'/0'/0/0` (Legacy), `m/84'/0'/0'/0/0` (Native SegWit)
- **Ethereum**: `m/44'/60'/0'/0/0`
- **Custom derivation paths** supported
- BIP-32, BIP-44, and BIP-84 compliant

### ✅ Multi-Blockchain Support
| Blockchain | Address Types | APIs |
|------------|---------------|------|
| **Bitcoin (BTC)** | Legacy, SegWit, Bech32 | Blockchair, Blockstream |
| **Ethereum (ETH)** | ETH & ERC-20 tokens | Etherscan |
| **Binance Smart Chain** | BEP-20 tokens | BscScan |
| **Polygon (MATIC)** | MATIC & tokens | Polygonscan |
| **Avalanche (AVAX)** | C-Chain | SnowTrace |
| **Arbitrum One** | ETH & tokens | Arbiscan |
| **Optimism** | ETH & tokens | Optimistic Etherscan |
| **Dogecoin (DOGE)** | Legacy | Dogechain |
| **Litecoin (LTC)** | Legacy, SegWit | Blockchair |

### ✅ High-Performance Scanning
- Multi-threaded execution for scanning thousands of phrases per minute
- Fast API-based scanning with public blockchain explorers
- Async/await architecture for optimal performance
- Configurable batch sizes and rate limiting

### ✅ Advanced Features
- Custom wordlist support for targeted scanning
- Passphrase-protected wallet support
- Real-time progress tracking
- Comprehensive result logging and export
- Balance history and transaction tracking

---

## 📦 Installation

### Method 1: From Source
```bash
git clone https://github.com/yourusername/crypto-wallet-seed-checker.git
cd crypto-wallet-seed-checker
pip install -r requirements.txt
Method 2: PIP Installation
bash
pip install crypto-wallet-seed-checker
🛠️ Quick Start
Basic Usage
python
from crypto_wallet_seed_checker import SeedChecker

# Initialize checker
checker = SeedChecker()

# Check a single seed
result = checker.check_seed(
    "abandon ability able about above absent absorb abstract absurd abuse access accident"
)

# Generate and check multiple seeds
results = checker.generate_and_check(
    count=1000,
    word_count=12,
    batch_size=50
)
Command Line Interface
bash
# Check single seed
python main.py --seed "your seed phrase here"

# Generate and check 1000 random seeds
python main.py --generate 1000 --words 12 --batch-size 50

# Check seeds from file
python main.py --file seeds.txt --output-dir ./results

# Advanced: Custom wordlist and derivation
python main.py --generate 5000 --words 24 --wordlist custom_words.txt --derivation "m/44'/60'/0'/0/0"
⚙️ Configuration
Supported Derivation Paths
json
{
  "bitcoin_legacy": "m/44'/0'/0'/0/0",
  "bitcoin_segwit": "m/84'/0'/0'/0/0", 
  "ethereum": "m/44'/60'/0'/0/0",
  "bsc": "m/44'/60'/0'/0/0",
  "dogecoin": "m/44'/3'/0'/0/0",
  "litecoin": "m/44'/2'/0'/0/0"
}
API Configuration
python
# config/settings.py
API_CONFIG = {
    "etherscan": "YOUR_API_KEY",
    "bscscan": "YOUR_API_KEY", 
    "rate_limit": 5  # requests per second
}
📊 Output Examples
Console Output
text
🎯 Crypto Wallet Seed Checker - Scan Results
===========================================
📅 Timestamp: 2024-01-15 10:30:45
🔍 Seeds Checked: 1,250
💰 Wallets with Balance: 3
⏱️  Execution Time: 2m 15s

💎 HITS FOUND:
-------------------------------------------
1. BTC: 0.15432001 BTC ($4,235.50)
   Address: bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh
   Mnemonic: abandon ability able about above absent absorb abstract absurd abuse access accident

2. ETH: 1.254300 ETH ($2,845.20)  
   Address: 0x742d35Cc6634C0532925a3b8Dc9F1a4C56b4a6a1
   Mnemonic: zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo party
Export Formats
JSON: Complete scan results with metadata

CSV: Tabular data for analysis

TXT: Human-readable summary

Log File: Continuous operation logging

🏗️ Project Structure
text
crypto-wallet-seed-checker/
├── 📁 src/
│   ├── 📁 core/
│   │   ├── bip39_generator.py
│   │   ├── hd_wallet.py
│   │   └── seed_analyzer.py
│   ├── 📁 blockchain/
│   │   ├── bitcoin.py
│   │   ├── ethereum.py
│   │   ├── evm_chains.py
│   │   └── scanners.py
│   └── 📁 utils/
│       ├── logger.py
│       ├── exporter.py
│       └── validator.py
├── 📁 config/
│   ├── chains.json
│   ├── wordlist.txt
│   └── settings.py
├── 📁 tests/
│   ├── test_bip39.py
│   ├── test_wallet.py
│   └── test_scanner.py
├── 📁 docs/
│   ├── usage.md
│   ├── api.md
│   └── security.md
├── 📁 examples/
│   ├── basic_usage.py
│   ├── batch_scan.py
│   └── custom_wordlist.py
├── 📄 requirements.txt
├── 📄 setup.py
├── 📄 main.py
└── 📄 README.md
🛡️ Security & Legal
🔒 Security Features
No internet connection required for generation

Local processing only (optional API calls)

Secure entropy generation

No data persistence unless explicitly exported

⚖️ Legal Compliance
Educational Use Only: This tool is for security research and educational purposes

No Warranty: Use at your own risk

Compliance: Users must comply with local laws and regulations

Ethical Use: Only test wallets you own or have explicit permission to analyze

🚫 Prohibited Uses
Accessing wallets without authorization

Illegal activities of any kind

Commercial exploitation without permission

Mass scanning of random seeds for profit

🤝 Contributing
We welcome contributions for educational improvements:

Fork the repository

Create a feature branch: git checkout -b feature/improvement

Commit changes: git commit -m 'Add educational feature'

Push to branch: git push origin feature/improvement

Open a Pull Request

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
BIP-39 Specification Authors

Bitcoin & Ethereum Development Communities

Blockchain Explorer API Providers

Cryptography Research Community

❓ FAQ
Q: Is this tool legal to use?
A: Yes, for educational and research purposes. No, for unauthorized access to wallets.

Q: How many seeds can I check per minute?
A: Typically 500-2000 seeds/minute depending on API limits and hardware.

Q: Can I use custom derivation paths?
A: Yes, fully customizable derivation paths are supported.

Q: Are my scanned seeds stored anywhere?
A: No, unless you explicitly enable logging or export results.

<div align="center">
🔐 Use Responsibly • 🎓 Learn Continuously • ⚖️ Stay Legal

For educational and research purposes only

</div>
📞 Support
📚 Full Documentation

🔧 API Reference

🛡️ Security Guidelines

🐛 Report Issues

<div align="center">
Made with ❤️ for the blockchain education community

</div> ```
