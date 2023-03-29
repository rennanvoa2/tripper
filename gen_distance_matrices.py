import pandas as pd
from places.distance_matrix import gen_dist_matrix
import googlemaps
import os 

# Define a chave da API do Google Cloud Platform
client = googlemaps.Client(key='AIzaSyDV93ChQ2_YJYGaLKy1elcyexcVj7ggzK4')
df = pd.read_parquet("data/touristic_spots.parquet")

# Salva o dataframe em um arquivo Parquet
#distances_df.to_parquet('distances.parquet')

for country in df.country.unique():
    temp_df = df.loc[df.country == country]
    temp_df.reset_index(inplace=True,drop=True)
    for i,city in enumerate(temp_df.city.unique()):
        print(country,city)
        try:
            if not os.path.isfile(f"/Users/rennanaraujo/routing_app/data/distance_matrices/walking/{country}/{city}.parquet"):
                city_df = temp_df.loc[temp_df.city == city]
                city_df.reset_index(inplace=True,drop=True)
                distances_df = gen_dist_matrix(city_df,client,mode="walking")
                directory = os.path.dirname(f"/Users/rennanaraujo/routing_app/data/distance_matrices/walking/{country}/")
                if not os.path.exists(directory):
                    os.makedirs(directory)
                distances_df.to_parquet(f"/Users/rennanaraujo/routing_app/data/distance_matrices/walking/{country}/{city}.parquet")
        except:
            pass
for country in df.country.unique():
    temp_df = df.loc[df.country == country]
    temp_df.reset_index(inplace=True,drop=True)
    for i,city in enumerate(temp_df.city.unique()):
        print(country,city)
        
        try:
            if not os.path.isfile(f"/Users/rennanaraujo/routing_app/data/distance_matrices/transit/{country}/{city}.parquet"):
                city_df = temp_df.loc[temp_df.city == city]
                city_df.reset_index(inplace=True,drop=True)
                distances_df = gen_dist_matrix(city_df,client,mode="transit")
                directory = os.path.dirname(f"/Users/rennanaraujo/routing_app/data/distance_matrices/transit/{country}/")
                if not os.path.exists(directory):
                    os.makedirs(directory)
                distances_df.to_parquet(f"/Users/rennanaraujo/routing_app/data/distance_matrices/transit/{country}/{city}.parquet")
        except:
            pass