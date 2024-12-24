from app.service.arrangement_data import process_articles
from app.service.newsapi import fetch_articles
import time

if __name__ == '__main__':
    while True:
        articles = fetch_articles()
        process_articles(articles)
        time.sleep(120)
