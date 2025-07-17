import re
import requests
import nltk
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_distances

# Download NLTK resources (if not already done)
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Preprocessing function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'[^a-z\s]', '', text)
    tokens = text.split()
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(tokens)

# Fetch live news from NewsAPI
def fetch_live_headlines(api_key, page_size=30):
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "language": "en",
        "pageSize": page_size,
        "apiKey": api_key,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        headlines = [article["title"] for article in articles if article["title"]]
        return headlines
    else:
        print("Failed to fetch news.")
        return []

# Your NewsAPI key
api_key = "530c11230d4d45309794557a7737c8fe"

# Fetch live headlines
headlines = fetch_live_headlines(api_key, page_size=30)

if not headlines:
    print("No headlines fetched. Exiting.")
    exit()

print(f"\n📡 Fetched {len(headlines)} live headlines:\n")
for h in headlines:
    print("-", h)

# Preprocess
cleaned_headlines = [preprocess_text(h) for h in headlines]

# Load high-quality embedding model
model = SentenceTransformer('paraphrase-mpnet-base-v2')

# Encode embeddings
embeddings = model.encode(cleaned_headlines)

# Compute cosine distance matrix
distance_matrix = cosine_distances(embeddings)

# Apply DBSCAN clustering
clustering_model = DBSCAN(eps=0.4, min_samples=2, metric='precomputed')

labels = clustering_model.fit_predict(distance_matrix)

# Group clustered headlines
clusters = {}
for idx, label in enumerate(labels):
    clusters.setdefault(label, []).append(headlines[idx])

# Display results
for cluster_id, cluster_headlines in clusters.items():
    if cluster_id != -1:
        print(f"\n🗞️ Cluster {cluster_id}:")
        for headline in cluster_headlines:
            print(f"  - {headline}")

# Print unclustered (unique) headlines
if -1 in clusters:
    print(f"\n❌ Unique (Unclustered) Headlines:")
    for headline in clusters[-1]:
        print(f"  - {headline}")
