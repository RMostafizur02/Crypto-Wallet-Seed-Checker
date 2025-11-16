"""
Input validation utilities
"""

import os
import argparse
from typing import List

def validate_arguments(args: argparse.Namespace):
    """Validate command line arguments"""
    if args.generate and args.generate <= 0:
        raise ValueError("Number of seeds to generate must be positive")
    
    if args.batch_size <= 0:
        raise ValueError("Batch size must be positive")
    
    if args.batch_size > 100:
        print("⚠️  Warning: Large batch sizes may cause performance issues")
    
    if args.file and not os.path.exists(args.file):
        raise FileNotFoundError(f"Seed file not found: {args.file}")
    
    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)

def validate_mnemonic_format(mnemonic: str) -> List[str]:
    """Validate and parse mnemonic string"""
    words = mnemonic.strip().split()
    
    if len(words) not in [12, 15, 18, 21, 24]:
        raise ValueError(f"Mnemonic must have 12, 15, 18, 21, or 24 words (got {len(words)})")
    
    # Check if words contain only letters
    for word in words:
        if not word.isalpha():
            raise ValueError(f"Invalid word in mnemonic: {word}")
    
    return words

def validate_derivation_path(path: str) -> bool:
    """Validate BIP-44 derivation path format"""
    if not path.startswith('m/'):
        return False
    
    segments = path.split('/')[1:]
    
    for segment in segments:
        if segment.endswith("'"):
            if not segment[:-1].isdigit():
                return False
        else:
            if not segment.isdigit():
                return False
    
    return True
