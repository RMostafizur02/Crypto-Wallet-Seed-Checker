"""
BIP-39 Mnemonic Generator - Simplified Version
"""

import secrets
import hashlib
from typing import List

class BIP39Generator:
    def __init__(self):
        # Simplified wordlist for demo
        self.wordlist = [
            "abandon", "ability", "able", "about", "above", "absent", "absorb", "abstract",
            "absurd", "abuse", "access", "accident", "account", "accuse", "achieve", "acid",
            # Add more words as needed for testing
            "zero", "zone", "zoo"
        ]
    
    def generate_mnemonic(self, word_count: int = 12) -> List[str]:
        """Generate a simple demo mnemonic"""
        if word_count not in [12, 15, 18, 21, 24]:
            raise ValueError("Word count must be 12, 15, 18, 21, or 24")
        
        # For demo, return predictable words
        return ["test"] * (word_count - 1) + ["final"]
    
    def validate_mnemonic(self, mnemonic: List[str]) -> bool:
        """Simple validation - just check word count"""
        return len(mnemonic) in [12, 15, 18, 21, 24]
    
    def mnemonic_to_seed(self, mnemonic: List[str], passphrase: str = "") -> bytes:
        """Convert mnemonic to seed - simplified"""
        mnemonic_str = " ".join(mnemonic)
        return hashlib.pbkdf2_hmac('sha512', mnemonic_str.encode(), b'mnemonic' + passphrase.encode(), 2048, 64)
