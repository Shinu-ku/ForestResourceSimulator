import heapq

def dijkstra(graph, start, end):
    distances = {vertex: float('infinity') for vertex in graph.adjacency_list}
    distances[start] = 0
    priority_queue = [(0, start)]
    previous_nodes = {vertex: None for vertex in graph.adjacency_list}

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_distance > distances[current_vertex]:
            continue
            
        if current_vertex == end:
            break

        for neighbor, weight in graph.get_neighbors(current_vertex).items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))

    path, current = [], end
    while previous_nodes[current] is not None:
        path.insert(0, current)
        current = previous_nodes[current]
    if path:
        path.insert(0, current)
        
    return path, distances[end] if distances[end] != float('infinity') else -1
