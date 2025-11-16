"""
Tests for HD wallet functionality
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.hd_wallet import HDWallet, DerivationPath
from core.bip39_generator import BIP39Generator

class TestHDWallet:
    def setup_method(self):
        self.generator = BIP39Generator()
        mnemonic = ["test"] * 12
        seed = self.generator.mnemonic_to_seed(mnemonic)
        self.wallet = HDWallet(seed)
    
    def test_derivation_path(self):
        """Test derivation path creation"""
        path = DerivationPath(44, 0, 0, 0, 0)
        assert path.to_string() == "m/44'/0'/0'/0/0"
    
    def test_get_derivation_paths(self):
        """Test getting standard derivation paths"""
        paths = HDWallet.get_derivation_paths()
        
        expected_chains = [
            "bitcoin_legacy", "bitcoin_segwit", "ethereum", 
            "bsc", "polygon", "dogecoin", "litecoin"
        ]
        
        for chain in expected_chains:
            assert chain in paths
            assert isinstance(paths[chain], DerivationPath)
    
    def test_derive_path(self):
        """Test path derivation"""
        # Test basic path derivation
        private_key, chain_code = self.wallet.derive_path("m/44'/0'/0'/0/0")
        
        assert len(private_key) == 32
        assert len(chain_code) == 32
        assert isinstance(private_key, bytes)
        assert isinstance(chain_code, bytes)
    
    def test_invalid_path(self):
        """Test error for invalid path"""
        with pytest.raises(ValueError):
            self.wallet.derive_path("invalid/path")
