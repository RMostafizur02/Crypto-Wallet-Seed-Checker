"""
BIP-39 Mnemonic Phrase Generator
"""

import secrets
import hashlib
import hmac
from typing import List, Optional
import os

class BIP39Generator:
    def __init__(self, wordlist_path: Optional[str] = None):
        self.wordlist = self._load_wordlist(wordlist_path)
    
    def _load_wordlist(self, wordlist_path: Optional[str] = None) -> List[str]:
        """Load BIP-39 wordlist"""
        if wordlist_path and os.path.exists(wordlist_path):
            with open(wordlist_path, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        else:
            # Use built-in wordlist
            return self._get_standard_wordlist()
    
    def _get_standard_wordlist(self) -> List[str]:
        """Return standard BIP-39 English wordlist"""
        # This would be the full 2048 words - truncated for example
        return [
            "abandon", "ability", "able", "about", "above", "absent", "absorb", "abstract",
            "absurd", "abuse", "access", "accident", "account", "accuse", "achieve", "acid",
            # ... full 2048 words would go here
            "zero", "zone", "zoo"
        ]
    
    def generate_entropy(self, strength: int = 128) -> bytes:
        """Generate cryptographically secure entropy"""
        if strength not in [128, 160, 192, 224, 256]:
            raise ValueError("Strength must be 128, 160, 192, 224, or 256 bits")
        
        return secrets.token_bytes(strength // 8)
    
    def entropy_to_mnemonic(self, entropy: bytes) -> List[str]:
        """Convert entropy to BIP-39 mnemonic phrase"""
        entropy_length = len(entropy) * 8
        checksum_length = entropy_length // 32
        
        # Calculate checksum
        hash_bytes = hashlib.sha256(entropy).digest()
        checksum_bits = bin(int.from_bytes(hash_bytes, 'big'))[2:].zfill(256)[:checksum_length]
        
        # Combine entropy and checksum
        entropy_bits = bin(int.from_bytes(entropy, 'big'))[2:].zfill(entropy_length)
        combined_bits = entropy_bits + checksum_bits
        
        # Split into 11-bit chunks and map to wordlist
        indices = [
            int(combined_bits[i:i+11], 2) 
            for i in range(0, len(combined_bits), 11)
        ]
        
        return [self.wordlist[index] for index in indices]
    
    def generate_mnemonic(self, word_count: int = 12) -> List[str]:
        """Generate a BIP-39 compliant mnemonic phrase"""
        strength_map = {12: 128, 15: 160, 18: 192, 21: 224, 24: 256}
        
        if word_count not in strength_map:
            raise ValueError("Word count must be 12, 15, 18, 21, or 24")
        
        entropy = self.generate_entropy(strength_map[word_count])
        return self.entropy_to_mnemonic(entropy)
    
    def validate_mnemonic(self, mnemonic: List[str]) -> bool:
        """Validate a BIP-39 mnemonic phrase"""
        try:
            # Convert words back to indices
            indices = [self.wordlist.index(word) for word in mnemonic]
            
            # Convert indices to bit string
            total_bits = len(mnemonic) * 11
            bit_string = ''.join([bin(index)[2:].zfill(11) for index in indices])
            
            # Extract entropy and checksum
            entropy_bits_length = (total_bits * 32) // 33
            checksum_bits_length = total_bits - entropy_bits_length
            
            entropy_bits = bit_string[:entropy_bits_length]
            checksum_bits = bit_string[entropy_bits_length:]
            
            # Convert entropy bits to bytes
            entropy = int(entropy_bits, 2).to_bytes(entropy_bits_length // 8, 'big')
            
            # Calculate expected checksum
            hash_bytes = hashlib.sha256(entropy).digest()
            expected_checksum = bin(int.from_bytes(hash_bytes, 'big'))[2:].zfill(256)[:checksum_bits_length]
            
            return checksum_bits == expected_checksum
            
        except (ValueError, IndexError):
            return False
    
    def mnemonic_to_seed(self, mnemonic: List[str], passphrase: str = "") -> bytes:
        """Convert mnemonic to seed using BIP-39 specification"""
        mnemonic_str = " ".join(mnemonic)
        salt = f"mnemonic{passphrase}".encode('utf-8')
        
        return hashlib.pbkdf2_hmac(
            'sha512',
            mnemonic_str.encode('utf-8'),
            salt,
            2048,
            64
        )
