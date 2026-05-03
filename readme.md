🔍 PySearch - Full-Stack End-to-End Search Engine
PySearch aik powerful, scratch-built search engine hai jo sirf word-matching nahi karta, balkay TF-IDF Ranking aur NLP Tokenization ka istemal kar ke relevancy ke mutabiq results dikhata hai. Ye project Data Structures (Hash Maps) aur Algorithms ki real-world implementation ko demonstrate karta hai.

🚀 Key Highlights
🌐 Custom Web Crawler: Common Crawl data (WET files) se massive amount mein data stream karta hai.

🧠 Intelligent Tokenization: NLTK library ka use kar ke stopwords remove karta hai aur Porter Stemmer ke zariye words ko unki base form mein lata hai.

⚡ O(1) Inverted Index: Aik advanced Hash Map structure jo lakon documents mein se constant time mein words dhoond nikalta hai.

📊 TF-IDF Ranking Engine: Mathematical formula (Term Frequency-Inverse Document Frequency) ka use kar ke results ko rank karta hai.

💡 "Did You Mean?" Feature: Levenshtein Distance algorithm ka istemal kar ke typos dhoondta hai aur search suggestions deta hai.

📝 Smart Snippets: Regex ke zariye search term ko highlight karta hai aur context preview generate karta hai.

🔌 Modern Stack: FastAPI backend aur Vanilla JS frontend jo full-page pagination support karta hai.

🏗️ Technical Architecture
Crawl: crawler.py raw internet data fetch kar ke raw.jsonl banata hai.

Index: indexer.py text ko clean kar ke aik inverted index aur document store (metadata) generate karta hai.

Search: search.py user ki query ko process karta hai, suggestions dhoondta hai aur TF-IDF score calculate karta hai.

Serve: api.py CORS-enabled REST API ke zariye frontend ko data bhejta hai.

📂 Project Structure
Plaintext
PySearch/
├── data/                    # Generated Data (Git Ignored)
│   ├── raw.jsonl            # Scraped content
│   ├── inverted_index.json  # Fast lookup hash map
│   └── docs_store.json      # Snippets & Metadata
├── src/                     # Core Logic
│   ├── crawler.py           # Data acquisition
│   ├── Tokenization.py      # NLP Pipeline
│   ├── indexer.py           # Index building
│   ├── search.py            # Ranking & Suggestions
│   └── api.py               # FastAPI Server
├── index.html               # Frontend UI
├── requirements.txt         # Dependencies
└── README.md                # Documentation
🛠️ Setup & Installation
Step 1: Clone & Install
Bash
git clone https://github.com/Muhammad-Yahya-Sohail/PySearch.git
cd PySearch
pip install -r requirements.txt
Step 2: Prepare NLP Data
Python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
Step 3: Run the Pipeline
Crawl Data: python src/crawler.py

Build Index: python src/indexer.py

Step 4: Launch API & UI
Bash
# Main directory se server start karein
uvicorn src.api:app --reload
API running at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

Ab simply index.html ko browser mein open karein (Live Server recommended) aur search shuru karein!

🤝 Contribution
Agar aap koi improvement ya naya algorithm add karna chahte hain, to Pull Request zaroor bhejein!

Developed with ❤️ by Muhammad Yahya Sohail