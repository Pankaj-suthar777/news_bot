from ..db.db_connection import connect_to_mongodb
from ..types.news import News
from ..config import  collection_name

def insert_article_if_not_exists(article:News) -> bool:
    client, db = connect_to_mongodb()
    collection = db[collection_name]
    try:
        is_exist =  collection.find_one({"news_id": article["news_id"], "is_posted": False})
        if is_exist:
            print(f"Article with title '{article['title']}' already exists. Skipping insertion.")
            return False
        
        collection.insert_one(article)
        print("Article inserted successfully.")
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
        if result.modified_count > 0:
            print(f"Article with news_id '{news_id}' updated successfully.")
        else:
            print(f"No article found with news_id '{news_id}'.")
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
        if result.modified_count > 0:
            print(f"Article with news_id '{news_id}' updated successfully.")
        else:
            print(f"No article found with news_id '{news_id}'.")
    except Exception as e:
        print(f"Error updating article: {e}")
    finally:
        client.close()


        