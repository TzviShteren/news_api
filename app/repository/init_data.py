from app.db.mongo_db.connection import get_collection


def insert_event_to_mongo(data):
    try:
        get_collection().insert_one(data)
        print(f"Document inserted")

    except Exception as e:
        print(f"An error occurred: {e}")
