#!/usr/bin/env python3
"""
Custom wordlist usage example
Educational Use Only
"""

import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.bip39_generator import BIP39Generator
from core.seed_analyzer import SeedAnalyzer

async def custom_wordlist_example():
    """Example using custom wordlists for targeted scanning"""
    print("🔤 Custom Wordlist Example")
    print("=" * 50)
    
    # Create a custom wordlist file
    custom_words = [
        "abandon", "ability", "able", "about", "above", "absent", "absorb", "abstract",
        "absurd", "abuse", "access", "accident", "account", "accuse", "achieve", "acid",
        # Add more words as needed for testing
        "zoo", "zone", "zero"
    ]
    
    # Write custom wordlist to file
    with open("custom_wordlist.txt", "w") as f:
        for word in custom_words:
            f.write(word + "\n")
    
    print("📝 Created custom wordlist with", len(custom_words), "words")
    
    # Initialize generator with custom wordlist
    generator = BIP39Generator("custom_wordlist.txt")
    
    # Generate seeds using custom wordlist
    print("\n🎲 Generating seeds with custom wordlist...")
    for i in range(5):
        mnemonic = generator.generate_mnemonic(12)
        print(f"   Seed {i+1}: {' '.join(mnemonic[:4])}...")
    
    # Initialize analyzer (will use default wordlist)
    analyzer = SeedAnalyzer()
    
    # Example: Check if specific patterns exist
    print("\n🔍 Checking for specific word patterns...")
    test_seeds = [
        "abandon " * 11 + "about",  # All "abandon" except last word
        "zoo " * 11 + "zone",       # All "zoo" except last word  
    ]
    
    for seed in test_seeds:
        print(f"   Testing: {seed[:40]}...")
        result = await analyzer.check_single_seed(seed)
        print(f"     Balance: {'Yes' if result['has_balance'] else 'No'}")
    
    # Clean up
    if os.path.exists("custom_wordlist.txt"):
        os.remove("custom_wordlist.txt")
        print("\n🧹 Cleaned up custom wordlist file")

def wordlist_analysis():
    """Analyze wordlist characteristics"""
    print("\n📊 Wordlist Analysis")
    print("=" * 30)
    
    generator = BIP39Generator()
    
    # Basic statistics
    wordlist = generator.wordlist
    print(f"Total words: {len(wordlist)}")
    print(f"First 10 words: {', '.join(wordlist[:10])}")
    print(f"Last 10 words: {', '.join(wordlist[-10:])}")
    
    # Word length analysis
    word_lengths = [len(word) for word in wordlist]
    avg_length = sum(word_lengths) / len(word_lengths)
    print(f"Average word length: {avg_length:.2f} characters")
    print(f"Shortest word: {min(word_lengths)} chars")
    print(f"Longest word: {max(word_lengths)} chars")

if __name__ == "__main__":
    asyncio.run(custom_wordlist_example())
    wordlist_analysis()
