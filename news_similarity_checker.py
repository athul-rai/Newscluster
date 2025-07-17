import requests
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Your NewsAPI Key
api_key = "530c11230d4d45309794557a7737c8fe"

# NewsAPI Endpoint and Parameters
url = "https://newsapi.org/v2/top-headlines"
params = {
    "language": "en",
    "pageSize": 30,  # fetch top 10 articles
    "apiKey": api_key,
}

# Fetch news articles
response = requests.get(url, params=params)
if response.status_code == 200:
    articles = response.json().get("articles", [])
    headlines = [article["title"] for article in articles]
    print(f"\nFetched {len(headlines)} headlines:\n")
    for title in headlines:
        print("-", title)
else:
    print("Failed to fetch news.")
    exit()

# Load the sentence-transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Convert headlines to embeddings
embeddings = model.encode(headlines)

# Compute similarity between headlines
similarity_matrix = cosine_similarity(embeddings)

# Find and display similar headlines
print("\n🔍 Similar Headlines (above 0.6 similarity):")
found_similar = False
for i in range(len(headlines)):
    for j in range(i + 1, len(headlines)):
        score = similarity_matrix[i][j]
        if score > 0.6:
            found_similar = True
            print(f"\n- {headlines[i]}\n- {headlines[j]}\nSimilarity: {score:.2f}")

if not found_similar:
    print("No similar headlines found.")
