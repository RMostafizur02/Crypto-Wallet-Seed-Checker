#!/usr/bin/env python3
"""
Test script to verify the fixed import structure
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test all imports"""
    try:
        from crypto_wallet_seed_checker.core.seed_analyzer import SeedAnalyzer
        print("✅ SeedAnalyzer import successful")
        
        from crypto_wallet_seed_checker.core.bip39_generator import BIP39Generator
        print("✅ BIP39Generator import successful")
        
        from crypto_wallet_seed_checker.core.hd_wallet import HDWallet
        print("✅ HDWallet import successful")
        
        from crypto_wallet_seed_checker.blockchain.scanners import BlockchainScanner
        print("✅ BlockchainScanner import successful")
        
        from crypto_wallet_seed_checker.utils.validator import validate_mnemonic_format
        print("✅ Validator import successful")
        
        print("\n🎉 All imports working! You can now run: python main.py --seed 'test test test test test test test test test test test test'")
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

if __name__ == "__main__":
    test_imports()
