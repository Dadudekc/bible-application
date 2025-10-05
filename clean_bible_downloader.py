#!/usr/bin/env python3
"""
Clean Bible Downloader with GUI

A GUI application to download Bible texts from Sefaria.org without HTML tags,
with options to select different versions and translations.
"""

import requests
import json
import re
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from pathlib import Path
from typing import Dict, List, Optional
import threading
import time

class CleanBibleDownloader:
    """Clean Bible text downloader with HTML tag removal"""
    
    def __init__(self):
        self.base_url = "https://www.sefaria.org/api"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Clean-Bible-Downloader/1.0'
        })
        
        # Common Bible books
        self.bible_books = {
            'genesis': 'Genesis', 'exodus': 'Exodus', 'leviticus': 'Leviticus', 
            'numbers': 'Numbers', 'deuteronomy': 'Deuteronomy', 'joshua': 'Joshua',
            'judges': 'Judges', 'samuel1': 'I Samuel', 'samuel2': 'II Samuel',
            'kings1': 'I Kings', 'kings2': 'II Kings', 'isaiah': 'Isaiah',
            'jeremiah': 'Jeremiah', 'ezekiel': 'Ezekiel', 'hosea': 'Hosea',
            'joel': 'Joel', 'amos': 'Amos', 'obadiah': 'Obadiah', 'jonah': 'Jonah',
            'micah': 'Micah', 'nahum': 'Nahum', 'habakkuk': 'Habakkuk',
            'zephaniah': 'Zephaniah', 'haggai': 'Haggai', 'zechariah': 'Zechariah',
            'malachi': 'Malachi', 'psalms': 'Psalms', 'proverbs': 'Proverbs',
            'job': 'Job', 'song_of_songs': 'Song of Songs', 'ruth': 'Ruth',
            'lamentations': 'Lamentations', 'ecclesiastes': 'Ecclesiastes',
            'esther': 'Esther', 'daniel': 'Daniel', 'ezra': 'Ezra',
            'nehemiah': 'Nehemiah', 'chronicles1': 'I Chronicles', 'chronicles2': 'II Chronicles'
        }
        
        # Available versions/translations on Sefaria
        self.versions = {
            'he': 'Hebrew (Original)',
            'en': 'English Translation',
            'he-en': 'Hebrew + English (Side by side)'
        }
    
    def clean_hebrew_text(self, text: str) -> str:
        """Remove HTML tags and clean Hebrew text"""
        # Remove HTML tags but preserve Hebrew letters
        clean = re.sub(r'<[^>]*>', '', text)
        
        # Remove extra whitespace and normalize
        clean = ' '.join(clean.split())
        
        return clean.strip()
    
    def clean_english_text(self, text: str) -> str:
        """Clean English text by removing HTML tags"""
        # Remove HTML tags
        clean = re.sub(r'<[^>]*>', '', text)
        
        # Remove extra whitespace
        clean = ' '.join(clean.split())
        
        return clean.strip()
    
    def get_chapter_count(self, book_name: str) -> int:
        """Get the number of chapters in a book"""
        try:
            response = self.session.get(f"{self.base_url}/\texts/{book_name}")
            response.raise_for_status()
            data = response.json()
            
            if 'text' in data:
                return len(data['text'])
            return 0
        except Exception as e:
            print(f"Error getting chapter count: {e}")
            return 0
    
    def download_chapter(self, book_name: str, chapter: int, version: str = 'he') -> Dict:
        """Download a specific chapter"""
        try:
            ref = f"{book_name}.{chapter}"
            url = f"{self.base_url}/texts/{ref}"
            
            params = {}
            if version == 'he-en':
                params = {'version': 'he'}
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Clean the text based on version
            if version == 'he':
                # Clean Hebrew text
                hebrew_lines = []
                if 'he' in data:
                    for line in data['he']:
                        hebrew_lines.append(self.clean_hebrew_text(line))
                return {'hebrew': hebrew_lines, 'english': []}
            
            elif version == 'en':
                # Clean English text
                english_lines = []
                if 'text' in data:
                    for line in data['text']:
                        english_lines.append(self.clean_english_text(line))
                return {'hebrew': [], 'english': english_lines}
            
            else:  # he-en (both)
                hebrew_lines = []
                english_lines = []
                
                if 'he' in data:
                    for line in data['he']:
                        hebrew_lines.append(self.clean_hebrew_text(line))
                
                if 'text' in data:
                    for line in data['text']:
                        english_lines.append(self.clean_english_text(line))
                
                return {'hebrew': hebrew_lines, 'english': english_lines}
                
        except Exception as e:
            print(f"Error downloading chapter: {e}")
            return {'hebrew': [], 'english': [], 'error': str(e)}
    
    def download_book(self, book_name: str, version: str = 'he') -> Dict:
        """Download an entire book"""
        chapter_count = self.get_chapter_count(book_name)
        if chapter_count == 0:
            return {'error': f'Could not determine chapter count for {book_name}'}
        
        print(f"Downloading {book_name} ({chapter_count} chapters)")
        
        all_text = {'hebrew': [], 'english': []}
        
        for chapter in range(1, chapter_count + 1):
            print(f"Downloading Chapter {chapter}...")
            
            chapter_data = self.download_chapter(book_name, chapter, version)
            
            if 'error' not in chapter_data:
                all_text['hebrew'].extend(chapter_data['hebrew'])
                all_text['english'].extend(chapter_data['english'])
            else:
                print(f"Error in Chapter {chapter}: {chapter_data['error']}")
            
            # Rate limiting
            time.sleep(0.5)
        
        return all_text

class BibleDownloaderGUI:
    """GUI for Bible Downloader"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Clean Bible Downloader - Sefaria")
        self.root.geometry("800x700")
        
        self.downloader = CleanBibleDownloader()
        
        self.create_widgets()
        
        # Update chapter count when book changes
        self.book_var.trace('w', self.update_chapter_range)
    
    def create_widgets(self):
        """Create GUI widgets"""
        # Title
        title_label = tk.Label(self.root, text="Clean Bible Text Downloader", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Book selection
        book_frame = tk.LabelFrame(main_frame, text="Book Selection", font=('Arial', 12, 'bold'))
        book_frame.pack(fill='x', pady=5)
        
        tk.Label(book_frame, text="Book:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        
        self.book_var = tk.StringVar(value='Genesis')
        book_combo = ttk.Combobox(book_frame, textvariable=self.book_var, 
                                  values=list(self.downloader.bible_books.values()),
                                  width=30)
        book_combo.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        book_frame.grid_columnconfigure(1, weight=1)
        
        # Version selection
        version_frame = tk.LabelFrame(main_frame, text="Version", font=('Arial', 12, 'bold'))
        version_frame.pack(fill='x', pady=5)
        
        tk.Label(version_frame, text="Version:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        
        self.version_var = tk.StringVar(value='he-en')
        version_combo = ttk.Combobox(version_frame, textvariable=self.version_var,
                                    values=list(self.downloader.versions.keys()),
                                    width=30)
        version_combo.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        # Version description
        self.version_desc = tk.Label(version_frame, text="Hebrew + English (Side by side)", 
                                   font=('Arial', 9), fg='gray')
        self.version_desc.grid(row=1, column=1, padx=5, pady=2, sticky='w')
        
        version_frame.grid_columnconfigure(1, weight=1)
        
        # Update version description when version changes
        self.version_var.trace('w', self.update_version_description)
        
        # Download options
        options_frame = tk.LabelFrame(main_frame, text="Download Options", font=('Arial', 12, 'bold'))
        
        # Chapter selection
        chapter_frame = tk.Frame(options_frame)
        
        self.download_type = tk.StringVar(value='chapter')
        
        rb1 = tk.Radiobutton(chapter_frame, text="Specific Chapter:", variable=self.download_type, 
                            value='chapter', command=self.toggle_download_options)
        rb1.pack(side='left', padx=5)
        
        self.chapter_var = tk.StringVar(value='1')
        self.chapter_spinbox = ttk.Spinbox(chapter_frame, from_=1, to=1, 
                                         textvariable=self.chapter_var, width=10)
        self.chapter_spinbox.pack(side='left', padx=5)
        
        chapter_frame.pack(anchor='w', pady=5)
        
        rb2 = tk.Radiobutton(options_frame, text="Entire Book", variable=self.download_type, 
                            value='book', command=self.toggle_download_options)
        rb2.pack(anchor='w', padx=5, pady=5)
        
        options_frame.pack(fill='x', pady=5)
        
        # Output directory
        output_frame = tk.LabelFrame(main_frame, text="Output", font=('Arial', 12, 'bold'))
        
        tk.Label(output_frame, text="Save to:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        
        self.output_var = tk.StringVar(value='clean_downloads')
        output_entry = ttk.Entry(output_frame, textvariable=self.output_var, width=50)
        output_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        browse_btn = ttk.Button(output_frame, text="Browse", command=self.browse_output_dir)
        browse_btn.grid(row=0, column=2, padx=5, pady=5)
        
        output_frame.grid_columnconfigure(1, weight=1)
        output_frame.pack(fill='x', pady=5)
        
        # Preview area
        preview_frame = tk.LabelFrame(main_frame, text="Preview", font=('Arial', 12, 'bold'))
        preview_frame.pack(fill='both', expand=True, pady=5)
        
        self.preview_text = scrolledtext.ScrolledText(preview_frame, height=10, font=('David', 12))
        self.preview_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Button frame
        button_frame = tk.Frame(main_frame)
        
        preview_btn = ttk.Button(button_frame, text="Preview Book Info", command=self.preview_book)
        preview_btn.pack(side='left', padx=5)
        
        download_btn = ttk.Button(button_frame, text="Download", command=self.start_download)
        download_btn.pack(side='left', padx=5)
        
        clear_btn = ttk.Button(button_frame, text="Clear Preview", command=self.clear_preview)
        clear_btn.pack(side='left', padx=5)
        
        button_frame.pack(pady=10)
    
    def update_version_description(self, *args):
        """Update version description label"""
        version = self.version_var.get()
        descriptions = {
            'he': 'Hebrew (Original)',
            'en': 'English Translation', 
            'he-en': 'Hebrew + English (Side by side)'
        }
        self.version_desc.config(text=descriptions.get(version, ''))
    
    def update_chapter_range(self, *args):
        """Update chapter range when book changes"""
        book_name = self.downloader.bible_books.get(
            list(self.downloader.bible_books.keys())[
                list(self.downloader.bible_books.values()).index(self.book_var.get())
            ]
        )
        
        chapter_count = self.downloader.get_chapter_count(book_name)
        self.chapter_spinbox.config(to=chapter_count)
        
        # Reset to chapter 1 if current selection exceeds range
        current_chapter = int(self.chapter_var.get())
        if current_chapter > chapter_count:
            self.chapter_var.set('1')
    
    def toggle_download_options(self):
        """Toggle download options based on selection"""
        if self.download_type.get() == 'book':
            self.chapter_spinbox.config(state='disabled')
        else:
            self.chapter_spinbox.config(state='normal')
    
    def browse_output_dir(self):
        """Browse for output directory"""
        directory = filedialog.askdirectory()
        if directory:
            self.output_var.set(directory)
    
    def preview_book(self):
        """Preview book information"""
        book_name = self.downloader.bible_books.get(
            list(self.downloader.bible_books.keys())[
                list(self.downloader.bible_books.values()).index(self.chapter_var.get())
            ]
        )
        
        if book_name:
            chapter_count = self.downloader.get_chapter_count(book_name)
            
            preview_text = f"""Book: {self.book_var.get()} ({book_name})
Version: {self.downloader.versions[self.version_var.get()]}
Total Chapters: {chapter_count}

Ready to download: {'Entire book' if self.download_type.get() == 'book' else f'Chapter {self.chapter_var.get()}'}
Output Directory: {self.output_var.get()}
"""
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(1.0, preview_text)
    
    def clear_preview(self):
        """Clear preview text"""
        self.preview_text.delete(1.0, tk.END)
    
    def start_download(self):
        """Start the download process"""
        # Run download in separate thread to avoid freezing GUI
        thread = threading.Thread(target=self.download_worker)
        thread.daemon = True
        thread.start()
    
    def download_worker(self):
        """Worker thread for download"""
        try:
            book_name = self.downloader.bible_books.get(
                list(self.downloader.bible_books.keys())[
                    list(self.downloader.bible_books.values()).index(self.book_var.get())
                ]
            )
            
            version = self.version_var.get()
            output_dir = self.output_var.get()
            
            # Create output directory
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            if self.download_type.get() == 'book':
                # Download entire book
                self.preview_text.insert(tk.END, f"\nStarting download of entire {self.book_var.get()}...\n")
                self.root.update()
                
                data = self.downloader.download_book(book_name, version)
                
                if 'error' not in data:
                    self.save_clean_text(data, output_dir, f"{book_name}_complete", version)
                    self.preview_text.insert(tk.END, f"Download completed! Saved to {output_dir}\n")
                else:
                    self.preview_text.insert(tk.END, f"Error: {data['error']}\n")
            
            else:
                # Download specific chapter
                chapter = int(self.chapter_var.get())
                self.preview_text.insert(tk.END, f"\nDownloading {self.book_var.get()} Chapter {chapter}...\n")
                self.root.update()
                
                data = self.downloader.download_chapter(book_name, chapter, version)
                
                if 'error' not in data:
                    self.save_clean_text(data, output_dir, f"{book_name}_chapter_{chapter}", version)
                    self.preview_text.insert(tk.END, f"Download completed! Saved to {output_dir}\n")
                else:
                    self.preview_text.insert(tk.END, f"Error: {data['error']}\n")
                    
        except Exception as e:
            self.preview_text.insert(tk.END, f"Download error: {str(e)}\n")
        
        self.root.update()
    
    def save_clean_text(self, data: Dict, output_dir: str, filename: str, version: str):
        """Save clean text to files"""
        
        # Save Hebrew text
        if data['hebrew']:
            hebrew_file = Path(output_dir) / f"{filename}_hebrew_clean.txt"
            with open(hebrew_file, 'w', encoding='utf-8') as f:
                f.write(f"Clean Hebrew Text - {filename}\n")
                f.write("=" * 50 + "\n\n")
                for line in data['hebrew']:
                    f.write(line + "\n")
        
        # Save English text
        if data['english']:
            english_file = Path(output_dir) / f"{filename}_english_clean.txt"
            with open(english_file, 'w', encoding='utf-8') as f:
                f.write(f"Clean English Text - {filename}\n")
                f.write("=" * 50 + "\n\n")
                for line in data['english']:
                    f.write(line + "\n")
        
        # Save combined text
        if data['hebrew'] and data['english']:
            combined_file = Path(output_dir) / f"{filename}_parallel_clean.txt"
            with open(combined_file, 'w', encoding='utf-8') as f:
                f.write(f"Parallel Hebrew-English Text - {filename}\n")
                f.write("=" * 50 + "\n\n")
                
                # Determine which array is longer
                max_lines = max(len(data['hebrew']), len(data['english']))
                
                for i in range(max_lines):
                    hebrew_line = data['hebrew'][i] if i < len(data['hebrew']) else ""
                    english_line = data['english'][i] if i < len(data['english']) else ""
                    
                    f.write(f"\n--- Verse {i+1} ---\n")
                    f.write(f"Hebrew:  {hebrew_line}\n")
                    f.write(f"English: {english_line}\n")
        
        # Show preview of downloaded content
        self.preview_text.insert(tk.END, f"\nSaved files:\n")
        
        if data['hebrew']:
            self.preview_text.insert(tk.END, f"- {filename}_hebrew_clean.txt\n")
        
        if data['english']:
            self.preview_text.insert(tk.END, f"- {filename}_english_clean.txt\n")
        
        if data['hebrew'] and data['english']:
            self.preview_text.insert(tk.END, f"- {filename}_parallel_clean.txt\n")
    
    def run(self):
        """Run the GUI"""
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = BibleDownloaderGUI()
        app.run()
    except Exception as e:
        print(f"Error starting GUI: {e}")
        print("Make sure tkinter is installed: sudo apt-get install python3-tk")
