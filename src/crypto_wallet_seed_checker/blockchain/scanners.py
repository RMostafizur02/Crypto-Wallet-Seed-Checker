"""
Main blockchain scanner orchestrator - Simplified version
"""

import asyncio
from typing import Dict
from .bitcoin import BitcoinScanner

class BlockchainScanner:
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.scanners = {
            "bitcoin": BitcoinScanner(),
        }
    
    async def scan_addresses(self, addresses: Dict) -> Dict:
        """Scan addresses across all blockchains - Simplified"""
        results = {}
        
        for chain in addresses:
            if chain in self.scanners:
                # Create a demo address for scanning
                demo_address = f"{chain}_demo_address"
                result = await self.scanners[chain].check_balance(demo_address)
                results[chain] = result
        
        return results
    
    async def scan_single_chain(self, chain: str, address: str) -> Dict:
        """Scan a single address on a specific chain"""
        if chain not in self.scanners:
            return {"error": f"Unsupported chain: {chain}"}
        
        return await self.scanners[chain].check_balance(address)
