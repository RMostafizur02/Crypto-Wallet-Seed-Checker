"""
Main Seed Analysis Engine
"""

import asyncio
import time
from typing import List, Dict, Optional

# Fix imports - use absolute imports
try:
    from crypto_wallet_seed_checker.core.bip39_generator import BIP39Generator
    from crypto_wallet_seed_checker.core.hd_wallet import HDWallet
    from crypto_wallet_seed_checker.blockchain.scanners import BlockchainScanner
    from crypto_wallet_seed_checker.utils.logger import Logger
    from crypto_wallet_seed_checker.utils.validator import validate_mnemonic_format
except ImportError:
    # Fallback for direct execution
    from .bip39_generator import BIP39Generator
    from .hd_wallet import HDWallet
    from ..blockchain.scanners import BlockchainScanner
    from ..utils.logger import Logger
    from ..utils.validator import validate_mnemonic_format

import logging
import os

class SeedAnalyzer:
    def __init__(self, config_path: Optional[str] = None):
        self.generator = BIP39Generator()
        self.scanner = BlockchainScanner()
        self.logger = Logger()
        self.results = []
    
    async def check_single_seed(self, mnemonic: List[str], passphrase: str = "") -> Dict:
        """Check a single seed phrase across all blockchains"""
        print(f"🔍 Analyzing seed: {' '.join(mnemonic[:4])}...")
        
        try:
            # Validate mnemonic
            if not self.generator.validate_mnemonic(mnemonic):
                return {"error": "Invalid BIP-39 mnemonic", "mnemonic": ' '.join(mnemonic)}
            
            # Generate seed
            seed = self.generator.mnemonic_to_seed(mnemonic, passphrase)
            
            # Create HD wallet
            wallet = HDWallet(seed)
            
            # Derive addresses for all blockchains
            addresses = {}
            derivation_paths = wallet.get_derivation_paths()
            
            for chain, path_obj in derivation_paths.items():
                path = path_obj.to_string()
                private_key, chain_code = wallet.derive_path(path)
                # In real implementation, convert to actual addresses
                addresses[chain] = {
                    "path": path,
                    "private_key": private_key.hex(),
                    "chain_code": chain_code.hex()
                }
            
            # Scan addresses for balances
            scan_results = await self.scanner.scan_addresses(addresses)
            
            result = {
                "mnemonic": ' '.join(mnemonic),
                "passphrase": passphrase,
                "addresses": addresses,
                "scan_results": scan_results,
                "has_balance": any(r.get("balance", 0) > 0 for r in scan_results.values() if isinstance(r, dict)),
                "timestamp": time.time()
            }
            
            if result["has_balance"]:
                self.logger.log_hit(result)
                print("💰 Balance found!")
            
            self.results.append(result)
            return result
            
        except Exception as e:
            error_result = {
                "mnemonic": ' '.join(mnemonic),
                "error": str(e),
                "has_balance": False,
                "timestamp": time.time()
            }
            self.results.append(error_result)
            return error_result
    
    async def generate_and_check_batch(self, count: int, word_count: int = 12, 
                                     passphrase: str = "", batch_size: int = 10) -> List[Dict]:
        """Generate and check multiple seed phrases"""
        print(f"🎯 Generating {count} {word_count}-word seeds...")
        
        all_results = []
        
        for i in range(count):
            try:
                mnemonic = self.generator.generate_mnemonic(word_count)
                result = await self.check_single_seed(mnemonic, passphrase)
                all_results.append(result)
                
                if (i + 1) % 10 == 0:
                    print(f"   Progress: {i + 1}/{count}")
                    
            except Exception as e:
                print(f"   Error generating seed {i+1}: {e}")
                all_results.append({
                    "error": f"Generation error: {e}",
                    "has_balance": False
                })
        
        return all_results
    
    async def check_from_file(self, filename: str, passphrase: str = "", batch_size: int = 10) -> List[Dict]:
        """Check seed phrases from a file"""
        print(f"📁 Reading seeds from {filename}...")
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                seeds = [line.strip() for line in f if line.strip()]
            
            results = []
            for i, seed_line in enumerate(seeds):
                try:
                    mnemonic = validate_mnemonic_format(seed_line)
                    result = await self.check_single_seed(mnemonic, passphrase)
                    results.append(result)
                    
                    if (i + 1) % 10 == 0:
                        print(f"   Progress: {i + 1}/{len(seeds)}")
                        
                except Exception as e:
                    results.append({
                        "raw_input": seed_line,
                        "error": str(e),
                        "has_balance": False
                    })
            
            return results
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Seed file not found: {filename}")
    
    def print_summary(self, results: List[Dict]):
        """Print comprehensive summary of results"""
        total_processed = len(results)
        hits = sum(1 for r in results if r.get('has_balance'))
        errors = sum(1 for r in results if r.get('error') and not r.get('has_balance'))
        
        print(f"\n{'='*60}")
        print(f"📊 COMPREHENSIVE SUMMARY")
        print(f"{'='*60}")
        print(f"✅ Total seeds processed: {total_processed}")
        print(f"💰 Wallets with balance: {hits}")
        print(f"❌ Errors encountered: {errors}")
        
        if hits > 0:
            print(f"\n🔍 Check detailed results in: {self.logger.log_file}")
            print(f"💡 Found {hits} wallet(s) with balances!")
        
        if errors > 0:
            print(f"⚠️  {errors} seeds had errors during processing")
        
        print(f"{'='*60}")

# For direct execution
async def demo():
    """Demo function for direct execution"""
    checker = SeedAnalyzer()
    mnemonic = ["abandon"] * 11 + ["about"]
    result = await checker.check_single_seed(mnemonic)
    checker.print_summary([result])

if __name__ == "__main__":
    asyncio.run(demo())
