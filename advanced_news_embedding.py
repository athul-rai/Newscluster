import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sentence_transformers import SentenceTransformer

# Download nltk resources (run once)
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Preprocessing function
def preprocess_text(text):
    # Lowercase
    text = text.lower()
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    # Remove punctuation & non-alphabetic chars
    text = re.sub(r'[^a-z\s]', '', text)
    # Tokenize & remove stopwords
    tokens = text.split()
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    # Lemmatize tokens
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    # Join back to string
    return ' '.join(tokens)

# Example headlines list (replace with your fetched data)
headlines = [
    "Trade war live: Trump says no extension to August tariff deadline",
    "Yankees finally moving Jazz Chisholm back to second base",
    "TSA will no longer require all passengers to take shoes off at airport security checkpoints"
]

# Preprocess headlines
cleaned_headlines = [preprocess_text(h) for h in headlines]

# Load stronger embedding model
model = SentenceTransformer('paraphrase-mpnet-base-v2')

# Encode cleaned headlines
embeddings = model.encode(cleaned_headlines)

# Show embeddings shape
print(f"Encoded {len(cleaned_headlines)} headlines into embeddings of shape: {embeddings.shape}")
