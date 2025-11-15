#!/usr/bin/env python3
"""
Crypto Wallet Seed Checker - Main Entry Point
Educational Use Only
"""

import asyncio
import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.seed_analyzer import SeedAnalyzer
from utils.logger import setup_logging
from utils.validator import validate_arguments
import argparse
import logging

def print_banner():
    banner = """
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                CRYPTO WALLET SEED CHECKER v1.0.0                    ║
    ║                                                                    ║
    ║           🚨 EDUCATIONAL AND RESEARCH USE ONLY 🚨                 ║
    ║         Unauthorized access to wallets is ILLEGAL                 ║
    ║                                                                    ║
    ║      Supports: BTC, ETH, BSC, MATIC, DOGE, LTC + EVM chains       ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

async def main():
    print_banner()
    
    parser = argparse.ArgumentParser(
        description='Crypto Wallet Seed Checker - Educational Blockchain Analysis Tool'
    )
    
    # Operation modes
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('--generate', type=int, help='Generate and check N seed phrases')
    mode_group.add_argument('--file', type=str, help='Check seed phrases from file')
    mode_group.add_argument('--seed', type=str, help='Check a single seed phrase')
    
    # Configuration
    parser.add_argument('--words', type=int, choices=[12, 15, 18, 21, 24], default=12)
    parser.add_argument('--passphrase', type=str, default='')
    parser.add_argument('--batch-size', type=int, default=10)
    parser.add_argument('--output-dir', type=str, default='./results')
    parser.add_argument('--verbose', '-v', action='store_true')
    
    args = parser.parse_args()
    
    try:
        validate_arguments(args)
        setup_logging(args.verbose)
        
        analyzer = SeedAnalyzer()
        
        if args.seed:
            print(f"🔍 Checking single seed phrase...")
            await analyzer.check_single_seed(args.seed, args.passphrase)
            
        elif args.file:
            print(f"📁 Checking seeds from file: {args.file}")
            await analyzer.check_from_file(args.file, args.passphrase, args.batch_size)
            
        elif args.generate:
            print(f"🎯 Generating and checking {args.generate} seeds...")
            await analyzer.generate_and_check(args.generate, args.words, args.passphrase, args.batch_size)
            
    except Exception as e:
        logging.error(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
