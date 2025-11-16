"""
Tests for blockchain scanners
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from blockchain.scanners import BlockchainScanner
from blockchain.bitcoin import BitcoinScanner
from blockchain.ethereum import EthereumScanner

class TestBlockchainScanner:
    def setup_method(self):
        self.scanner = BlockchainScanner()
    
    def test_initialize_scanners(self):
        """Test scanner initialization"""
        scanners = self.scanner.scanners
        
        expected_scanners = [
            "bitcoin", "ethereum", "bsc", "polygon", 
            "avalanche", "arbitrum", "optimism"
        ]
        
        for chain in expected_scanners:
            assert chain in scanners
    
    @pytest.mark.asyncio
    async def test_scan_single_chain(self):
        """Test scanning single chain"""
        # Mock the scanner to avoid actual API calls
        with patch.object(BitcoinScanner, 'check_balance') as mock_scan:
            mock_scan.return_value = {
                "address": "test_address",
                "balance": 0.0,
                "has_balance": False
            }
            
            result = await self.scanner.scan_single_chain("bitcoin", "test_address")
            
            assert "address" in result
            assert "balance" in result
            assert "has_balance" in result
    
    def test_unsupported_chain(self):
        """Test error for unsupported chain"""
        result = self.scanner.scan_single_chain("unsupported", "test_address")
        assert "error" in result

class TestBitcoinScanner:
    def setup_method(self):
        self.scanner = BitcoinScanner()
    
    def test_derive_address(self):
        """Test Bitcoin address derivation"""
        # Test with dummy public key
        public_key = b'\x02' * 33  # Compressed public key format
        
        legacy_address = self.scanner.derive_address(public_key, "legacy")
        segwit_address = self.scanner.derive_address(public_key, "segwit")
        
        assert isinstance(legacy_address, str)
        assert isinstance(segwit_address, str)
        assert legacy_address.startswith('1') or legacy_address.startswith('3')
        assert segwit_address.startswith('bc1')
    
    def test_invalid_address_type(self):
        """Test error for invalid address type"""
        public_key = b'\x02' * 33
        
        with pytest.raises(ValueError):
            self.scanner.derive_address(public_key, "invalid")
