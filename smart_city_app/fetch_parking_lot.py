import requests
import json

overpass_query = """
[out:json];
node
  [amenity=parking]
  (around:100000, 53.343792, -6.2546);
out;
"""

encoded_query = requests.utils.quote(overpass_query)

url = f"http://overpass-api.de/api/interpreter?data={encoded_query}"

headers = {'Accept': 'application/json'}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    json_data = response.json()

    # Write the json data to a file
    with open('sensor_data_1.json', 'w') as file:
        json.dump(json_data, file, indent=4)
else:
    print(f"Error: {response.status_code}")
