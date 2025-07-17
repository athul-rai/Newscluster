from app.fetch_news import fetch_latest_news
from app.logger import get_logger
from app.save_results import save_to_json
from app.manual_categorizer import categorize_article
from collections import defaultdict
from datetime import datetime
from rich.console import Console
from rich.table import Table

logger = get_logger(__name__)
console = Console()

if __name__ == "__main__":
    logger.info("Fetching latest news articles...")
    articles = fetch_latest_news()

    if not articles:
        logger.error("No articles fetched. Exiting.")
        exit()

    logger.info("Categorizing articles manually based on topic keywords...")
    clustered_articles = defaultdict(list)

    for article in articles:
        category = categorize_article(article)
        clustered_articles[category].append(article)

    final_clusters = []

    for category, articles_in_category in clustered_articles.items():
        console.print(f"\n[bold cyan]Category: {category}[/bold cyan]")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("No.", style="dim")
        table.add_column("Title")

        for idx, article in enumerate(articles_in_category, start=1):
            table.add_row(str(idx), article["title"])

        console.print(table)

        summary = category  # ✅ Just use the category name as summary

        cluster_data = {
            "id": category,
            "summary": summary,
            "timestamp": datetime.now().isoformat(),
            "articles": [
                {
                    "source": article.get("source", {}),
                    "author": article.get("author", None),
                    "title": article.get("title", ""),
                    "description": article.get("description", ""),
                    "url": article.get("url", ""),
                    "urlToImage": article.get("urlToImage", ""),
                    "publishedAt": article.get("publishedAt", ""),
                    "content": article.get("content", None),
                }
                for article in articles_in_category
            ]
        }
        final_clusters.append(cluster_data)

    save_to_json(final_clusters)
    logger.info("✅ Categorization and saving complete.")
