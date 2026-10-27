from collections import deque

def bfs_path(graph, start, end):
    """
    Finds the shortest path between start and end in terms of number of hops (edges).
    Returns (path, total_cost).
    """
    if start == end:
        return [start], 0
        
    queue = deque([[start]])
    visited = {start}
    
    while queue:
        path = queue.popleft()
        current = path[-1]
        
        if current == end:
            # Calculate total edge cost for this path
            total_cost = 0
            for i in range(len(path) - 1):
                neighbors = graph.get_neighbors(path[i])
                total_cost += neighbors.get(path[i + 1], 1)
            return path, total_cost
            
        for neighbor, _ in graph.get_neighbors(current).items():
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])
                
    return [], -1
