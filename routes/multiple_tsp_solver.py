import numpy as np
from sklearn.cluster import KMeans
from routes.ortools_tsp import TSPSolver
import pandas as pd

class TSPMultipleRoutesSolver:
    def __init__(self, distance_matrix, places):
        self.distance_matrix = distance_matrix
        self.places = places

    def solve(self, route_numbers=2, max_time=3):
        # Use K-Means clustering to split the distance matrix.
        kmeans = KMeans(n_clusters=route_numbers, random_state=0)
        cluster_rows = kmeans.fit_predict(self.distance_matrix)
        cluster_cols = kmeans.fit_predict(self.distance_matrix.transpose())

        # Create a list of sub-matrices.
        sub_matrices = []
        sub_names = []
        for i in range(route_numbers):
            rows_indices = np.where(cluster_rows == i)[0]
            rows_names = self.distance_matrix.index[rows_indices]
            print(rows_names)
            sub_names.append(rows_names)
            cols_indices = np.where(cluster_cols == i)[0]
            sub_matrix = self.distance_matrix.iloc[rows_indices, cols_indices]
            sub_matrices.append(sub_matrix)

        # Create a TSP solver for each sub-matrix.
        solvers = [TSPSolver(sub_matrix, sub_names[i]) for i,sub_matrix in enumerate(sub_matrices)]

        # Solve each TSP problem.
        routes = []
        for solver in solvers:
            solution = solver.solve(max_time=max_time)
            routes.append(solution)

        # Combine the routes into a single solution.
        """solution = {"route_names": [], "route_indexes": [], "distance": 0}
        for route in routes:
            solution["route_names"] += [self.places[i] for i in route[1:]]
            solution["route_indexes"] += route[1:]
            solution["distance"] += sum(self.distance_matrix.iloc[route[i], route[i+1]] for i in range(len(route)-1))

        # Add the starting point to the solution.
        solution["route_names"] = [self.places[0]] + solution["route_names"]
        solution["route_indexes"] = [0] + solution["route_indexes"]"""

        return routes