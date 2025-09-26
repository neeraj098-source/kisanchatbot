import json
from pymongo import MongoClient

# --- Connection Setup ---
CONNECTION_STRING = "mongodb+srv://Neeraj:neeraj7204yadav@cluster0neeraj.q7birvm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0neeraj"
DB_NAME = "kisan_sahayak"
COLLECTION_NAME = "knowledge_base"

# --- Script Logic ---
try:
    # Connect to the database
    client = MongoClient(CONNECTION_STRING)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    print("Database se connection safal raha!")

    # Clear old data
    print("Purana data saaf kiya jaa raha hai...")
    collection.delete_many({})
    print("Collection saaf ho gayi.")

    # Load new data from JSON file
    print("Nayi file se data daala jaa raha hai...")
    with open('knowledge_base.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Insert new data into the collection
    if data and isinstance(data, list):
        result = collection.insert_many(data)
        print(f"Success! {len(result.inserted_ids)} documents database mein daal diye gaye hain.")
    else:
        print("Error: knowledge_base.json file khaali hai ya format galat hai. File mein data [...] list format mein hona chahiye.")

except json.JSONDecodeError:
    print("FATAL ERROR: knowledge_base.json file ka format PURI TARAH GALAT hai. Please check karein.")
except Exception as e:
    print(f"Ek error aa gaya hai: {e}")

finally:
    # Close the connection
    if 'client' in locals():
        client.close()
        print("Connection band kar diya gaya hai.")