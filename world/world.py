from dsa.graphs.graph import Graph

class World:
    def __init__(self):
        self.map_graph = Graph()
        self.locations = {}
        
    def add_location(self, name, loc_data):
        self.locations[name] = loc_data
        self.map_graph.add_vertex(name)
        
    def connect(self, loc1, loc2, cost):
        self.map_graph.add_edge(loc1, loc2, cost)
