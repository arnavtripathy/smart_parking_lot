# Dublin Smart Parking lot Concept App 

Smart Parking lot app for Urban computing subject - Msc Trinity college Dublin

Written in Django and map generated using Leaflet.js.

Parking lot data is stored in Firebase.

## Parking lot Visualisation

Below is a screenshot of the parking lot visualisation for the app:

<img width="1219" alt="Screenshot 2024-11-28 021102" src="https://github.com/user-attachments/assets/f591a96b-9500-4ffc-92c5-f0707f034987">

The goal of this visualisation was to fetch parking lots available as per user’s choice. The browser takes the current location of the user. Once the user inputs the radius value in meters (1000 in above example) , it displays the parking lots available in that radius.


Internally, the page calls overpass-turbo api and fetches the details. The map is generated using leaflet.js. The user can use the “Take me” option to find navigation to the parking lot. If the user chooses the “Book spot”, the user can attempt to book the spot. 

## Additional Tasks

- User Registration and Login to keep track of user details using the Parking lot.
<img width="1205" alt="Screenshot 2024-12-07 132526" src="https://github.com/user-attachments/assets/887686a5-0c51-4934-93a1-77b7cba151a6">


- Real time change in numbers of the parking  lot. The numbers change as more users book a parking lot.
<img width="404" alt="Screenshot 2024-11-28 022956" src="https://github.com/user-attachments/assets/72062516-aa44-4491-9f6a-907364a68149">

- Option to navigate is given to the user when they select the “Take me” option:
<img width="1183" alt="Screenshot 2024-11-28 023119" src="https://github.com/user-attachments/assets/61301b75-fc7b-4187-b6ad-2bfaf4ee783c">

- PDF generation of a ticket with details and a QR code is created so that user can present the ticket at the parking lot:
<img width="615" alt="Screenshot 2024-11-28 023309" src="https://github.com/user-attachments/assets/adb24951-5474-42d7-ac53-bcd296d5f00e">


The motivation behind these features was to replicate the closest working model of a parking lot booking system as real as possible. We could have added more features to make it more realistic, however, due to time constraints, we were unable to add.

## Instructions to run code:

Steps to follow:
- Clone the repo : `git clone https://github.com/arnavtripathy/smart_parking_lot` 
- Once cloned , please generate a firebase key and fix path as mentioned here `https://github.com/arnavtripathy/smart_parking_lot/blob/master/smart_city_app/settings.py#L18C1-L18C63`
- Create a python virtual environment with below commands `python3 -m venv venv`
- Activate the environment `source venv/bin/activate`
- Install packages `pip3 install -r requirements.txt`
- Once created, please run below command to start server : `python3 manage.py runserver`

The server will be running on localhost:8000
