"""
Search and Ranking Engine for PySearch
--------------------------------------
This script is the main interface for the search engine.
It takes a user's search query, cleans the text, and looks for matching
words in the Inverted Index. To make sure the best results come first,
it uses the TF-IDF formula to score and rank the documents based on relevance.
"""

import json
import os
import math
import re  
from src.Tokenization import clean_text

# ==========================================
# 📂 PATH SETUP
# ==========================================
INDEX_FILE = r"C:\Users\ghaza\OneDrive\Desktop\Semester 4\Analysis of Algorithms\Project\pysearch\data\inverted_index.json"
DOCS_STORE_FILE = r"C:\Users\ghaza\OneDrive\Desktop\Semester 4\Analysis of Algorithms\Project\pysearch\data\docs_store.json" 


class PySearchEngine:
    def __init__(self, index_path, docs_path):
        print("Loading Inverted Index and Document Store into memory... Please wait.")
        with open(index_path, "r", encoding="utf-8") as f:
            self.index = json.load(f)

        with open(docs_path, "r", encoding="utf-8") as f:
            self.docs_store = json.load(f)

        # Calculate the total number of documents for IDF calculation
        self.total_docs = self._calculate_total_docs()
        print(f"Index loaded successfully! Total indexed documents: {self.total_docs}")

    def _calculate_total_docs(self):
        unique_docs = set()
        for token, docs in self.index.items():
            for doc_uri in docs.keys():
                unique_docs.add(doc_uri)
        return max(1, len(unique_docs))

    # ==========================================
    # 📏 EDIT DISTANCE (Levenshtein Distance)
    # ==========================================
    def _levenshtein_distance(self, s1, s2):
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]

    # ==========================================
    # 🤔 DID YOU MEAN - SUGGESTION ENGINE
    # ==========================================
    def find_closest_match(self, broken_word):
        best_match = None
        min_dist = float('inf')
        for valid_word in self.index.keys():
            dist = self._levenshtein_distance(broken_word, valid_word)
            # Find the closest match, allowing a max of 2 typos
            if dist < min_dist and dist <= 2: 
                min_dist = dist
                best_match = valid_word
        return best_match

    def get_spell_suggestion(self, raw_query):
        words = raw_query.split() 
        corrected_words = []
        has_changes = False

        for word in words:
            if word.lower() not in self.index:
                best_match = self.find_closest_match(word.lower()) 
                if best_match:
                    corrected_words.append(best_match)
                    has_changes = True
                else:
                    corrected_words.append(word)
            else:
                corrected_words.append(word)

        if has_changes:
            return " ".join(corrected_words) 
        return None

    # ==========================================
    # ✂️ SNIPPET GENERATOR LOGIC
    # ==========================================
    def _generate_snippet(self, text, tokens):
        lower_text = text.lower()
        for token in tokens:
            idx = lower_text.find(token)
            if idx != -1:
                start = max(0, idx - 50)
                end = min(len(text), idx + 80)
                snippet = text[start:end]
                highlighted_snippet = re.sub(
                    f"({token})", r"<b>\1</b>", snippet, flags=re.IGNORECASE
                )
                return "..." + highlighted_snippet.strip() + "..."
        return text[:100] + "..."

    def search(self, query, page=1, page_size=10):
        tokens = clean_text(query)
        if not tokens:
            return [], 0, None

        scores = {}
        
        for token in tokens:
            if token in self.index:
                doc_freq = len(self.index[token])
                idf = math.log10(self.total_docs / doc_freq)
                for uri, tf in self.index[token].items():
                    if uri not in scores:
                        scores[uri] = 0
                    scores[uri] += tf * idf

        # Generate "Did You Mean" using the full raw query
        did_you_mean_suggestion = self.get_spell_suggestion(query)

        ranked_results = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        total_matches = len(ranked_results)

        # Pagination Logic 
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size

        final_results = []
        for uri, score in ranked_results[start_idx:end_idx]:
            text_preview = self.docs_store.get(uri, "No text preview available.")
            snippet = self._generate_snippet(text_preview, tokens)
            final_results.append({"url": uri, "score": score, "snippet": snippet})

        return final_results, total_matches, did_you_mean_suggestion


# ==========================================
# 🚀 INTERACTIVE TERMINAL
# ==========================================
if __name__ == "__main__":
    if not os.path.exists(INDEX_FILE) or not os.path.exists(DOCS_STORE_FILE):
        print("Error: Required files not found. Please run indexer.py first.")
    else:
        engine = PySearchEngine(INDEX_FILE, DOCS_STORE_FILE)

        print("\n" + "=" * 40)
        print("   🔍 WELCOME TO PYSEARCH ENGINE   ")
        print("=" * 40)

        while True:
            user_query = input("\nEnter your search query (or type 'exit' to quit): ")

            if user_query.lower() == "exit":
                print("PySearch is closing. Goodbye!")
                break

            results, total_results, suggestions = engine.search(user_query)

            if not results:
                print("No results found. Please try searching for something else.")
                if suggestions:
                    print(f"\n💡 Did you mean: {suggestions}")
            else:
                print(f"\nTop {len(results)} Results for '{user_query}':")
                for i, res in enumerate(results, 1):
                    print(f"{i}. {res['url']} (Relevance Score: {res['score']:.4f})")
                    print(f"   Snippet: {res['snippet']}")
                
                if suggestions:
                    print(f"\n💡 Did you mean: {suggestions}")