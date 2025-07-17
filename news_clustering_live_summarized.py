import re
import requests
import nltk
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_distances
from transformers import pipeline
from datetime import datetime

# Download NLTK Resources
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Output file to save results (append mode)
output_file = open("output_clusters.txt", "a", encoding="utf-8")

# Write log divider
output_file.write("\n" + "="*80 + "\n")

# Text Preprocessing
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

# Fetch live headlines
def fetch_live_headlines(api_key, page_size=30):
    url = "https://newsapi.org/v2/top-headlines"
    params = {"language": "en", "pageSize": page_size, "apiKey": api_key}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        return [article["title"] for article in articles if article["title"]]
    else:
        text = f"❌ Failed to fetch news. Status Code: {response.status_code}"
        print(text)
        output_file.write(text + "\n")
        return []

# Summarizer pipeline (using BART)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# API key (replace if needed)
api_key = "530c11230d4d45309794557a7737c8fe"

# Fetch news
headlines = fetch_live_headlines(api_key, page_size=30)
if not headlines:
    text = "No headlines fetched."
    print(text)
    output_file.write(text + "\n")
    output_file.close()
    exit()

# Print timestamp and fetched headlines
timestamp = f"\n🕒 Fetched {len(headlines)} live headlines at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:\n"
print(timestamp)
output_file.write(timestamp + "\n")

for h in headlines:
    print("-", h)
    output_file.write("- " + h + "\n")

# Preprocess and encode headlines
cleaned_headlines = [preprocess_text(h) for h in headlines]
model = SentenceTransformer('paraphrase-mpnet-base-v2')

try:
    embeddings = model.encode(cleaned_headlines)
except Exception as e:
    error_msg = f"⚠️ Embedding generation failed: {e}"
    print(error_msg)
    output_file.write(error_msg + "\n")
    output_file.close()
    exit()

# Compute cosine distance matrix and cluster with DBSCAN
distance_matrix = cosine_distances(embeddings)
clustering_model = DBSCAN(eps=0.5, min_samples=2, metric='precomputed')
labels = clustering_model.fit_predict(distance_matrix)

# Group headlines by cluster label
clusters = {}
for idx, label in enumerate(labels):
    clusters.setdefault(label, []).append(headlines[idx])

# Display clusters with summaries
for cluster_id, cluster_headlines in clusters.items():
    if cluster_id != -1:
        text = f"\n🗞️ Cluster {cluster_id} ({len(cluster_headlines)} headlines):"
        print(text)
        output_file.write(text + "\n")

        for headline in cluster_headlines:
            print(f"  - {headline}")
            output_file.write(f"  - {headline}\n")

        combined_text = " ".join(cluster_headlines)

        # Generate summary if text is long enough
        if len(combined_text.split()) > 30:
            try:
                summary = summarizer(
                    combined_text,
                    max_length=60,
                    min_length=20,
                    do_sample=False
                )[0]['summary_text']
                summary_text = f"\n📌 Summary: {summary}"
                print(summary_text)
                output_file.write(summary_text + "\n")
            except Exception as e:
                error_text = f"\n⚠️ Could not generate summary: {e}"
                print(error_text)
                output_file.write(error_text + "\n")

# Show unclustered (unique) headlines
if -1 in clusters:
    text = f"\n❌ Unique (Unclustered) Headlines ({len(clusters[-1])}):"
    print(text)
    output_file.write(text + "\n")
    for headline in clusters[-1]:
        print(f"  - {headline}")
        output_file.write(f"  - {headline}\n")

# Close the output file
output_file.close()
print("\n📄 Results saved to 'output_clusters.txt'")
