"""
Crypto Wallet Seed Checker
A high-performance tool for educational analysis of BIP-39 mnemonic phrases
"""

__version__ = "1.0.0"
__author__ = "Crypto Wallet Seed Checker Team"
__description__ = "Educational blockchain analysis tool"

from .core.seed_analyzer import SeedAnalyzer
from .core.bip39_generator import BIP39Generator
from .core.hd_wallet import HDWallet

__all__ = ['SeedAnalyzer', 'BIP39Generator', 'HDWallet']
