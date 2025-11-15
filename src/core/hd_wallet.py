"""
Hierarchical Deterministic Wallet Implementation
"""

import hmac
import hashlib
import struct
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class DerivationPath:
    purpose: int
    coin_type: int
    account: int
    change: int
    address_index: int
    
    def to_string(self) -> str:
        return f"m/{self.purpose}'/{self.coin_type}'/{self.account}'/{self.change}/{self.address_index}"

class HDWallet:
    def __init__(self, seed: bytes):
        self.seed = seed
        self.master_private_key, self.master_chain_code = self._generate_master_keys()
    
    def _generate_master_keys(self) -> Tuple[bytes, bytes]:
        """Generate master private key and chain code from seed"""
        # HMAC-SHA512 with "Bitcoin seed" as key
        hmac_result = hmac.new(b"Bitcoin seed", self.seed, hashlib.sha512).digest()
        private_key = hmac_result[:32]
        chain_code = hmac_result[32:]
        return private_key, chain_code
    
    def derive_child_key(self, private_key: bytes, chain_code: bytes, index: int) -> Tuple[bytes, bytes]:
        """Derive child key using BIP-32"""
        if index & 0x80000000:
            # Hardened derivation
            data = b'\x00' + private_key + struct.pack('>I', index)
        else:
            # Normal derivation - would need public key in real implementation
            data = private_key + struct.pack('>I', index)
        
        hmac_result = hmac.new(chain_code, data, hashlib.sha512).digest()
        child_private_key = hmac_result[:32]
        child_chain_code = hmac_result[32:]
        
        return child_private_key, child_chain_code
    
    def derive_path(self, path: str) -> Tuple[bytes, bytes]:
        """Derive keys for a specific BIP-44 path"""
        if not path.startswith('m/'):
            raise ValueError("Path must start with 'm/'")
        
        segments = path.split('/')[1:]
        private_key = self.master_private_key
        chain_code = self.master_chain_code
        
        for segment in segments:
            if segment.endswith("'"):
                # Hardened
                index = int(segment[:-1]) + 0x80000000
            else:
                # Normal
                index = int(segment)
            
            private_key, chain_code = self.derive_child_key(private_key, chain_code, index)
        
        return private_key, chain_code
    
    @staticmethod
    def get_derivation_paths() -> Dict[str, DerivationPath]:
        """Get standard derivation paths for different blockchains"""
        return {
            "bitcoin_legacy": DerivationPath(44, 0, 0, 0, 0),
            "bitcoin_segwit": DerivationPath(84, 0, 0, 0, 0),
            "ethereum": DerivationPath(44, 60, 0, 0, 0),
            "bsc": DerivationPath(44, 60, 0, 0, 0),
            "polygon": DerivationPath(44, 60, 0, 0, 0),
            "dogecoin": DerivationPath(44, 3, 0, 0, 0),
            "litecoin": DerivationPath(44, 2, 0, 0, 0),
        }
