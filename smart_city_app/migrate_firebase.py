import firebase_admin
from firebase_admin import credentials, firestore
import json
import random

cred = credentials.Certificate('../../serviceAccountKey.json')  # Replace with your Firebase service account path with the config path
firebase_admin.initialize_app(cred)

# Firestore database reference
db = firestore.client()
collection_name = 'smart-parking-lot'

parking_json_file_path = 'sensor_data.json'

with open(parking_json_file_path, 'r') as f:
    json_data = json.load(f)

def upload_data(data):
    for item in data:
        doc_id = str(item["id"])  
        lat = item["lat"]
        lon = item["lon"]
        
        # Extract 'name' from tags, or set default name
        name = item["tags"].get("name", "Unidentified Parking Lot")
        
        # Extract 'capacity' from tags, default to a random number if not found
        capacity = item["tags"].get("capacity", str(random.randint(100, 200)))
        
        # Create the data dictionary for Firestore
        doc_data = {
            "lat": lat,
            "lon": lon,
            "name": name,
            "capacity": capacity
          }
        
        # Upload to Firestore
        db.collection(collection_name).document(doc_id).set(doc_data)
        print(f"Uploaded document ID: {doc_id}")


upload_data(json_data)