#!/usr/bin/env python3
"""
Basic usage example for Crypto Wallet Seed Checker
Educational Use Only
"""

import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.seed_analyzer import SeedAnalyzer
from utils.logger import setup_logging

async def main():
    """Basic usage example"""
    print("🔐 Crypto Wallet Seed Checker - Basic Usage Example")
    print("=" * 50)
    
    # Setup logging
    setup_logging()
    
    # Initialize analyzer
    analyzer = SeedAnalyzer()
    
    # Example 1: Check single seed
    print("\n1. Checking single seed phrase...")
    result = await analyzer.check_single_seed(
        "abandon ability able about above absent absorb abstract absurd abuse access accident"
    )
    print(f"   Result: {'Balance found!' if result['has_balance'] else 'No balance'}")
    
    # Example 2: Generate and check multiple seeds
    print("\n2. Generating and checking 10 seeds...")
    results = await analyzer.generate_and_check(
        count=10,
        word_count=12,
        batch_size=5
    )
    
    hits = sum(1 for r in results if r.get('has_balance'))
    print(f"   Results: {len(results)} seeds, {hits} with balance")
    
    # Example 3: Print summary
    print("\n3. Final Summary:")
    analyzer.print_summary(results)

if __name__ == "__main__":
    asyncio.run(main())
