import requests
from ..types.news import News
from ..config import NEWS_API_KEY, NEWS_CATEGORY, NEWS_LANGUAGE, NEWS_COUNTRY
from typing import List

def get_latest_news() -> List[News]:
    url = f'https://gnews.io/api/v4/top-headlines?category={NEWS_CATEGORY}&lang={NEWS_LANGUAGE}&country={NEWS_COUNTRY}&max=10&apikey={NEWS_API_KEY}'
    response = requests.get(url)
    data = response.json()
    articles = []
    if 'articles' in data:
        for article in data['articles']:
            news_article = News(
                news_id=article.get('id', 0), 
                title=article.get('title', ''),
                description=article.get('description', ''),
                news_url=article.get('url', ''),
                image_url=article.get('image', ''),
                content=article.get('content', ''),
                is_posted=False
            )
            articles.append(news_article)
    
    return articles
