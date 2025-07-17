from sentence_transformers import SentenceTransformer
from app.logger import get_logger

logger = get_logger(__name__)

# Load pre-trained embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_sentences(sentences):
    """
    Converts a list of sentences (strings) into their vector embeddings
    """
    logger.info(f"Generating embeddings for {len(sentences)} sentences...")
    
    embeddings = model.encode(sentences, show_progress_bar=True)

    logger.info("Embedding generation complete.")
    return embeddings

# Test run
if __name__ == "__main__":
    test_sentences = [
        "India wins cricket match against Australia",
        "Stock markets rally as tech stocks rise"
    ]
    vectors = embed_sentences(test_sentences)
    print(vectors)
