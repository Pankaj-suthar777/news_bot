from pymongo import MongoClient
from ..config import MONGO_URI, database_name, collection_name

def connect_to_mongodb(
    timeout_ms=30000   
):
    try:
            
        uri = MONGO_URI
        client = MongoClient(uri, serverSelectionTimeoutMS=timeout_ms)

        # Test the connection
        client.server_info()  
        
        # Access the database
        db = client[database_name]
        
        print("Connected successfully!")

        create_index(db, collection_name, "news_id")

        return client, db
    
    except Exception as e:
        print(f"Connection failed: {e}")
        raise

def create_index(db, collection_name, field_name):
    collection = db[collection_name]
    
    # Get list of existing indexes
    existing_indexes = collection.index_information()
    
    # Check if index already exists
    index_exists = any(
        field_name in [f[0] for f in index['key']]
        for index in existing_indexes.values()
    )
    
    if index_exists:
        print(f"Index on '{field_name}' already exists.")
    else:
        collection.create_index(field_name)
        print(f"Index on '{field_name}' created successfully.")
