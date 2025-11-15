"""
EVM-compatible blockchain scanners (BSC, Polygon, etc.)
"""

import requests
from typing import Dict, List

class EVMChainScanner:
    def __init__(self, chain_name: str, api_key: str = None):
        self.chain_name = chain_name
        self.api_key = api_key
        self.api_config = self._get_api_config(chain_name)
    
    def _get_api_config(self, chain_name: str) -> Dict:
        """Get API configuration for different EVM chains"""
        configs = {
            "bsc": {
                "api_url": "https://api.bscscan.com/api",
                "symbol": "BNB",
                "decimals": 18
            },
            "polygon": {
                "api_url": "https://api.polygonscan.com/api", 
                "symbol": "MATIC",
                "decimals": 18
            },
            "avalanche": {
                "api_url": "https://api.snowtrace.io/api",
                "symbol": "AVAX", 
                "decimals": 18
            },
            "arbitrum": {
                "api_url": "https://api.arbiscan.io/api",
                "symbol": "ETH",
                "decimals": 18
            },
            "optimism": {
                "api_url": "https://api-optimistic.etherscan.io/api",
                "symbol": "ETH", 
                "decimals": 18
            }
        }
        return configs.get(chain_name, {})
    
    async def check_balance(self, address: str) -> Dict:
        """Check balance on EVM chain"""
        if not self.api_config:
            return {"error": f"Unsupported chain: {self.chain_name}"}
        
        try:
            url = f"{self.api_config['api_url']}?module=account&action=balance&address={address}&tag=latest"
            if self.api_key:
                url += f"&apikey={self.api_key}"
            
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data.get("status") == "1":
                balance_wei = int(data["result"])
                balance = balance_wei / (10 ** self.api_config["decimals"])
                
                return {
                    "address": address,
                    "balance": balance,
                    "unit": self.api_config["symbol"],
                    "has_balance": balance > 0
                }
            else:
                return {
                    "address": address,
                    "error": data.get("message", "API error"),
                    "has_balance": False
                }
                
        except Exception as e:
            return {
                "address": address,
                "error": str(e),
                "has_balance": False
            }
