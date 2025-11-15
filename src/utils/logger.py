"""
Logging and result tracking utilities
"""

import logging
import time
import json
from typing import Dict
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class Logger:
    def __init__(self, log_file: str = "seed_checker.log"):
        self.log_file = log_file
        self.hits = []
    
    def log_hit(self, result: Dict):
        """Log a wallet with balance found"""
        hit_data = {
            "timestamp": time.time(),
            "mnemonic": result["mnemonic"],
            "passphrase": result.get("passphrase", ""),
            "scan_results": result.get("scan_results", {}),
            "total_balance": self._calculate_total_balance(result)
        }
        
        self.hits.append(hit_data)
        
        # Print to console
        print(f"\n{Fore.GREEN}💰 HIT FOUND!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Mnemonic:{Style.RESET_ALL} {result['mnemonic'][:50]}...")
        print(f"{Fore.CYAN}Total Balance:{Style.RESET_ALL} {hit_data['total_balance']}")
        
        # Write to log file
        self._write_to_log(hit_data)
    
    def _calculate_total_balance(self, result: Dict) -> float:
        """Calculate total balance across all chains"""
        total = 0.0
        scan_results = result.get("scan_results", {})
        
        for chain_data in scan_results.values():
            if isinstance(chain_data, dict) and "balance" in chain_data:
                total += chain_data["balance"]
        
        return total
    
    def _write_to_log(self, hit_data: Dict):
        """Write hit to log file"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(hit_data, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"{Fore.RED}Error writing to log: {e}{Style.RESET_ALL}")
    
    def get_summary(self) -> Dict:
        """Get summary of scanning session"""
        return {
            "total_hits": len(self.hits),
            "hits": self.hits,
            "log_file": self.log_file
        }

def setup_logging(verbose: bool = False):
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('seed_checker_runtime.log')
        ]
    )
