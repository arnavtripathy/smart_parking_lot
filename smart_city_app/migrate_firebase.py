import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('../../serviceAccountKey.json')  # Replace with your Firebase service account path with the config path
firebase_admin.initialize_app(cred)

# Firestore database reference
db = firestore.client()
collection_name = 'smart-parking-lot'

# Sample JSON data
json_data = [
    {
        "type": "node",
        "id": 111887569,
        "lat": 53.3487574,
        "lon": -6.2420851,
        "tags": {
            "amenity": "parking",
            "capacity": "104",
            "layer": "-1",
            "parking": "underground"
        }
    },
    {
        "type": "node",
        "id": 111929646,
        "lat": 53.3485887,
        "lon": -6.2461854,
        "tags": {
            "access": "yes",
            "amenity": "parking",
            "capacity": "370",
            "fee": "yes",
            "name": "IFSC Car Park",
            "parking": "multi-storey"
        }
    },
    {
        "type": "node",
        "id": 133459155,
        "lat": 53.3493115,
        "lon": -6.2558171,
        "tags": {
            "amenity": "parking",
            "fee": "yes",
            "layer": "-1",
            "name": "Irish Life Car Park",
            "parking": "underground"
        }
    }
]

def upload_data(data):
    for item in data:
        doc_id = str(item["id"])  
        lat = item["lat"]
        lon = item["lon"]
        
        # Extract 'name' from tags, or set default name
        name = item["tags"].get("name", "Unidentified Parking Lot")
        
        # Extract 'capacity' from tags, default to None if not found
        capacity = item["tags"].get("capacity")
        
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