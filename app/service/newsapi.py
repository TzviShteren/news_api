import requests
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

page = 1


def fetch_articles():
    global page
    payload = {
        "action": "getArticles",
        "keyword": "terror attack",
        "ignoreSourceGroupUri": "paywall/paywalled_sources",
        "articlesPage": page,
        "articlesCount": 100,
        "articlesSortBy": "socialScore",
        "articlesSortByAsc": False,
        "dataType": ["news", "pr"],
        "forceMaxDataTimeWindow": 31,
        "resultType": "articles",
        "apiKey": os.environ['NEWS_KEY']
    }
    try:
        response = requests.post(os.environ['NEWS_URL'], json=payload)
        response.raise_for_status()
        print(f"Page {page} fetched successfully.")
        page += 1
        return response.json().get("articles", {}).get("results", [])

    except requests.exceptions.RequestException as e:
        print(f"Error fetching articles for page {page}: {e}")

