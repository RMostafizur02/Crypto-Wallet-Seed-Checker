#!/usr/bin/env python3
"""
Crypto Wallet Seed Checker - Main Entry Point
Educational Use Only
"""

import asyncio
import sys
import os

# Add src to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

try:
    from crypto_wallet_seed_checker.core.seed_analyzer import SeedAnalyzer
    from crypto_wallet_seed_checker.utils.validator import validate_mnemonic_format
    print("✅ All imports successful!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please make sure all required dependencies are installed:")
    print("pip install -r requirements.txt")
    sys.exit(1)

import argparse
import logging
import time
import signal

def setup_logging(verbose: bool = False):
    """Setup comprehensive logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('seed_checker_runtime.log')
        ]
    )

def print_banner():
    """Print enhanced application banner"""
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

def validate_arguments(args):
    """Validate command line arguments"""
    if args.generate and args.generate <= 0:
        raise ValueError("Number of seeds to generate must be positive")
    
    if args.batch_size <= 0:
        raise ValueError("Batch size must be positive")
    
    if args.batch_size > 50:
        print("⚠️  Warning: Large batch sizes may cause API rate limiting")
    
    if args.file and not os.path.exists(args.file):
        raise FileNotFoundError(f"Seed file not found: {args.file}")
    
    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)

def print_configuration(args):
    """Print current configuration"""
    print("\n🔧 Configuration:")
    print(f"   Mode: {get_mode_description(args)}")
    print(f"   Word Count: {args.words}")
    print(f"   Passphrase: {'*' * len(args.passphrase) if args.passphrase else 'None'}")
    print(f"   Batch Size: {args.batch_size}")
    print(f"   Output Directory: {args.output_dir or 'Default'}")
    print(f"   Verbose: {args.verbose}")
    print()

def get_mode_description(args):
    """Get human-readable mode description"""
    if args.seed:
        return "Single Seed Check"
    elif args.file:
        return f"File Check ({args.file})"
    elif args.generate:
        return f"Generate & Check ({args.generate} seeds)"
    return "Unknown"

async def main():
    """Enhanced main application entry point"""
    setup_logging()
    print_banner()
    
    parser = argparse.ArgumentParser(
        description='Crypto Wallet Seed Checker - Educational Blockchain Analysis Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
📖 EXAMPLES:
  Single seed check:
    python main.py --seed "abandon ability able about above absent absorb abstract absurd abuse access accident"

  Generate and check random seeds:
    python main.py --generate 100 --words 12 --batch-size 5

  Check seeds from file:
    python main.py --file seeds.txt --passphrase "mypass" --output-dir ./results

⚡ PERFORMANCE TIPS:
  - Use batch-size 5-10 for optimal performance
  - 12-word seeds are fastest to process
  --verbose flag shows detailed debugging info

🔒 SECURITY REMINDER:
  This tool is for EDUCATIONAL USE ONLY. Never use with wallets you don't own.
        """
    )
    
    # Operation modes (mutually exclusive)
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('--generate', type=int, metavar='N', 
                          help='Generate and check N random seed phrases')
    mode_group.add_argument('--file', type=str, metavar='FILEPATH',
                          help='Check seed phrases from text file (one per line)')
    mode_group.add_argument('--seed', type=str, metavar='SEED_PHRASE',
                          help='Check a single seed phrase')
    
    # Configuration options
    parser.add_argument('--words', type=int, choices=[12, 15, 18, 21, 24], 
                       default=12, help='Number of words in mnemonic (default: 12)')
    parser.add_argument('--passphrase', type=str, default='', 
                       help='BIP-39 passphrase for seed generation/checking')
    parser.add_argument('--batch-size', type=int, default=5, 
                       help='Batch size for concurrent checking (default: 5)')
    parser.add_argument('--output-dir', type=str, 
                       help='Custom directory for results and logs')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output and debugging')
    
    args = parser.parse_args()
    
    try:
        # Validate arguments
        validate_arguments(args)
        
        # Print configuration
        print_configuration(args)
        
        # Initialize checker
        checker = SeedAnalyzer()
        
        # Set output directory if specified
        if args.output_dir:
            checker.logger.log_file = os.path.join(args.output_dir, 'seed_checker.log')
        
        # Confirm large operations
        if args.generate and args.generate > 1000:
            confirm = input(f"⚠️  About to generate and check {args.generate} seeds. Continue? (y/N): ")
            if confirm.lower() not in ['y', 'yes']:
                print("Operation cancelled.")
                return
        
        # Execute based on mode
        results = []
        
        if args.seed:
            print("🔍 Checking single seed phrase...")
            mnemonic = validate_mnemonic_format(args.seed)
            result = await checker.check_single_seed(mnemonic, args.passphrase)
            results.append(result)
            
        elif args.file:
            print(f"📁 Checking seeds from file: {args.file}")
            results = await checker.check_from_file(args.file, args.passphrase)
            
        elif args.generate:
            print(f"🎯 Generating and checking {args.generate} seed phrases...")
            results = await checker.generate_and_check_batch(
                args.generate, args.words, args.passphrase, args.batch_size
            )
        
        # Print final summary
        checker.print_summary(results)
        
        # Print completion message
        print(f"\n✅ Operation completed successfully!")
        
    except KeyboardInterrupt:
        print(f"\n⏹️  Operation cancelled by user")
        sys.exit(130)
    except FileNotFoundError as e:
        print(f"❌ File error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"❌ Invalid argument: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

def signal_handler(signum, frame):
    """Handle interrupt signals gracefully"""
    print(f"\n⏹️  Received interrupt signal. Shutting down gracefully...")
    sys.exit(130)

if __name__ == "__main__":
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        sys.exit(1)
    
    # Run the application
    try:
        start_time = time.time()
        asyncio.run(main())
        elapsed = time.time() - start_time
        print(f"⏱️  Total execution time: {elapsed:.2f} seconds")
    except KeyboardInterrupt:
        print("\n👋 Operation cancelled. Goodbye!")
        sys.exit(130)
    except RuntimeError as e:
        if "Event loop is closed" not in str(e):
            print(f"❌ Runtime error: {e}")
            sys.exit(1)
