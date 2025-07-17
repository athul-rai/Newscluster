import requests
from app.logger import get_logger
from rapidfuzz import fuzz
import os
from dotenv import load_dotenv
from datetime import datetime
import random

logger = get_logger(__name__)
load_dotenv()

NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
API_KEYS = os.getenv("NEWS_API_KEYS", "").split(",")

def fetch_latest_news():
    logger.info("Fetching latest worldwide news articles...")
    articles = []

    if not API_KEYS or API_KEYS == [""]:
        logger.error("No API keys found. Check your .env file or environment variables.")
        return []

    today = datetime.now().date().isoformat()
    logger.info(f"Fetching articles from: {today}")

    # Shuffle API keys to avoid overloading the first one
    random.shuffle(API_KEYS)

    for key in API_KEYS:
        if not key.strip():
            logger.warning("Encountered empty API key, skipping...")
            continue

        for page in range(1, 6):  # Up to 500 articles (100 per page)
            params = {
                "pageSize": 100,
                "page": page,
                "apiKey": key,
                "language": "en",
                "from": today,  # 🔥 force freshness
                "sortBy": "publishedAt",  # Optional: newer articles first
                "country": "us"  # Optional: reduce junk
            }

            try:
                response = requests.get(NEWS_API_URL, params=params, timeout=10)
                logger.info(f"[{key[:4]}...] Page {page}: {response.status_code}")

                if response.status_code == 200:
                    fetched = response.json().get("articles", [])
                    logger.info(f"Fetched {len(fetched)} articles from page {page}")
                    articles.extend(fetched)
                    if len(fetched) < 100:
                        break
                else:
                    logger.warning(f"Key {key[:4]}... failed on page {page}: {response.text[:200]}")
                    break

            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed for key {key[:4]}... page {page}: {str(e)}")
                break

    logger.info(f"Total fetched before deduplication: {len(articles)}")
    deduplicated = clean_and_deduplicate_articles(articles)
    logger.info(f"Total unique articles retained: {len(deduplicated)}")
    return deduplicated

def clean_and_deduplicate_articles(articles, similarity_threshold=90):
    seen_titles = []
    unique_articles = []

    for article in articles:
        title = article.get("title", "").strip().lower()
        if not title:
            continue

        duplicate_found = False
        for seen in seen_titles:
            if fuzz.ratio(title, seen) > similarity_threshold:
                duplicate_found = True
                break

        if not duplicate_found:
            seen_titles.append(title)
            unique_articles.append(article)

    return unique_articles
