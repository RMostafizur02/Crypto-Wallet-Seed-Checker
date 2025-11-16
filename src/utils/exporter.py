"""
Result export utilities
"""

import json
import csv
import os
from typing import List, Dict
from datetime import datetime

class ResultExporter:
    def __init__(self):
        self.export_formats = ['json', 'csv', 'txt']
    
    def export_results(self, results: List[Dict], filename: str, format: str = 'json'):
        """Export results to file"""
        if format not in self.export_formats:
            raise ValueError(f"Unsupported format: {format}. Use: {self.export_formats}")
        
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        if format == 'json':
            self._export_json(results, filename)
        elif format == 'csv':
            self._export_csv(results, filename)
        elif format == 'txt':
            self._export_txt(results, filename)
    
    def _export_json(self, results: List[Dict], filename: str):
        """Export results as JSON"""
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "total_results": len(results),
            "results_with_balance": len([r for r in results if r.get('has_balance')]),
            "results": results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    def _export_csv(self, results: List[Dict], filename: str):
        """Export results as CSV"""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Mnemonic', 'Has Balance', 'Total Balance', 'Timestamp'])
            
            for result in results:
                total_balance = 0.0
                scan_results = result.get('scan_results', {})
                
                for chain_data in scan_results.values():
                    if isinstance(chain_data, dict) and 'balance' in chain_data:
                        total_balance += chain_data['balance']
                
                writer.writerow([
                    result.get('mnemonic', ''),
                    result.get('has_balance', False),
                    total_balance,
                    datetime.fromtimestamp(result.get('timestamp', 0)).isoformat()
                ])
    
    def _export_txt(self, results: List[Dict], filename: str):
        """Export results as human-readable text"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Crypto Wallet Seed Checker - Results\n")
            f.write("=" * 50 + "\n")
            f.write(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Seeds Checked: {len(results)}\n")
            
            hits = [r for r in results if r.get('has_balance')]
            f.write(f"Wallets with Balance: {len(hits)}\n\n")
            
            if hits:
                f.write("WALLETS WITH BALANCES:\n")
                f.write("-" * 30 + "\n")
                
                for i, hit in enumerate(hits, 1):
                    f.write(f"\n{i}. Mnemonic: {hit['mnemonic']}\n")
                    
                    scan_results = hit.get('scan_results', {})
                    for chain, data in scan_results.items():
                        if isinstance(data, dict) and data.get('balance', 0) > 0:
                            f.write(f"   {chain.upper()}: {data['balance']} {data.get('unit', '')}\n")
                    
                    f.write(f"   Timestamp: {datetime.fromtimestamp(hit.get('timestamp', 0))}\n")
