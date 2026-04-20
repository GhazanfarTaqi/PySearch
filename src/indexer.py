"""
Indexer Module for PySearch
---------------------------
This script builds the core Inverted Index from the raw crawled data (raw.jsonl). 
To prevent Out-of-Memory (OOM) crashes in worst-case scenarios with massive datasets, 
it streams the file line-by-line, maintaining O(1) auxiliary memory per document. 
It cleans the text using the tokenization pipeline and maps each unique term to a 
Hash Map containing its source URIs and Term Frequencies (TF). The final structure 
is saved to disk, enabling O(1) time complexity for future search lookups.
"""

import json
import os
# Tumhari fast Tokenization file se function import kar rahe hain
from Tokenization import clean_text

# ==========================================
# 📂 PATH SETUP (Dynamic Paths)
# ==========================================
# Ye automatically PySearch folder ka rasta dhoondh lega
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # --> ../data/inverted_index.json 
DATA_DIR = os.path.join(BASE_DIR, "data")

INPUT_FILE = os.path.join(DATA_DIR, "raw.jsonl")
OUTPUT_INDEX_FILE = os.path.join(DATA_DIR, "inverted_index.json")

def build_inverted_index(input_path, output_path):
    print("Inverted Index banna shuru ho gaya hai...")
    inverted_index = {}
    
    try:
        # Worst-case O(1) space complexity ke liye line-by-line read
        with open(input_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file):
                try:
                    # JSON line ko dictionary mein convert karo
                    doc = json.loads(line.strip())
                    uri = doc.get("uri", "")
                    text = doc.get("text", "")
                    
                    if not uri or not text:
                        continue
                    
                    # 🚀 FAST TOKENIZATION: Text saaf karo aur tokens lo
                    tokens = clean_text(text)
                    
                    # ==========================================
                    # 🧠 INVERTED INDEX LOGIC
                    # ==========================================
                    for token in tokens:
                        if token not in inverted_index:
                            inverted_index[token] = {}
                        
                        # Term Frequency (TF) count kar rahe hain
                        if uri not in inverted_index[token]:
                            inverted_index[token][uri] = 1
                        else:
                            inverted_index[token][uri] += 1
                            
                except json.JSONDecodeError:
                    print(f"Skipping Line {line_num}: JSON parsing error.")
                    continue
                
                # Progress Update
                if (line_num + 1) % 50 == 0:
                    print(f"{line_num + 1} documents index ho gaye...")
                    
    except FileNotFoundError:
        print(f"Error: Input file nahi mili is path par: {input_path}")
        print("Make sure aapne Crawler run kiya hai aur raw.jsonl majood hai.")
        return

    # Index ko Disk par save karna
    print("Saving Inverted Index to disk...")
    with open(output_path, 'w', encoding='utf-8') as out_file:
        json.dump(inverted_index, out_file, ensure_ascii=False, indent=2)
        
    print(f"\nSuccess! Index ban kar '{output_path}' mein save ho gaya hai.")

if __name__ == "__main__":
    build_inverted_index(INPUT_FILE, OUTPUT_INDEX_FILE)