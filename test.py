from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import requests
import pandas as pd

ids_df = pd.read_parquet("data/touristic_spots.parquet")
city = "Porto"
country = "Portugal"
url = "http://127.0.0.1:8080/trace_route"
place_ids = ids_df.loc[(ids_df.city == city) & (ids_df.country == country)][:10].id.to_list()
j = {
    "city":city,
    "country":country,
    "place_ids":place_ids
}
place_ids = [str(i) for i in place_ids]
distance_matrix = pd.read_parquet(f"data/distance_matrices/walking/{country}/{city}.parquet")

class TSPSolver:
    def __init__(self, distance_matrix,places):
        self.distance_matrix = distance_matrix
        self.num_vehicles = 1
        self.depot = 0
        self.places = places

    def solve(self,max_time=3):
        """Solve the TSP problem and return the solution."""
        # Create the routing index manager.
        manager = pywrapcp.RoutingIndexManager(len(self.distance_matrix),
                                               self.num_vehicles, self.depot)

        # Create Routing Model.
        routing = pywrapcp.RoutingModel(manager)

        # Create and register a transit callback.
        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return self.distance_matrix.iloc[from_node,to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        # Define cost of each arc.
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Set the solver parameters.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
        search_parameters.time_limit.seconds = max_time

        # Solve the problem.
        solution = routing.SolveWithParameters(search_parameters)

        # Return the solution.
        if solution:
            return self._get_solution(manager, routing, solution,self.places)

    @staticmethod
    def _get_solution(manager, routing, solution,places):
        """Return the solution as a dictionary."""
        index = routing.Start(0)
        route = [manager.IndexToNode(index)]
        distance = 0
        while not routing.IsEnd(index):
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route.append(manager.IndexToNode(index))
            distance += routing.GetArcCostForVehicle(previous_index, index, 0)
        return {
            "route_names": [places[i] for i in route],
            "route_indexes":route,
            "distance": distance
        }
    
solver = TSPSolver(distance_matrix.loc[place_ids, place_ids],place_ids)
rs =solver.solve(max_time=10)
print(rs)