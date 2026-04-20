"""
Search and Ranking Engine for PySearch
--------------------------------------
This script is the main interface for the search engine.
It takes a user's search query, cleans the text, and looks for matching
words in the Inverted Index. To make sure the best results come first,
it uses the TF-IDF formula to score and rank the documents based on relevance.
While we have already captured the Term Frequency (TF) in our Inverted Index, we still need to implement the Inverse Document Frequency (IDF) logic. In the worst-case scenario, without a proper ranking system, the search engine would display the most irrelevant and useless links at the top. Therefore, we must mathematically score these results to ensure accuracy and relevance.
"""

import json
import os
import math
from Tokenization import clean_text

# ==========================================
# 📂 PATH SETUP
# ==========================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_FILE = os.path.join(BASE_DIR, "data", "inverted_index.json")


class PySearchEngine:
    def __init__(self, index_path):
        print("Loading Inverted Index into memory... Please wait.")
        with open(index_path, "r", encoding="utf-8") as f:
            self.index = json.load(f)

        # Calculate the total number of documents for IDF calculation
        self.total_docs = self._calculate_total_docs()
        print(f"Index loaded successfully! Total indexed documents: {self.total_docs}")

    def _calculate_total_docs(self):
        # Extract total unique URLs by adding them to a set
        unique_docs = set()
        for token, docs in self.index.items():
            for doc_uri in docs.keys():
                unique_docs.add(doc_uri)
        return max(1, len(unique_docs))  # Max 1 to prevent Divide by Zero errors

    def search(self, query, top_k=10):
        # 1. Clean and tokenize the user's query
        tokens = clean_text(query)
        if not tokens:
            return []

        scores = {}

        # 2. TF-IDF Scoring Logic
        for token in tokens:
            if token in self.index:
                doc_freq = len(
                    self.index[token]
                )  # Number of documents containing this word

                # Mathematical formula for IDF
                idf = math.log10(self.total_docs / doc_freq)

                # Score the document
                for uri, tf in self.index[token].items():
                    if uri not in scores:
                        scores[uri] = 0
                    scores[uri] += tf * idf

        # 3. Sort results (Highest score comes first)
        ranked_results = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        return ranked_results[:top_k]


# ==========================================
# 🚀 INTERACTIVE TERMINAL
# ==========================================
if __name__ == "__main__":
    if not os.path.exists(INDEX_FILE):
        print("Error: inverted_index.json not found. Please run indexer.py first.")
    else:
        engine = PySearchEngine(INDEX_FILE)

        print("\n" + "=" * 40)
        print("   🔍 WELCOME TO PYSEARCH ENGINE   ")
        print("=" * 40)

        while True:
            # Translated the user prompt to English
            user_query = input("\nEnter your search query (or type 'exit' to quit): ")

            if user_query.lower() == "exit":
                print("PySearch is closing. Goodbye!")
                break

            results = engine.search(user_query)

            if not results:
                print("No results found. Please try searching for something else.")
            else:
                print(f"\nTop {len(results)} Results for '{user_query}':")
                for i, (uri, score) in enumerate(results, 1):
                    print(f"{i}. {uri} (Relevance Score: {score:.4f})")
