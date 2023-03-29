import googlemaps
import numpy as np


class GMapsRoutes:
    def __init__(self) -> None:
        pass

    def response_to_matrix(self,response):
        """
        Converts the response from the Maps API to a distance matrix.
    
        Args:
        - response: A dictionary representing the response from the Maps API.
        
        Returns:
        - A NumPy array representing the distance matrix.
        """
        n = len(response['destination_addresses'])
        matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                if i == j:
                    matrix[i][j] = 0
                elif response['rows'][i]['elements'][j]['status'] == 'OK':
                    matrix[i][j] = response['rows'][i]['elements'][j]['distance']['value']
                else:
                    matrix[i][j] = np.inf
        return matrix

    def get_distance_matrix(self,list_of_places,mode="walking"):
        gmaps = googlemaps.Client(key='AIzaSyDV93ChQ2_YJYGaLKy1elcyexcVj7ggzK4')

        # Obter a matriz de distância entre os lugares
        matrix = gmaps.distance_matrix(list_of_places, list_of_places, mode=mode)

        #generate the distance matrix
        distance_matrix = self.response_to_matrix(matrix)

        return distance_matrix



