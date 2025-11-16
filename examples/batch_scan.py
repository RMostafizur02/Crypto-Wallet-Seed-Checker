#!/usr/bin/env python3
"""
Batch scanning example for large-scale operations
Educational Use Only
"""

import asyncio
import sys
import os
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.seed_analyzer import SeedAnalyzer
from utils.logger import setup_logging
from utils.exporter import ResultExporter

async def large_scale_scan():
    """Example of large-scale batch scanning"""
    print("🎯 Large Scale Batch Scanning Example")
    print("=" * 50)
    
    setup_logging(verbose=True)
    analyzer = SeedAnalyzer()
    exporter = ResultExporter()
    
    start_time = time.time()
    
    try:
        # Perform large-scale scan
        print("Starting large-scale scan (1000 seeds)...")
        results = await analyzer.generate_and_check(
            count=1000,
            word_count=12,
            batch_size=20,  # Conservative batch size for stability
            passphrase=""
        )
        
        # Calculate statistics
        total_seeds = len(results)
        seeds_with_balance = sum(1 for r in results if r.get('has_balance'))
        errors = sum(1 for r in results if r.get('error'))
        
        elapsed_time = time.time() - start_time
        seeds_per_second = total_seeds / elapsed_time if elapsed_time > 0 else 0
        
        # Print summary
        print(f"\n📊 SCAN COMPLETED")
        print(f"✅ Total seeds processed: {total_seeds}")
        print(f"💰 Seeds with balance: {seeds_with_balance}")
        print(f"❌ Errors: {errors}")
        print(f"⏱️  Time elapsed: {elapsed_time:.2f} seconds")
        print(f"🚀 Speed: {seeds_per_second:.2f} seeds/second")
        
        # Export results
        print(f"\n💾 Exporting results...")
        exporter.export_results(results, "results/large_scan.json", "json")
        exporter.export_results(results, "results/large_scan.csv", "csv")
        
        print("✅ Results exported to results/ directory")
        
    except KeyboardInterrupt:
        print("\n⏹️  Scan interrupted by user")
        # Export partial results
        if analyzer.results:
            exporter.export_results(analyzer.results, "results/partial_scan.json", "json")
            print("💾 Partial results saved to results/partial_scan.json")
    
    except Exception as e:
        print(f"❌ Error during scan: {e}")
        raise

async def optimized_scan():
    """Example of optimized scanning with different parameters"""
    print("\n⚡ Optimized Scanning Example")
    print("=" * 50)
    
    analyzer = SeedAnalyzer()
    
    # Test different batch sizes
    batch_sizes = [5, 10, 25, 50]
    
    for batch_size in batch_sizes:
        print(f"\nTesting batch size: {batch_size}")
        start_time = time.time()
        
        results = await analyzer.generate_and_check(
            count=100,
            word_count=12,
            batch_size=batch_size
        )
        
        elapsed = time.time() - start_time
        speed = 100 / elapsed if elapsed > 0 else 0
        
        print(f"   Time: {elapsed:.2f}s, Speed: {speed:.2f} seeds/sec")

if __name__ == "__main__":
    # Create results directory
    os.makedirs("results", exist_ok=True)
    
    # Run examples
    asyncio.run(large_scale_scan())
    # asyncio.run(optimized_scan())  # Uncomment to test different batch sizes
