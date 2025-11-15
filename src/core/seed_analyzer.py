"""
Main Seed Analysis Engine
"""

import asyncio
import time
from typing import List, Dict, Optional
from .bip39_generator import BIP39Generator
from .hd_wallet import HDWallet
from blockchain.scanners import BlockchainScanner
from utils.logger import Logger
from utils.exporter import ResultExporter

class SeedAnalyzer:
    def __init__(self, config_path: Optional[str] = None):
        self.generator = BIP39Generator()
        self.scanner = BlockchainScanner()
        self.logger = Logger()
        self.exporter = ResultExporter()
        self.results = []
    
    async def check_single_seed(self, mnemonic: str, passphrase: str = "") -> Dict:
        """Check a single seed phrase across all blockchains"""
        print(f"🔍 Analyzing seed: {mnemonic[:50]}...")
        
        try:
            # Validate mnemonic
            mnemonic_words = mnemonic.strip().split()
            if not self.generator.validate_mnemonic(mnemonic_words):
                return {"error": "Invalid BIP-39 mnemonic", "mnemonic": mnemonic}
            
            # Generate seed
            seed = self.generator.mnemonic_to_seed(mnemonic_words, passphrase)
            
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
                "mnemonic": mnemonic,
                "passphrase": passphrase,
                "addresses": addresses,
                "scan_results": scan_results,
                "has_balance": any(r.get("balance", 0) > 0 for r in scan_results.values()),
                "timestamp": time.time()
            }
            
            if result["has_balance"]:
                self.logger.log_hit(result)
                print("💰 Balance found!")
            
            self.results.append(result)
            return result
            
        except Exception as e:
            error_result = {
                "mnemonic": mnemonic,
                "error": str(e),
                "has_balance": False,
                "timestamp": time.time()
            }
            self.results.append(error_result)
            return error_result
    
    async def generate_and_check(self, count: int, word_count: int = 12, 
                               passphrase: str = "", batch_size: int = 10) -> List[Dict]:
        """Generate and check multiple seed phrases"""
        print(f"🎯 Generating {count} {word_count}-word seeds...")
        
        tasks = []
        for i in range(count):
            mnemonic_words = self.generator.generate_mnemonic(word_count)
            mnemonic = " ".join(mnemonic_words)
            task = self.check_single_seed(mnemonic, passphrase)
            tasks.append(task)
            
            # Process in batches
            if len(tasks) >= batch_size:
                await asyncio.gather(*tasks)
                tasks = []
                print(f"   Progress: {i+1}/{count}")
        
        # Process remaining tasks
        if tasks:
            await asyncio.gather(*tasks)
        
        return self.results
    
    async def check_from_file(self, filename: str, passphrase: str = "", batch_size: int = 10) -> List[Dict]:
        """Check seed phrases from a file"""
        print(f"📁 Reading seeds from {filename}...")
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                seeds = [line.strip() for line in f if line.strip()]
            
            tasks = []
            for i, seed in enumerate(seeds):
                task = self.check_single_seed(seed, passphrase)
                tasks.append(task)
                
                if len(tasks) >= batch_size:
                    await asyncio.gather(*tasks)
                    tasks = []
                    print(f"   Progress: {i+1}/{len(seeds)}")
            
            if tasks:
                await asyncio.gather(*tasks)
            
            return self.results
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Seed file not found: {filename}")
