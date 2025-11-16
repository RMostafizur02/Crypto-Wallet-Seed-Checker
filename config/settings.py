"""
Application settings and configuration
"""

import os
from dotenv import load_dotenv

load_dotenv()

# API Keys (set in .env file)
ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')
BSCSCAN_API_KEY = os.getenv('BSCSCAN_API_KEY')
POLYGONSCAN_API_KEY = os.getenv('POLYGONSCAN_API_KEY')
SNOWTRACE_API_KEY = os.getenv('SNOWTRACE_API_KEY')

# Application Settings
DEFAULT_BATCH_SIZE = 10
MAX_BATCH_SIZE = 100
RATE_LIMIT_REQUESTS_PER_SECOND = 5
DEFAULT_WORD_COUNT = 12

# File Paths
DEFAULT_WORDLIST_PATH = "config/wordlist.txt"
DEFAULT_CHAINS_CONFIG = "config/chains.json"
DEFAULT_OUTPUT_DIR = "results"

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "seed_checker.log"

# Blockchain Settings
SUPPORTED_CHAINS = [
    "bitcoin", "ethereum", "bsc", "polygon", "avalanche", 
    "arbitrum", "optimism", "dogecoin", "litecoin"
]

DERIVATION_PATHS = {
    "bitcoin_legacy": "m/44'/0'/0'/0/0",
    "bitcoin_segwit": "m/84'/0'/0'/0/0",
    "ethereum": "m/44'/60'/0'/0/0",
    "bsc": "m/44'/60'/0'/0/0",
    "polygon": "m/44'/60'/0'/0/0",
    "avalanche": "m/44'/60'/0'/0/0",
    "arbitrum": "m/44'/60'/0'/0/0",
    "optimism": "m/44'/60'/0'/0/0",
    "dogecoin": "m/44'/3'/0'/0/0",
    "litecoin": "m/44'/2'/0'/0/0",
}
