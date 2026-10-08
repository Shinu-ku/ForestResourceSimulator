class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_vertex(self, vertex):
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = {}

    def add_edge(self, u, v, weight=1, bidirectional=True):
        self.add_vertex(u)
        self.add_vertex(v)
        self.adjacency_list[u][v] = weight
        if bidirectional:
            self.adjacency_list[v][u] = weight

    def get_neighbors(self, vertex):
        return self.adjacency_list.get(vertex, {})
