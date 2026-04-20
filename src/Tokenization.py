# Final code of Tokenization for PySearch

import re
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# ==========================================
# 🚀 INITIALIZATION OUTSIDE THE FUNCTION
# Yeh sab RAM mein sirf 1 dafa load hoga
# ==========================================
EMAIL_REGEX = re.compile(r'\S+@\S+')
PUNCT_TABLE = str.maketrans('', '', string.punctuation)
STOP_WORDS = set(stopwords.words('english'))
STEMMER = PorterStemmer()

def clean_text(text):
    # 1. Emails remove karo (Pre-compiled regex use kar rahe hain)
    text = EMAIL_REGEX.sub('', text)
    
    # 2. Remove emojis and symbols
    text = text.encode('ascii', 'ignore').decode('ascii')
    
    # 3. Punctuation hatao (Pre-compiled table use kar rahe hain)
    text = text.translate(PUNCT_TABLE)
    
    # 4. Tokenize aur Lowercase
    # PRO TIP: NLTK ka `word_tokenize` phir bhi thora slow hai. 
    # Agar tumhe XTREME SPEED chahiye toh iski jagah sirf `tokens = text.lower().split()` use kar lena!
    tokens = word_tokenize(text.lower())
    
    # 5. Stopwords hatao aur Stemming karo
    # Yahan pehle se loaded STEMMER aur STOP_WORDS use honge
    cleaned_tokens = [STEMMER.stem(w) for w in tokens if w not in STOP_WORDS and w.isalnum()]
    
    return cleaned_tokens

# Testing
if __name__ == "__main__":
    sample = "The boy is running and sending emails to info@domain.org! 😊"
    
    text = """
    Hello! 😊 This is a test email@example.com. 
    Can you remove this? 👍 Also, check info@domain.org! 
    """
    
    text1 = "Hello! 😊 This is a test email@example.com. Can you remove this? 👍 Also, check info@domain.org!"
    
    print(clean_text(sample))
    print(clean_text(text))
    print(clean_text(text1))