from places.touristic_spots import request_touristic_places
import os
import pandas as pd
import json

countries = ["Portugal","Spain","France","Germany","United Kingdom","Italy","Austria","Netherlands","Switzerland","Greece"]

with open('cities.json', 'r') as f:
    cities_json = json.load(f)

df = None
for country in countries:
    cities = cities_json[country]
    for i,city in enumerate(cities):
        """try:
            df = pd.read_parquet("data/touristic_spots.parquet")
        except:
            df = None"""
        if df is None :
            df = request_touristic_places(country,city)
        else:
            df = df.append(request_touristic_places(country,city))
            df.reset_index(inplace=True,drop=True)
    df.to_parquet("data/touristic_spots.parquet")

df.to_parquet("data/touristic_spots.parquet")