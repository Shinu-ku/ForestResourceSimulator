from dsa.graphs.graph import Graph
from dsa.graphs.dijkstra import dijkstra
from dsa.graphs.bfs import bfs_path
from dsa.graphs.dfs import dfs_path
from world.locations import LOCATIONS, EDGES

class World:
    def __init__(self):
        self.locations = LOCATIONS
        self.graph = Graph()
        
        # Populate graph
        for loc_name in self.locations:
            self.graph.add_vertex(loc_name)
            
        for u, v, cost in EDGES:
            self.graph.add_edge(u, v, cost)

    def get_location_data(self, name):
        return self.locations.get(name)

    def get_neighbors(self, name):
        return self.graph.get_neighbors(name)

    def find_route(self, start, end, algorithm="dijkstra"):
        """
        Finds a route between start and end using the specified algorithm:
        'dijkstra' (Shortest cost), 'bfs' (Fewest hops), or 'dfs' (Exploratory).
        Returns dict with: path, total_cost, distance, algorithm.
        """
        if start not in self.locations or end not in self.locations:
            return {"path": [], "total_cost": 0, "distance": 0, "algorithm": algorithm}
            
        if algorithm == "dijkstra":
            path, cost = dijkstra(self.graph, start, end)
        elif algorithm == "bfs":
            path, cost = bfs_path(self.graph, start, end)
        elif algorithm == "dfs":
            path, cost = dfs_path(self.graph, start, end)
        else:
            path, cost = dijkstra(self.graph, start, end)
            
        return {
            "path": path,
            "total_cost": cost,
            "distance": len(path),
            "algorithm": algorithm
        }
