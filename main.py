from flask import Flask, jsonify, request, render_template
from routes.ortools_tsp import TSPSolver
from routes.multiple_tsp_solver import TSPMultipleRoutesSolver
import math
from gmaps.distances import GMapsRoutes
import pandas as pd

app = Flask(__name__)
route_generator = GMapsRoutes()
ids_df = pd.read_parquet("data/touristic_spots.parquet")

@app.route('/trace_route', methods=["POST"])
def trace_route():
    json_data = request.json

    if "place_ids" not in json_data:
        return "place_ids must be in the json",400
    else:
        place_ids = json_data["place_ids"]
        place_ids = [str(i) for i in place_ids]

    if "country" not in json_data:
        return "country must be in the json",400
    else:
        country = json_data["country"]

    if "city" not in json_data:
        return "city must be in the json",400
    else:
        city = json_data["city"]

    distance_matrix = pd.read_parquet(f"data/distance_matrices/walking/{country}/{city}.parquet")

    distance_filtered = distance_matrix.loc[place_ids, place_ids]


    nr_of_routes = json_data["nr_of_routes"] if "nr_of_routes" in json_data else 1
    max_total_time = json_data["max_total_time"] if "max_total_time" in json_data else 10

    #Divide the total time per number of subroutes that it has to calculate
    time_per_run = math.floor(max_total_time/nr_of_routes)
   

    #matrix = route_generator.get_distance_matrix(places)

    if nr_of_routes > 1:
        multi_tsp = TSPMultipleRoutesSolver(distance_filtered,place_ids)
        rs = multi_tsp.solve(route_numbers=nr_of_routes,max_time=time_per_run)
        return jsonify(rs)

    else:
        tsp_solver = TSPSolver(distance_filtered,place_ids) 
        routes = [tsp_solver.solve(max_time=time_per_run)]

    return jsonify(routes)

@app.route('/')
def index():
  return "Ok",200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True, use_reloader=True)