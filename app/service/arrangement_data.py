import uuid
from app.repository.init_data import insert_event_to_mongo
from app.service.groq_client import get_full_details


def process_articles(articles):
    if not isinstance(articles, list):
        print("Error: Fetched articles are not in a list format.")
        return

    for article in articles:
        if not isinstance(article, dict):
            print(f"Skipping invalid article: {article}")
            continue

        try:
            # Generate UUID for the document
            doc_id = str(uuid.uuid4())

            # Get all details from Groq
            details = get_full_details(article)

            # Structure the document for MongoDB
            doc = {
                "_id": doc_id,  # Use generated UUID
                "summary": details['summary'],
                "attack_type": details['attack_type'],
                "num_perpetrators": details['num_perpetrators'],
                "date": {
                    "year": int(article.get("dateTime", "1970-01-01T00:00:00Z")[:4]),
                    "month": int(article.get("dateTime", "1970-01-01T00:00:00Z")[5:7]),
                    "day": int(article.get("dateTime", "1970-01-01T00:00:00Z")[8:10]),
                },
                "location": {
                    "country": details['country'],
                    "region": details['region'],
                    "province": details['province'],
                    "city": details['attack_type'],
                    "latitude": details['latitude'],
                    "longitude": details['longitude'],
                },
                "casualties": {
                    "num_killed": details['num_killed'],
                    "num_wounded": details['num_wounded'],
                    "property_damage_extent": details['property_damage_extent'],
                },
                "target": {
                    "type": details['type'],
                    "subtype": details['subtype'],
                    "nationality": details['nationality'],
                },
                "group": details['group'],
                "weapon": details['weapon'],
            }

            insert_event_to_mongo(doc)

            print(f"Document inserted/updated: {doc['_id']}")

        except Exception as e:
            print(f"Error processing article: {article.get('uri', 'Unknown')} - {e}")
