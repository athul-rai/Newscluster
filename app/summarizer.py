from transformers import pipeline
from app.logger import get_logger

logger = get_logger(__name__)

# Load a pre-trained summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_cluster(titles):
    logger.info(f"Summarizing cluster with {len(titles)} articles")
    text = " ".join(titles)

    if len(text) > 3000:
        text = text[:3000]

    input_length = len(text.split())
    max_length = min(60, max(25, input_length // 2 + 10))
    min_length = min(20, max_length - 5)

    summary = summarizer(
        text,
        max_length=max_length,
        min_length=min_length,
        do_sample=False
    )
    return summary[0]['summary_text']

def summarize_clusters(clusters):
    logger.info(f"Summarizing {len(clusters)} clusters")
    results = {}

    for cluster_id, articles in clusters.items():
        titles = [article.get("title", "") for article in articles]
        summary_text = summarize_cluster(titles)

        results[cluster_id] = {
            "id": cluster_id,
            "summary": summary_text,
            "articles": articles
        }

    return results
