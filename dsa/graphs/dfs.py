def dfs_path(graph, start, end, visited=None):
    """
    Finds an exploratory path between start and end using Depth-First Search.
    Returns (path, total_cost).
    """
    if visited is None:
        visited = set()
        
    if start == end:
        return [start], 0
        
    visited.add(start)
    
    for neighbor, weight in graph.get_neighbors(start).items():
        if neighbor not in visited:
            sub_path, sub_cost = dfs_path(graph, neighbor, end, visited)
            if sub_path:
                return [start] + sub_path, weight + sub_cost
                
    return [], -1
