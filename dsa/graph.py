from collections import deque


class Graph:
    """Adjacency-list graph with BFS traversal."""

    def __init__(self):
        self.adjacency = {}

    def add_vertex(self, vertex):
        if vertex not in self.adjacency:
            self.adjacency[vertex] = []

    def add_edge(self, first, second):
        self.add_vertex(first)
        self.add_vertex(second)
        self.adjacency[first].append(second)
        self.adjacency[second].append(first)

    def bfs(self, start):
        if start not in self.adjacency:
            return []

        visited = set([start])
        queue = deque([start])
        order = []

        while queue:
            current = queue.popleft()
            order.append(current)

            for neighbor in self.adjacency[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return order
