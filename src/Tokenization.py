# Final code of Tokenization for PySearch

import re
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

def clean_text(text):
    # 1. Emails remove karo (Fixed Regex)
    text = re.sub(r'\S+@\S+', '', text)
    
    # Step 2: Remove emojis and symbols
    text = text.encode('ascii', 'ignore').decode('ascii')
    
    # 3. Punctuation hatao
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # 4. Tokenize aur Lowercase
    tokens = word_tokenize(text.lower())
    
    # 5. Stopwords hatao aur Stemming karo
    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()
    
    # Sirf wo words rakho jo stopword nahi hain aur unki base form lo
    cleaned_tokens = [ps.stem(w) for w in tokens if w not in stop_words and w.isalnum()]
    
    return cleaned_tokens

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