import numpy as np
from functools import lru_cache
from app.schemas.graph import Graph, PathResult
from typing import Optional, Tuple

def solve_tsp(graph: Graph) -> PathResult:
    nodes = graph.nodes
    edges = graph.edges
    size = len(nodes)

    for edge in edges:
        if len(edge) != 3 or edge[0] not in nodes or edge[1] not in nodes:
            raise ValueError(f"Invalid edge {edge}: nodes must be in {nodes}")

    node_index = {node: idx for idx, node in enumerate(nodes)}

    distance_matrix = np.full((size, size), float('inf'))
    np.fill_diagonal(distance_matrix, 0)  # расстояние до самого себя = 0

    for u, v, w in edges:
        i, j = node_index[u], node_index[v]
        distance_matrix[i][j] = w
        distance_matrix[j][i] = w

    all_seen = (1 << size) - 1

    @lru_cache(None)
    def explore(place: int, seen: int) -> float:
        if seen == all_seen:
            dist_to_origin = distance_matrix[place][0]
            return float(dist_to_origin) if dist_to_origin != float('inf') else float('inf')

        lowest_cost = float('inf')
        for next_place in range(size):
            if not (seen & (1 << next_place)):
                edge_cost = distance_matrix[place][next_place]
                if edge_cost != float('inf'):
                    total = edge_cost + explore(next_place, seen | (1 << next_place))
                    lowest_cost = min(lowest_cost, total)
        return float(lowest_cost)

    def trace_route() -> Tuple[Optional[float], list[int]]:
        marked = 1 << 0
        route = [0]
        total_weight = 0.0
        while len(route) < size:
            min_weight = float('inf')
            next_stop = None
            current = route[-1]
            for candidate in range(size):
                if not (marked & (1 << candidate)):
                    weight = distance_matrix[current][candidate]
                    if weight != float('inf') and weight < min_weight:
                        min_weight = weight
                        next_stop = candidate

            if next_stop is None:
                return None, []

            route.append(next_stop)
            total_weight += float(min_weight)
            marked |= 1 << next_stop

        if distance_matrix[route[-1]][0] != float('inf'):
            total_weight += float(distance_matrix[route[-1]][0])
            route_nodes = [nodes[idx] for idx in route]
            return float(total_weight), route_nodes

        return None, []

    cost = explore(0, 1 << 0)
    final_cost, path = trace_route()

    return PathResult(path=path if path else [], total_distance=final_cost)
