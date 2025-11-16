"""
Tests for BIP-39 generator
"""

import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.bip39_generator import BIP39Generator

class TestBIP39Generator:
    def setup_method(self):
        self.generator = BIP39Generator()
    
    def test_generate_entropy(self):
        """Test entropy generation for different strengths"""
        for strength in [128, 160, 192, 224, 256]:
            entropy = self.generator.generate_entropy(strength)
            assert len(entropy) == strength // 8
    
    def test_generate_mnemonic(self):
        """Test mnemonic generation for different word counts"""
        for word_count in [12, 15, 18, 21, 24]:
            mnemonic = self.generator.generate_mnemonic(word_count)
            assert len(mnemonic) == word_count
            # All words should be in wordlist
            for word in mnemonic:
                assert word in self.generator.wordlist
    
    def test_validate_mnemonic(self):
        """Test mnemonic validation"""
        # Test valid mnemonic
        valid_mnemonic = self.generator.generate_mnemonic(12)
        assert self.generator.validate_mnemonic(valid_mnemonic) == True
        
        # Test invalid mnemonic
        invalid_mnemonic = valid_mnemonic.copy()
        invalid_mnemonic[0] = "invalidword"
        assert self.generator.validate_mnemonic(invalid_mnemonic) == False
    
    def test_mnemonic_to_seed(self):
        """Test seed generation from mnemonic"""
        mnemonic = ["abandon"] * 11 + ["about"]
        seed = self.generator.mnemonic_to_seed(mnemonic, "testpass")
        
        assert len(seed) == 64  # 512 bits
        assert isinstance(seed, bytes)
    
    def test_invalid_word_count(self):
        """Test error for invalid word count"""
        with pytest.raises(ValueError):
            self.generator.generate_mnemonic(13)
