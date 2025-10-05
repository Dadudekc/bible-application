#!/usr/bin/env python3
"""
Test Clean Download - Command Line Version
Download Genesis Chapter 1 with clean text (no HTML tags)
"""

from clean_bible_downloader import CleanBibleDownloader
import json

def main():
    downloader = CleanBibleDownloader()
    
    print("=== Clean Bible Download Test ===")
    print()
    
    # Download Genesis Chapter 1 in Hebrew + English
    print("Downloading Genesis Chapter 1 (Hebrew + English)...")
    data = downloader.download_chapter('Genesis', 1, 'he-en')
    
    print("\n=== Clean Hebrew Text ===")
    for i, line in enumerate(data['hebrew'][:5], 1):  # Show first 5 verses
        print(f"{i}: {line}")
    
    print("\n=== Clean English Text ===")
    for i, line in enumerate(data['english'][:5], 1):  # Show first 5 verses
        print(f"{i}: {line}")
    
    print("\n=== Parallel Text (Side by Side) ===")
    for i in range(5):
        hebrew_line = data['hebrew'][i] if i < len(data['hebrew']) else ""
        english_line = data['english'][i] if i < len(data['english']) else ""
        print(f"\nVerse {i+1}:")
        print(f"Hebrew:  {hebrew_line}")
        print(f"English: {english_line}")
    
    # Save clean files
    import os
    os.makedirs('clean_test', exist_ok=True)
    
    # Save Hebrew only
    with open('clean_test/Genesis_chapter_1_hebrew_only.txt', 'w', encoding='utf-8') as f:
        f.write("Clean Hebrew Text - Genesis Chapter 1\n")
        f.write("=" * 50 + "\n\n")
        for line in data['hebrew']:
            f.write(line + "\n")
    
    # Save English only  
    with open('clean_test/Genesis_chapter_1_english_only.txt', 'w', encoding='utf-8') as f:
        f.write("Clean English Text - Genesis Chapter 1\n")
        f.write("=" * 50 + "\n\n")
        for line in data['english']:
            f.write(line + "\n")
    
    # Save parallel
    with open('clean_test/Genesis_chapter_1_parallel.txt', 'w', encoding='utf-8') as f:
        f.write("Parallel Hebrew-English - Genesis Chapter 1\n")
        f.write("=" * 50 + "\n\n")
        
        max_lines = max(len(data['hebrew']), len(data['english']))
        
        for i in range(max_lines):
            hebrew_line = data['hebrew'][i] if i < len(data['hebrew']) else ""
            english_line = data['english'][i] if i < len(data['english']) else ""
            
            f.write(f"\n--- Verse {i+1} ---\n")
            f.write(f"Hebrew:  {hebrew_line}\n")
            f.write(f"English: {english_line}\n")
    
    print(f"\nFiles saved to 'clean_test/' directory:")
    print("- Genesis_chapter_1_hebrew_only.txt")
    print("- Genesis_chapter_1_english_only.txt") 
    print("- Genesis_chapter_1_parallel.txt")
    
    print("\nOriginal first verse Hebrew:")
    print("בְּרֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים אֵ֥ת הַ־ָּמַ֖יִם וְאֵ֥ת הָאָֽרֶץ")
    print("\nClean first verse Hebrew (no tags):")
    print(data['hebrew'][0])

if __name__ == "__main__":
    main()
