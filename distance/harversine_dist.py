import math

def calculate_haversine(lat1, lon1, lat2, lon2):
    r = 6371 # raio médio da Terra em km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat / 2)**2 + \
        math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * \
        math.sin(d_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c * 1000 # retorna a distância em metros

# Exemplo de uso
lat1 = -22.951389
lon1 = -43.210833
lat2 = -23.550520
lon2 = -46.633309
dist = calculate_haversine(lat1, lon1, lat2, lon2)
print(f"A distância entre os pontos é {dist:.2f} metros.")
