"""
Blockchain Scanner - Simplified Version
"""

import asyncio
from typing import Dict

class BlockchainScanner:
    def __init__(self):
        pass
    
    async def scan_addresses(self, addresses: Dict) -> Dict:
        """Simple scanner that always returns no balance for demo"""
        results = {}
        for chain in addresses:
            results[chain] = {
                "address": f"{chain}_demo_address",
                "balance": 0.0,
                "unit": "ETH" if chain == "ethereum" else "BTC",
                "has_balance": False,
                "note": "Demo mode - No actual scanning"
            }
        return results
