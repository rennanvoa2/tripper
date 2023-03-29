import requests
import json
import pandas as pd

URL = 'https://maps.googleapis.com/maps/api/place/textsearch/json'

def request_touristic_places(country,city):
    #Before running the code set the key as GMAPS_KEY env varible
    params = {'query': f'tourist spots in {city} - {country}', 'key': "AIzaSyDV93ChQ2_YJYGaLKy1elcyexcVj7ggzK4"}
    
    # Make a request to the Places API
    response = requests.get(URL, params=params)

    # Parse the JSON response
    data = json.loads(response.text)
    results = data['results']
    response = {}
    for result in results:
        name = result['name']
        address = result['formatted_address']

        try:
            lat = result['geometry']['location']['lat']
        except:
            lat = None

        try:
            lng = result['geometry']['location']['lng']
        except:
            lng = None

        try:
            photos = [photo['photo_reference'] for photo in result["photos"] if len(photo) > 0]
        except:
            photos = []

        response.update({name:{
            "address":address,
            "lat":lat,
            "lng":lng,
            "photo_references":photos
                              }})
        
    df = pd.DataFrame.from_dict(response, orient='index')
    df = df.reset_index()
    df.columns = ["place_names","address","lat","lng","photo_references"]
    df.insert(0,"country",country)
    df.insert(0,"city",city)

    return df


