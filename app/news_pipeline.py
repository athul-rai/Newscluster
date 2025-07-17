from app.embedder import embed_sentences
from app.clusterer import cluster_embeddings
from app.fetch_news import fetch_latest_news
from app.logger import get_logger
from app.save_results import save_to_json
from app.summarizer import summarize_cluster
from collections import defaultdict
from datetime import datetime
import numpy as np



logger = get_logger(__name__)

def convert_numpy_types(obj):
    if isinstance(obj, dict):
        return {k: convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(i) for i in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj

def run_news_pipeline():
    logger.info("Fetching latest news articles...")
    articles = fetch_latest_news()

    if not articles:
        logger.error("No articles fetched.")
        return {"status": "error", "message": "No articles fetched."}

    titles = [article['title'] for article in articles]

    logger.info(f"Embedding {len(titles)} article titles...")
    embeddings = embed_sentences(titles)

    logger.info("Clustering article embeddings...")
    labels = cluster_embeddings(embeddings, eps=0.45, min_samples=2)

    clustered_articles = defaultdict(list)
    for article, label in zip(articles, labels):
        clustered_articles[int(label)].append(article)

    final_clusters = []
    for cluster_id, articles_in_cluster in clustered_articles.items():
        if cluster_id == -1:
            summary = "Miscellaneous News"
        else:
            summary = summarize_cluster([a["title"] for a in articles_in_cluster])

        cluster_data = {
            "id": int(cluster_id),
            "summary": summary,
            "timestamp": datetime.now().isoformat(),
            "articles": articles_in_cluster
        }
        final_clusters.append(cluster_data)

    save_to_json(convert_numpy_types(final_clusters))
    logger.info(f"✅ Saved and returned {len(final_clusters)} total clusters.")
    return convert_numpy_types(final_clusters)
