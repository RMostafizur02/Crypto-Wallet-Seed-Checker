"""
Bitcoin Blockchain Scanner and Address Generator
Educational Use Only
"""

import hashlib
import base58
import requests
import asyncio
from typing import Dict, List, Optional
from dataclasses import dataclass
from ..utils.logger import setup_logging
import logging

@dataclass
class BitcoinAddress:
    address: str
    balance: float
    transactions: int
    total_received: float
    address_type: str

class BitcoinScanner:
    """
    Bitcoin blockchain scanner for address generation and balance checking
    Supports Legacy (P2PKH), SegWit (P2SH), and Native SegWit (Bech32) addresses
    """
    
    def __init__(self, api_keys: Optional[Dict] = None):
        self.api_keys = api_keys or {}
        self.logger = logging.getLogger(__name__)
        
        # Blockchain explorer APIs
        self.api_endpoints = {
            'blockstream': 'https://blockstream.info/api',
            'blockchain_com': 'https://blockchain.info',
            'blockcypher': 'https://api.blockcypher.com/v1/btc/main',
            'mempool_space': 'https://mempool.space/api'
        }
        
        # Address version bytes (mainnet)
        self.version_bytes = {
            'legacy': 0x00,      # P2PKH
            'p2sh': 0x05,        # P2SH
            'bech32': 'bc'       # Native SegWit
        }
    
    def derive_address_from_public_key(self, public_key: bytes, address_type: str = "legacy") -> str:
        """
        Derive Bitcoin address from public key
        
        Args:
            public_key: Compressed or uncompressed public key bytes
            address_type: "legacy", "p2sh", or "bech32"
            
        Returns:
            Bitcoin address string
        """
        if address_type == "legacy":
            return self._derive_legacy_address(public_key)
        elif address_type == "p2sh":
            return self._derive_p2sh_address(public_key)
        elif address_type == "bech32":
            return self._derive_bech32_address(public_key)
        else:
            raise ValueError(f"Unsupported address type: {address_type}")
    
    def _derive_legacy_address(self, public_key: bytes) -> str:
        """
        Derive legacy P2PKH address (starts with 1)
        """
        # Ensure compressed public key format (33 bytes starting with 0x02 or 0x03)
        if len(public_key) == 65:  # Uncompressed
            # Compress the public key
            x = public_key[1:33]
            y = public_key[33:]
            prefix = b'\x02' if y[-1] % 2 == 0 else b'\x03'
            public_key = prefix + x
        
        # SHA-256 hash
        sha256_hash = hashlib.sha256(public_key).digest()
        
        # RIPEMD-160 hash
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(sha256_hash)
        ripemd160_hash = ripemd160.digest()
        
        # Add version byte (0x00 for mainnet)
        versioned_payload = b'\x00' + ripemd160_hash
        
        # Double SHA-256 for checksum
        checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[:4]
        
        # Base58 encode
        return base58.b58encode(versioned_payload + checksum).decode('utf-8')
    
    def _derive_p2sh_address(self, public_key: bytes) -> str:
        """
        Derive P2SH address (starts with 3) - SegWit compatible
        """
        # For P2SH-wrapped SegWit, we use P2WPKH nested in P2SH
        # First create the witness program
        witness_program = self._create_witness_program(public_key)
        
        # Create P2SH script: OP_HASH160 <scriptHash> OP_EQUAL
        script_hash = hashlib.new('ripemd160', hashlib.sha256(witness_program).digest()).digest()
        
        # Add version byte (0x05 for P2SH mainnet)
        versioned_payload = b'\x05' + script_hash
        
        # Double SHA-256 for checksum
        checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[:4]
        
        # Base58 encode
        return base58.b58encode(versioned_payload + checksum).decode('utf-8')
    
    def _derive_bech32_address(self, public_key: bytes) -> str:
        """
        Derive native SegWit Bech32 address (starts with bc1)
        Simplified implementation - in production use bech32 library
        """
        # This is a simplified version. In production, use proper bech32 encoding
        witness_program = self._create_witness_program(public_key)
        
        # For demonstration, return a placeholder
        # In real implementation, use: bech32.encode('bc', 0, witness_program)
        return "bc1q" + base58.b58encode(witness_program)[:39].decode('utf-8')
    
    def _create_witness_program(self, public_key: bytes) -> bytes:
        """
        Create witness program for SegWit addresses
        """
        # Ensure compressed public key
        if len(public_key) == 65:
            x = public_key[1:33]
            y = public_key[33:]
            prefix = b'\x02' if y[-1] % 2 == 0 else b'\x03'
            public_key = prefix + x
        
        # SHA-256 of public key
        sha256_hash = hashlib.sha256(public_key).digest()
        
        # RIPEMD-160 of SHA-256
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(sha256_hash)
        ripemd160_hash = ripemd160.digest()
        
        # Witness program: version byte (0x00) + RIPEMD-160 hash
        return b'\x00\x14' + ripemd160_hash  # 0x00 = witness version, 0x14 = 20 bytes
    
    def derive_address_from_private_key(self, private_key: bytes, address_type: str = "legacy") -> str:
        """
        Derive Bitcoin address from private key
        In production, this would use proper elliptic curve cryptography
        """
        # This is a simplified demonstration
        # In production, you would:
        # 1. Generate public key from private key using secp256k1
        # 2. Use the public key to derive addresses
        
        # For demo purposes, create a deterministic address from private key hash
        private_key_hash = hashlib.sha256(private_key).digest()
        ripemd160_hash = hashlib.new('ripemd160', private_key_hash).digest()
        
        if address_type == "legacy":
            versioned = b'\x00' + ripemd160_hash
        elif address_type == "p2sh":
            versioned = b'\x05' + ripemd160_hash
        else:
            versioned = b'\x00' + ripemd160_hash  # Default to legacy
        
        checksum = hashlib.sha256(hashlib.sha256(versioned).digest()).digest()[:4]
        return base58.b58encode(versioned + checksum).decode('utf-8')
    
    async def check_balance(self, address: str) -> Dict:
        """
        Check Bitcoin balance and transaction history
        
        Args:
            address: Bitcoin address to check
            
        Returns:
            Dictionary with balance information
        """
        self.logger.info(f"Checking Bitcoin balance for address: {address}")
        
        # Try different APIs until one works
        apis = [
            self._check_balance_blockstream,
            self._check_balance_blockchain_com,
            self._check_balance_blockcypher,
            self._check_balance_mempool_space
        ]
        
        for api_method in apis:
            try:
                result = await api_method(address)
                if result and not result.get('error'):
                    return result
            except Exception as e:
                self.logger.debug(f"API {api_method.__name__} failed: {e}")
                continue
        
        return {
            "address": address,
            "balance": 0,
            "balance_satoshis": 0,
            "total_received": 0,
            "total_sent": 0,
            "transaction_count": 0,
            "unit": "BTC",
            "has_balance": False,
            "error": "All API endpoints failed",
            "address_type": self._detect_address_type(address)
        }
    
    async def _check_balance_blockstream(self, address: str) -> Dict:
        """Check balance using Blockstream API"""
        try:
            url = f"{self.api_endpoints['blockstream']}/address/{address}"
            async with requests.Session() as session:
                response = await session.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    
                    chain_stats = data.get('chain_stats', {})
                    mempool_stats = data.get('mempool_stats', {})
                    
                    funded = chain_stats.get('funded_txo_sum', 0)
                    spent = chain_stats.get('spent_txo_sum', 0)
                    balance_satoshis = funded - spent
                    
                    # Add mempool transactions
                    mempool_funded = mempool_stats.get('funded_txo_sum', 0)
                    mempool_spent = mempool_stats.get('spent_txo_sum', 0)
                    mempool_balance = mempool_funded - mempool_spent
                    
                    total_balance_satoshis = balance_satoshis + mempool_balance
                    balance_btc = total_balance_satoshis / 100000000
                    
                    return {
                        "address": address,
                        "balance": balance_btc,
                        "balance_satoshis": total_balance_satoshis,
                        "total_received": funded / 100000000,
                        "total_sent": spent / 100000000,
                        "transaction_count": chain_stats.get('tx_count', 0),
                        "unit": "BTC",
                        "has_balance": total_balance_satoshis > 0,
                        "source": "blockstream",
                        "address_type": self._detect_address_type(address)
                    }
        except Exception as e:
            self.logger.warning(f"Blockstream API error: {e}")
            return {"error": f"Blockstream API error: {e}"}
    
    async def _check_balance_blockchain_com(self, address: str) -> Dict:
        """Check balance using Blockchain.com API"""
        try:
            url = f"{self.api_endpoints['blockchain_com']}/rawaddr/{address}"
            async with requests.Session() as session:
                response = await session.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    
                    balance_satoshis = data.get('final_balance', 0)
                    balance_btc = balance_satoshis / 100000000
                    total_received = data.get('total_received', 0) / 100000000
                    total_sent = data.get('total_sent', 0) / 100000000
                    
                    return {
                        "address": address,
                        "balance": balance_btc,
                        "balance_satoshis": balance_satoshis,
                        "total_received": total_received,
                        "total_sent": total_sent,
                        "transaction_count": data.get('n_tx', 0),
                        "unit": "BTC",
                        "has_balance": balance_satoshis > 0,
                        "source": "blockchain.com",
                        "address_type": self._detect_address_type(address)
                    }
        except Exception as e:
            self.logger.warning(f"Blockchain.com API error: {e}")
            return {"error": f"Blockchain.com API error: {e}"}
    
    async def _check_balance_blockcypher(self, address: str) -> Dict:
        """Check balance using BlockCypher API"""
        try:
            url = f"{self.api_endpoints['blockcypher']}/addrs/{address}/balance"
            async with requests.Session() as session:
                response = await session.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    
                    balance_satoshis = data.get('final_balance', 0)
                    balance_btc = balance_satoshis / 100000000
                    total_received = data.get('total_received', 0) / 100000000
                    
                    return {
                        "address": address,
                        "balance": balance_btc,
                        "balance_satoshis": balance_satoshis,
                        "total_received": total_received,
                        "total_sent": (total_received * 100000000 - balance_satoshis) / 100000000,
                        "transaction_count": data.get('n_tx', 0),
                        "unit": "BTC",
                        "has_balance": balance_satoshis > 0,
                        "source": "blockcypher",
                        "address_type": self._detect_address_type(address)
                    }
        except Exception as e:
            self.logger.warning(f"BlockCypher API error: {e}")
            return {"error": f"BlockCypher API error: {e}"}
    
    async def _check_balance_mempool_space(self, address: str) -> Dict:
        """Check balance using Mempool.space API"""
        try:
            url = f"{self.api_endpoints['mempool_space']}/address/{address}"
            async with requests.Session() as session:
                response = await session.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    
                    # Mempool.space returns chain statistics
                    chain_stats = data.get('chain_stats', {})
                    funded = chain_stats.get('funded_txo_sum', 0)
                    spent = chain_stats.get('spent_txo_sum', 0)
                    balance_satoshis = funded - spent
                    balance_btc = balance_satoshis / 100000000
                    
                    return {
                        "address": address,
                        "balance": balance_btc,
                        "balance_satoshis": balance_satoshis,
                        "total_received": funded / 100000000,
                        "total_sent": spent / 100000000,
                        "transaction_count": chain_stats.get('tx_count', 0),
                        "unit": "BTC",
                        "has_balance": balance_satoshis > 0,
                        "source": "mempool.space",
                        "address_type": self._detect_address_type(address)
                    }
        except Exception as e:
            self.logger.warning(f"Mempool.space API error: {e}")
            return {"error": f"Mempool.space API error: {e}"}
    
    def _detect_address_type(self, address: str) -> str:
        """
        Detect Bitcoin address type
        
        Args:
            address: Bitcoin address string
            
        Returns:
            Address type: "legacy", "p2sh", or "bech32"
        """
        if address.startswith('1'):
            return "legacy"
        elif address.startswith('3'):
            return "p2sh"
        elif address.startswith('bc1'):
            return "bech32"
        else:
            return "unknown"
    
    async def get_transaction_history(self, address: str, limit: int = 10) -> List[Dict]:
        """
        Get transaction history for a Bitcoin address
        
        Args:
            address: Bitcoin address
            limit: Number of transactions to return
            
        Returns:
            List of transaction dictionaries
        """
        try:
            url = f"{self.api_endpoints['blockstream']}/address/{address}/txs"
            async with requests.Session() as session:
                response = await session.get(url, timeout=10)
                if response.status_code == 200:
                    transactions = response.json()
                    
                    formatted_txs = []
                    for tx in transactions[:limit]:
                        # Calculate net amount for this address in the transaction
                        net_amount = 0
                        for output in tx.get('vout', []):
                            if 'scriptpubkey_address' in output and output['scriptpubkey_address'] == address:
                                net_amount += output.get('value', 0)
                        
                        for input_tx in tx.get('vin', []):
                            if 'prevout' in input_tx and 'scriptpubkey_address' in input_tx['prevout']:
                                if input_tx['prevout']['scriptpubkey_address'] == address:
                                    net_amount -= input_tx['prevout'].get('value', 0)
                        
                        formatted_txs.append({
                            'txid': tx.get('txid'),
                            'timestamp': tx.get('status', {}).get('block_time'),
                            'confirmations': tx.get('status', {}).get('confirmed', False),
                            'amount_btc': net_amount / 100000000,
                            'amount_satoshis': net_amount,
                            'block_height': tx.get('status', {}).get('block_height'),
                            'fee': tx.get('fee', 0) / 100000000 if tx.get('fee') else 0
                        })
                    
                    return formatted_txs
        except Exception as e:
            self.logger.error(f"Error fetching transaction history: {e}")
            return []
    
    async def get_utxos(self, address: str) -> List[Dict]:
        """
        Get unspent transaction outputs (UTXOs) for an address
        
        Args:
            address: Bitcoin address
            
        Returns:
            List of UTXO dictionaries
        """
        try:
            url = f"{self.api_endpoints['blockstream']}/address/{address}/utxo"
            async with requests.Session() as session:
                response = await session.get(url, timeout=10)
                if response.status_code == 200:
                    utxos = response.json()
                    
                    formatted_utxos = []
                    for utxo in utxos:
                        formatted_utxos.append({
                            'txid': utxo.get('txid'),
                            'vout': utxo.get('vout'),
                            'value': utxo.get('value', 0),
                            'value_btc': utxo.get('value', 0) / 100000000,
                            'confirmations': utxo.get('status', {}).get('confirmed', False),
                            'scriptpubkey': utxo.get('scriptpubkey', ''),
                            'address': address
                        })
                    
                    return formatted_utxos
        except Exception as e:
            self.logger.error(f"Error fetching UTXOs: {e}")
            return []
    
    def validate_address(self, address: str) -> bool:
        """
        Validate Bitcoin address format
        
        Args:
            address: Bitcoin address to validate
            
        Returns:
            True if address format is valid
        """
        try:
            # Basic format validation
            if not address or not isinstance(address, str):
                return False
            
            address_type = self._detect_address_type(address)
            
            if address_type == "unknown":
                return False
            
            # For legacy and P2SH addresses, verify base58 checksum
            if address_type in ["legacy", "p2sh"]:
                decoded = base58.b58decode(address)
                if len(decoded) != 25:  # 1 version + 20 hash + 4 checksum
                    return False
                
                version = decoded[0]
                checksum = decoded[-4:]
                payload = decoded[:-4]
                
                # Verify checksum
                computed_checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
                if checksum != computed_checksum:
                    return False
                
                # Verify version byte
                if address_type == "legacy" and version != 0x00:
                    return False
                if address_type == "p2sh" and version != 0x05:
                    return False
            
            # For bech32, basic prefix validation (simplified)
            elif address_type == "bech32":
                if not address.startswith('bc1'):
                    return False
                # In production, use proper bech32 validation
            
            return True
            
        except Exception:
            return False

# Example usage and testing
async def main():
    """Example usage of BitcoinScanner"""
    scanner = BitcoinScanner()
    
    # Test addresses (these are example addresses, not real wallets)
    test_addresses = [
        "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",  # Satoshi's genesis block address (legacy)
        "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy",  # Example P2SH address
        "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"  # Example bech32 address
    ]
    
    for address in test_addresses:
        print(f"\n🔍 Checking address: {address}")
        
        # Validate address
        is_valid = scanner.validate_address(address)
        print(f"   Valid: {is_valid}")
        
        if is_valid:
            # Check balance
            balance_info = await scanner.check_balance(address)
            print(f"   Balance: {balance_info.get('balance', 0)} BTC")
            print(f"   Transactions: {balance_info.get('transaction_count', 0)}")
            print(f"   Address Type: {balance_info.get('address_type', 'unknown')}")
            
            # Get recent transactions
            transactions = await scanner.get_transaction_history(address, limit=3)
            print(f"   Recent transactions: {len(transactions)}")
            
            # Get UTXOs
            utxos = await scanner.get_utxos(address)
            print(f"   UTXOs: {len(utxos)}")

if __name__ == "__main__":
    # Setup logging
    setup_logging()
    
    # Run example
    asyncio.run(main())
