import requests

api_key = "530c11230d4d45309794557a7737c8fe"
url = "https://newsapi.org/v2/top-headlines"
params = {
    "language": "en",
    "pageSize": 5,
    "apiKey": api_key,
}

response = requests.get(url, params=params)
print(f"Response status code: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    articles = data.get("articles", [])
    print(f"Number of articles fetched: {len(articles)}")
    for article in articles:
        print(article["title"])
else:
    print("Failed to fetch news. Check your API key and network.")
