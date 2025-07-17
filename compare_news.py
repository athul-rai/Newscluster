from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Sample news headlines
headlines = [
    "S&P 500 Futures Hold Steady as Trump Buys Time",
    "Trump aides discuss Ukraine weapons after shipments resume",
    "Kremlin calls transportation minister's death tragic",
    "Trump administration to send new military aid to Ukraine",
    "S&P 500 markets stay flat amid political concerns"
]

# Load the sentence-transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Convert headlines to vector embeddings
embeddings = model.encode(headlines)

# Compute cosine similarity between all headline embeddings
similarity_matrix = cosine_similarity(embeddings)

# Show similarity scores for each pair of headlines
for i in range(len(headlines)):
    for j in range(i + 1, len(headlines)):
        score = similarity_matrix[i][j]
        if score > 0.6:  # threshold for considering headlines similar
            print(f"\nSimilar:\n- {headlines[i]}\n- {headlines[j]}\nSimilarity: {score:.2f}")
