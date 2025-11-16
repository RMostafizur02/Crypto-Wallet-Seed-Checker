# Crypto Wallet Seed Checker - Usage Guide

## 🚀 Quick Start

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/crypto-wallet-seed-checker.git
cd crypto-wallet-seed-checker

# Install dependencies
pip install -r requirements.txt



Basic Usage
bash
# Check a single seed phrase
python main.py --seed "abandon ability able about above absent absorb abstract absurd abuse access accident"

# Generate and check 100 random seeds
python main.py --generate 100 --words 12

# Check seeds from a file
python main.py --file seeds.txt --output-dir ./results
📋 Command Line Options
Option	Description	Default
--seed SEED	Check a single seed phrase	-
--generate N	Generate and check N seeds	-
--file FILE	Check seeds from text file	-
--words COUNT	Words in mnemonic (12,15,18,21,24)	12
--passphrase PASS	BIP-39 passphrase	""
--batch-size N	Concurrent checking batch size	10
--output-dir DIR	Output directory for results	./results
--verbose	Enable verbose logging	False
🔧 Advanced Usage
Custom Wordlists
bash
# Use custom wordlist file
python main.py --generate 1000 --wordlist custom_words.txt
Specific Derivation Paths
bash
# Use custom derivation path
python main.py --seed "your seed" --derivation "m/44'/60'/0'/0/0"
API Configuration
Create a .env file for API keys:

env
ETHERSCAN_API_KEY=your_etherscan_key
BSCSCAN_API_KEY=your_bscscan_key
POLYGONSCAN_API_KEY=your_polygonscan_key
📊 Output Formats
The tool supports multiple output formats:

Console Output
text
🎯 Crypto Wallet Seed Checker - Scan Results
===========================================
📅 Timestamp: 2024-01-15 10:30:45
🔍 Seeds Checked: 1,250
💰 Wallets with Balance: 3
⏱️  Execution Time: 2m 15s
File Exports
JSON: Complete results with metadata

CSV: Tabular data for analysis

TXT: Human-readable summary

Log Files
seed_checker.log: All wallets with balances

seed_checker_runtime.log: Detailed execution logs

🔄 Batch Processing
Large-scale Scanning
bash
# Scan 10,000 seeds with optimal settings
python main.py --generate 10000 --words 12 --batch-size 50 --output-dir ./large_scan
Resume Scanning
The tool maintains state and can resume interrupted scans.

⚙️ Configuration
Custom Settings
Edit config/settings.py for:

API rate limiting

Default batch sizes

Custom derivation paths

Logging configuration

Supported Blockchains
Bitcoin (Legacy, SegWit)

Ethereum & EVM chains

Binance Smart Chain

Polygon

Avalanche

Arbitrum

Optimism

Dogecoin

Litecoin

🐛 Troubleshooting
Common Issues
Import Errors

bash
# Make sure you're in the correct directory
cd crypto-wallet-seed-checker

# Install dependencies
pip install -r requirements.txt
API Rate Limiting

bash
# Reduce batch size and add delays
python main.py --generate 1000 --batch-size 5
Memory Issues

bash
# Use smaller batches for large scans
python main.py --generate 50000 --batch-size 10
Getting Help
Check the log files for detailed error information

Run with --verbose flag for debug output

Check the API documentation for integration help

Review security guidelines for best practices

🎯 Examples
Basic Scan
bash
python main.py --seed "zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo party"
Educational Research
bash
# Study common seed patterns
python main.py --generate 5000 --words 12 --output-dir ./research
Security Testing
bash
# Test your own wallets (educational only)
python main.py --file my_wallets.txt --passphrase "mypass"
Remember: This tool is for educational and research purposes only.

text

### `docs/api.md`
```markdown
# Crypto Wallet Seed Checker - API Documentation

## 📦 Package Structure
crypto-wallet-seed-checker/
├── core/ # Core functionality
├── blockchain/ # Blockchain scanners
├── utils/ # Utilities
└── config/ # Configuration

text

## 🔧 Core API

### SeedAnalyzer Class
Main class for seed analysis operations.

```python
from src.core.seed_analyzer import SeedAnalyzer

# Initialize analyzer
analyzer = SeedAnalyzer()

# Check single seed
result = await analyzer.check_single_seed(
    "abandon ability able about above absent absorb abstract absurd abuse access accident",
    "passphrase"
)

# Generate and check multiple seeds
results = await analyzer.generate_and_check(
    count=1000,
    word_count=12,
    passphrase="",
    batch_size=50
)

# Check seeds from file
results = await analyzer.check_from_file(
    filename="seeds.txt",
    passphrase="",
    batch_size=20
)
BIP39Generator Class
BIP-39 mnemonic generation and validation.

python
from src.core.bip39_generator import BIP39Generator

generator = BIP39Generator()

# Generate mnemonic
mnemonic = generator.generate_mnemonic(word_count=12)

# Validate mnemonic
is_valid = generator.validate_mnemonic(mnemonic)

# Generate seed
seed = generator.mnemonic_to_seed(mnemonic, "passphrase")
HDWallet Class
Hierarchical Deterministic wallet operations.

python
from src.core.hd_wallet import HDWallet

# Create wallet from seed
wallet = HDWallet(seed)

# Derive keys for path
private_key, chain_code = wallet.derive_path("m/44'/0'/0'/0/0")

# Get standard derivation paths
paths = HDWallet.get_derivation_paths()
🔗 Blockchain API
BlockchainScanner Class
Orchestrates scanning across multiple blockchains.

python
from src.blockchain.scanners import BlockchainScanner

scanner = BlockchainScanner()

# Scan addresses across all chains
results = await scanner.scan_addresses(addresses)

# Scan single chain
result = await scanner.scan_single_chain("bitcoin", address)
Individual Scanners
python
from src.blockchain.bitcoin import BitcoinScanner
from src.blockchain.ethereum import EthereumScanner
from src.blockchain.evm_chains import EVMChainScanner

# Bitcoin
btc_scanner = BitcoinScanner()
address = btc_scanner.derive_address(public_key, "legacy")
balance = await btc_scanner.check_balance(address)

# Ethereum
eth_scanner = EthereumScanner(api_key="your_key")
balance = await eth_scanner.check_balance(address)

# EVM Chains
bsc_scanner = EVMChainScanner("bsc", api_key="your_key")
balance = await bsc_scanner.check_balance(address)
🛠️ Utilities API
Logger Class
Result logging and tracking.

python
from src.utils.logger import Logger, setup_logging

# Setup logging
setup_logging(verbose=True)

# Initialize logger
logger = Logger("custom_log.log")

# Log hits
logger.log_hit(result)

# Get summary
summary = logger.get_summary()
ResultExporter Class
Export results in multiple formats.

python
from src.utils.exporter import ResultExporter

exporter = ResultExporter()

# Export results
exporter.export_results(
    results=results,
    filename="./results/scan.json",
    format="json"
)

exporter.export_results(
    results=results,
    filename="./results/scan.csv", 
    format="csv"
)

exporter.export_results(
    results=results,
    filename="./results/scan.txt",
    format="txt"
)
Validator Functions
Input validation utilities.

python
from src.utils.validator import (
    validate_arguments,
    validate_mnemonic_format,
    validate_derivation_path
)

# Validate command line arguments
validate_arguments(args)

# Validate mnemonic format
words = validate_mnemonic_format(mnemonic_string)

# Validate derivation path
is_valid = validate_derivation_path("m/44'/0'/0'/0/0")
⚙️ Configuration API
Settings
Application configuration.

python
from config.settings import (
    ETHERSCAN_API_KEY,
    DEFAULT_BATCH_SIZE,
    SUPPORTED_CHAINS,
    DERIVATION_PATHS
)

# Use settings in your code
api_key = ETHERSCAN_API_KEY
batch_size = DEFAULT_BATCH_SIZE
supported_chains = SUPPORTED_CHAINS
Chain Configuration
python
import json

# Load chain configurations
with open("config/chains.json", "r") as f:
    chains_config = json.load(f)

# Access specific chain config
btc_config = chains_config["bitcoin"]
eth_config = chains_config["ethereum"]
🔌 Integration Examples
Custom Scanner Implementation
python
from src.core.seed_analyzer import SeedAnalyzer
from src.blockchain.scanners import BlockchainScanner

class CustomScanner(BlockchainScanner):
    async def scan_addresses(self, addresses):
        # Custom scanning logic
        results = {}
        for chain, address_data in addresses.items():
            # Your custom scanning implementation
            results[chain] = await self.custom_scan_method(address_data)
        return results

# Use custom scanner
analyzer = SeedAnalyzer()
analyzer.scanner = CustomScanner()
Batch Processing with Progress
python
import asyncio
from tqdm import tqdm

async def batch_process_with_progress(analyzer, seeds, batch_size=10):
    results = []
    
    for i in tqdm(range(0, len(seeds), batch_size)):
        batch = seeds[i:i + batch_size]
        batch_tasks = [analyzer.check_single_seed(seed) for seed in batch]
        batch_results = await asyncio.gather(*batch_tasks)
        results.extend(batch_results)
    
    return results
Custom Export Format
python
from src.utils.exporter import ResultExporter

class CustomExporter(ResultExporter):
    def _export_custom(self, results, filename):
        # Custom export logic
        with open(filename, 'w') as f:
            for result in results:
                if result.get('has_balance'):
                    f.write(f"HIT: {result['mnemonic']}\n")

# Use custom exporter
exporter = CustomExporter()
exporter.export_formats.append('custom')
🧪 Testing API
Running Tests
bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_bip39.py

# Run with coverage
pytest --cov=src tests/
Writing Tests
python
import pytest
from src.core.bip39_generator import BIP39Generator

class TestCustomFunctionality:
    def setup_method(self):
        self.generator = BIP39Generator()
    
    def test_custom_feature(self):
        # Test implementation
        result = self.generator.custom_method()
        assert result == expected_value
    
    @pytest.mark.asyncio
    async def test_async_feature(self):
        result = await async_function()
        assert result is not None
📈 Performance Tips
Optimizing Large Scans
python
# Use appropriate batch sizes
analyzer = SeedAnalyzer()

# For API-heavy operations
results = await analyzer.generate_and_check(
    count=10000,
    batch_size=5,  # Smaller batches for API limits
    word_count=12
)

# For local operations  
results = await analyzer.generate_and_check(
    count=10000,
    batch_size=100,  # Larger batches for local processing
    word_count=12
)
Memory Management
python
# Process results in chunks to avoid memory issues
chunk_size = 1000
for i in range(0, len(large_results), chunk_size):
    chunk = large_results[i:i + chunk_size]
    exporter.export_results(chunk, f"results_chunk_{i}.json")
