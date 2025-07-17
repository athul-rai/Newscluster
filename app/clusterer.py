from sklearn.cluster import DBSCAN
import numpy as np
from app.logger import get_logger
from app import embedder

logger = get_logger(__name__)

def cluster_embeddings(embeddings, eps=0.45, min_samples=2) -> np.ndarray:
    """
    Cluster the sentence embeddings using DBSCAN (cosine metric).
    Returns a NumPy array of cluster labels.
    """
    if embeddings is None or len(embeddings) == 0:
        logger.error("No embeddings provided for clustering.")
        return np.array([])

    logger.info("Clustering embeddings using DBSCAN...")
    model = DBSCAN(eps=eps, min_samples=min_samples, metric="cosine")
    model.fit(np.array(embeddings))

    labels = model.labels_
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    logger.info(f"✅ Clustering complete. Found {n_clusters} clusters.")

    return labels

def cluster_articles(articles, eps=0.45, min_samples=2):
    """
    Cluster articles based on their titles.
    Returns a dictionary of {cluster_id: list of articles}.
    """
    if not articles:
        logger.error("No articles provided for clustering.")
        return {}

    titles = [a.get("title", "") for a in articles]
    embeddings = embedder.embed_sentences(titles)
    labels = cluster_embeddings(embeddings, eps=eps, min_samples=min_samples)

    clusters = {}
    for label, article in zip(labels, articles):
        clusters.setdefault(label, []).append(article)

    logger.info(f"✅ Grouped into {len(clusters)} total clusters (including noise).")
    return clusters
