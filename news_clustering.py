import re
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

# Sample headlines (replace these later with your fetched headlines)
headlines = [
    "Trade war live: Trump says no extension to August tariff deadline",
    "Trump administration delays tariff deadline amid trade war concerns",
    "Yankees finally moving Jazz Chisholm back to second base",
    "Samsung’s event spoiled by massive last-minute leak",
    "New Samsung products leaked hours before big event"
]

# Preprocess headlines
cleaned_headlines = [preprocess_text(h) for h in headlines]

# Load powerful embedding model
model = SentenceTransformer('paraphrase-mpnet-base-v2')

# Embed cleaned headlines
embeddings = model.encode(cleaned_headlines)

# Compute cosine distance matrix
distance_matrix = cosine_distances(embeddings)

# Apply DBSCAN clustering (eps=0.4 is a good starting point, tweakable)
clustering_model = DBSCAN(eps=0.4, min_samples=2, metric='precomputed')
labels = clustering_model.fit_predict(distance_matrix)

# Group and display clustered headlines
clusters = {}
for idx, label in enumerate(labels):
    clusters.setdefault(label, []).append(headlines[idx])

# Print clusters
for cluster_id, cluster_headlines in clusters.items():
    if cluster_id != -1:  # -1 means noise/unclustered
        print(f"\n🗞️ Cluster {cluster_id}:")
        for headline in cluster_headlines:
            print(f"  - {headline}")

# Print noise articles (unclustered)
if -1 in clusters:
    print(f"\n❌ No Cluster (Unique Headlines):")
    for headline in clusters[-1]:
        print(f"  - {headline}")
