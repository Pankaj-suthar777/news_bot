from ..db.db_connection import connect_to_mongodb
from ..types.news import News
from ..config import  collection_name
import json
from .gemini import get_gemini_response
from .twitter import post_tweet_with_image_url
from ..utils.formatting import format_article_to_post
from .news_service import get_latest_news

def insert_article_if_not_exists(article:News) -> bool:
    client, db = connect_to_mongodb()
    collection = db[collection_name]
    try:
        is_exist =  collection.find_one({"news_id": article["news_id"], "is_posted": False})
        if is_exist:
            return False
        
        collection.insert_one(article)
        client.close()

        return True
    except Exception as e:
        print(f"Error inserting article: {e}")
        client.close()
        return False

def update_posted_status(news_id: str, is_posted: bool):
    client, db = connect_to_mongodb()
    collection = db[collection_name]
    try:
        result = collection.update_one(
            {"news_id": news_id},
            {"$set": {"is_posted": is_posted}}
        )
    except Exception as e:
        print(f"Error updating article: {e}")
    finally:
        client.close()


def add_fields_in_db_post_document(news_id: str, fields: dict):
    client, db = connect_to_mongodb()
    collection = db[collection_name]
    try:
        result = collection.update_one(
            {"news_id": news_id},
            {"$set": fields}
        )
    except Exception as e:
        print(f"Error updating article: {e}")
    finally:
        client.close()


        
def process_news_in_background():
    news = get_latest_news()

    for article in news:
        insert_article_if_not_exists(article)
        gemini_response = get_gemini_response(article)

        data = json.loads(gemini_response)

        formatted_post_content = format_article_to_post(data)
        post_tweet_with_image_url(
            formatted_post_content,
            article["image_url"],
            f"Check it out 👇\n{article['news_url']}"
        )

        update_posted_status(article["news_id"], True)
        add_fields_in_db_post_document(article["news_id"], data)

    print("✅ Finished posting all articles in background")