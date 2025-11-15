"""
Main blockchain scanner orchestrator
"""

import asyncio
from typing import Dict, List
from .bitcoin import BitcoinScanner
from .ethereum import EthereumScanner
from .evm_chains import EVMChainScanner

class BlockchainScanner:
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.scanners = self._initialize_scanners()
    
    def _initialize_scanners(self) -> Dict:
        """Initialize scanners for all supported blockchains"""
        return {
            "bitcoin": BitcoinScanner(),
            "ethereum": EthereumScanner(self.config.get("etherscan_key")),
            "bsc": EVMChainScanner("bsc", self.config.get("bscscan_key")),
            "polygon": EVMChainScanner("polygon", self.config.get("polygonscan_key")),
            "avalanche": EVMChainScanner("avalanche", self.config.get("snowtrace_key")),
            "arbitrum": EVMChainScanner("arbitrum", self.config.get("arbiscan_key")),
            "optimism": EVMChainScanner("optimism", self.config.get("optimism_key")),
        }
    
    async def scan_addresses(self, addresses: Dict) -> Dict:
        """Scan addresses across all blockchains"""
        tasks = []
        address_map = {}
        
        # Create scanning tasks
        for chain, address_data in addresses.items():
            if chain in self.scanners:
                scanner = self.scanners[chain]
                # In real implementation, derive actual address from keys
                demo_address = f"{chain}_address_placeholder"
                task = scanner.check_balance(demo_address)
                tasks.append(task)
                address_map[task] = chain
        
        # Execute all scans concurrently
        results = {}
        if tasks:
            scan_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for task, result in zip(tasks, scan_results):
                chain = address_map[task]
                if isinstance(result, Exception):
                    results[chain] = {"error": str(result)}
                else:
                    results[chain] = result
        
        return results
    
    async def scan_single_chain(self, chain: str, address: str) -> Dict:
        """Scan a single address on a specific chain"""
        if chain not in self.scanners:
            return {"error": f"Unsupported chain: {chain}"}
        
        return await self.scanners[chain].check_balance(address)
