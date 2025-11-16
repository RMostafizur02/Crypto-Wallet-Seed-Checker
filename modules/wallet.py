"""
HD Wallet - Simplified Version
"""

import hashlib
import hmac
from typing import Dict, Tuple
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
    
    def derive_path(self, path: str) -> Tuple[bytes, bytes]:
        """Simple path derivation for demo"""
        # For demo, return deterministic values based on seed and path
        data = self.seed + path.encode()
        private_key = hashlib.sha256(data).digest()[:32]
        chain_code = hashlib.sha256(data).digest()[32:64]
        return private_key, chain_code
    
    @staticmethod
    def get_derivation_paths() -> Dict[str, DerivationPath]:
        """Get standard derivation paths"""
        return {
            "bitcoin": DerivationPath(44, 0, 0, 0, 0),
            "ethereum": DerivationPath(44, 60, 0, 0, 0),
            "bsc": DerivationPath(44, 60, 0, 0, 0),
        }
