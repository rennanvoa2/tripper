import pandas as pd

def gen_dist_matrix(df, client,mode="walking"):
    # Cria um dicionário para armazenar as distâncias
    distances = {}

    # Itera sobre cada lugar
    for i, row in df.iterrows():
        origem = (row['lat'], row['lng'])
        distances[row['place_names']] = {}
        # Itera novamente sobre cada lugar
        for j, row2 in df.iterrows():
            destino = (row2['lat'], row2['lng'])
            # Chama a API Directions do Google Maps para obter a distância em metros
            directions_result = client.directions(origem, destino, mode=mode) 
            if len(directions_result) > 0:
                distance = directions_result[0]['legs'][0]['distance']['value']
                distances[row['place_names']][str(row2['id'])] = distance
    # Cria um dataframe com as distâncias
    distances_df = pd.DataFrame(distances)
    distances_df.columns = distances_df.index
    return distances_df
