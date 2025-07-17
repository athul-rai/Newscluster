import re

CATEGORIES = {
    "Politics": [
        "election", "trump", "biden", "government", "senate", "congress", "minister", "policy",
        "president", "parliament", "diplomacy", "diplomat", "campaign", "law", "republican", "democrat",
        "vote", "legislation", "cabinet", "immigration", "summit", "embassy", "prime minister",
        "democracy", "dictator", "coup", "referendum", "governor", "political", "ballot", "candidate",
        "ambassador", "legislature", "administration", "foreign affairs", "lawmaker", "executive",
        "judiciary", "convention", "policy maker", "politics"
    ],
    "Sports": [
        "football", "cricket", "nba", "fifa", "match", "tournament", "olympics", "goal", "tennis",
        "athlete", "soccer", "championship", "league", "score", "coach", "baseball", "rugby", "basketball",
        "medal", "boxing", "marathon", "player", "referee", "umpire", "season", "draft", "stadium",
        "scoreboard", "playoff", "world cup", "final", "team", "athletics", "swimming", "cycling",
        "gymnastics", "skateboarding", "esports", "sportswear", "sportsman", "sportswoman"
    ],
    "Technology": [
        "ai", "artificial intelligence", "robot", "software", "microsoft", "apple", "google", "startup",
        "computer", "smartphone", "chip", "gadget", "app", "cybersecurity", "blockchain", "internet",
        "algorithm", "data", "cloud", "device", "automation", "machine learning", "quantum",
        "programming", "coding", "developer", "internet of things", "iot", "vr", "virtual reality",
        "augmented reality", "ar", "5g", "network", "database", "cryptocurrency", "bitcoin", "eth",
        "technology", "software update", "operating system", "android", "ios", "tech giant", "processor"
    ],
    "Health": [
        "vaccine", "covid", "health", "hospital", "doctor", "mental health", "disease", "cancer",
        "virus", "pandemic", "treatment", "symptom", "infection", "medicine", "epidemic", "wellness",
        "nutrition", "surgery", "nurse", "clinic", "immunization", "public health", "healthcare",
        "pharmaceutical", "diagnosis", "outbreak", "flu", "epidemiology", "mental illness", "therapy",
        "healthcare policy", "cdc", "who", "medical research", "patient", "health insurance", "genetics"
    ],
    "Entertainment": [
        "movie", "film", "actor", "series", "music", "netflix", "celebrity", "drama", "bollywood",
        "hollywood", "concert", "album", "festival", "award", "director", "theater", "show", "comic",
        "tv", "pop star", "box office", "performance", "artist", "celebrity gossip", "broadway",
        "tv show", "music video", "release", "music awards", "soundtrack", "oscars", "emmy", "grammy",
        "celebrity news", "box office collection", "documentary", "streaming", "netflix series"
    ],
    "Science": [
        "nasa", "space", "mars", "moon", "physics", "biology", "scientist", "experiment",
        "research", "climate", "environment", "quantum", "discovery", "astronomy", "geology",
        "chemistry", "ecology", "genetics", "evolution", "scientific", "laboratory", "scientist",
        "spacecraft", "satellite", "scientific study", "climate change", "global warming",
        "biology research", "marine biology", "physics experiment", "solar system", "particle",
        "genome", "dna", "fossil", "earth science", "meteorology", "environmental science"
    ],
    "Business": [
        "stock", "market", "economy", "finance", "investment", "trade", "inflation", "bank",
        "company", "revenue", "profit", "shares", "billionaire", "startup", "merger", "acquisition",
        "tax", "industry", "commercial", "sales", "businessman", "entrepreneur", "funding",
        "ceo", "corporate", "stock exchange", "dow jones", "nasdaq", "wall street", "cryptocurrency",
        "blockchain", "financial report", "economics", "market share", "venture capital",
        "initial public offering", "ipo", "business news", "currency", "trade war", "economic policy"
    ],
}

def categorize_article(article):
    title = article.get("title") or ""
    description = article.get("description") or ""
    text = f"{title} {description}".lower()

    for category, keywords in CATEGORIES.items():
        for kw in keywords:
            # Escape special regex chars in keywords
            if re.search(rf"\b{re.escape(kw)}\b", text):
                return category

    return "Miscellaneous"
