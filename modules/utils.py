"""
Utilities - Simplified Version
"""

from typing import List

def validate_mnemonic_format(mnemonic: str) -> List[str]:
    """Validate mnemonic format"""
    words = mnemonic.strip().split()
    
    if len(words) not in [12, 15, 18, 21, 24]:
        raise ValueError(f"Mnemonic must have 12, 15, 18, 21, or 24 words (got {len(words)})")
    
    return words

class Logger:
    def __init__(self, log_file: str = "seed_checker.log"):
        self.log_file = log_file
        self.hits = []
    
    def log_hit(self, result):
        """Log a hit"""
        print(f"💰 HIT FOUND: {result.get('mnemonic', 'Unknown')}")
        self.hits.append(result)
