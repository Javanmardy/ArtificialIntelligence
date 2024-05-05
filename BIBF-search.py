import heapq

cities = {
    "Arad": {"Zerind": 75, "Timisoara": 118, "Sibiu": 140},
    "Zerind": {"Arad": 75, "Oradea": 71},
    "Timisoara": {"Arad": 118, "Lugoj": 111},
    "Sibiu": {"Arad": 140, "Oradea": 151, "Fagaras": 99, "Rimnicu Vilcea": 80},
    "Oradea": {"Zerind": 71, "Sibiu": 151},
    "Lugoj": {"Timisoara": 111, "Mehadia": 70},
    "Mehadia": {"Lugoj": 70, "Drobeta": 75},
    "Drobeta": {"Mehadia": 75, "Craiova": 120},
    "Craiova": {"Drobeta": 120, "Rimnicu Vilcea": 146, "Pitesti": 138},
    "Rimnicu Vilcea": {"Sibiu": 80, "Craiova": 146, "Pitesti": 97},
    "Fagaras": {"Sibiu": 99, "Bucharest": 211},
    "Pitesti": {"Rimnicu Vilcea": 97, "Craiova": 138, "Bucharest": 101},
    "Giurgiu": {"Bucharest": 90},
    "Bucharest": {"Fagaras": 211, "Pitesti": 101, "Giurgiu": 90},
}

heuristic = {
    "Arad": 366,
    "Zerind": 374,
    "Timisoara": 329,
    "Sibiu": 253,
    "Oradea": 380,
    "Lugoj": 244,
    "Mehadia": 241,
    "Drobeta": 242,
    "Craiova": 160,
    "Rimnicu Vilcea": 193,
    "Fagaras": 176,
    "Pitesti": 100,
    "Bucharest": 0,
    "Giurgiu": 77,
}


def bidirectional(graph, start, goal, heuristics):
    def reconstruct(meeting_point, start_parents, goal_parents):
        path = []
        node = meeting_point
        while node != start:
            path.append(node)
            node = start_parents[node]
        path.append(start)
        path.reverse()

        node = meeting_point
        while node != goal:
            node = goal_parents[node]
            path.append(node)

        return path

    def star_search(
        queue,
        visited,
        costs,
        parents,
        end,
        other_visited,
        other_parents,
        search_direction,
    ):
        if queue:
            current_cost, current_node = heapq.heappop(queue)
            print(
                f"Expanding node {current_node} in {search_direction} search with current cost {current_cost}"
            )
            if current_node in other_visited:
                print(f"Meeting point found at {current_node}")
                return (
                    current_node,
                    costs[current_node] + other_visited[current_node],
                    parents,
                    other_parents,
                )

            for neighbor, distance in graph[current_node].items():
                new_cost = costs[current_node] + distance
                if neighbor not in visited or new_cost < visited[neighbor]:
                    visited[neighbor] = new_cost
                    parents[neighbor] = current_node
                    f_score = new_cost + heuristics[neighbor]
                    heapq.heappush(queue, (f_score, neighbor))
                    costs[neighbor] = new_cost
                    print(
                        f"Added/Updated node {neighbor} in {search_direction} search with f-score {f_score}"
                    )
        return None, float("inf"), parents, other_parents

    forward_queue = [(heuristics[start], start)]
    backward_queue = [(heuristics[goal], goal)]
    forward_visited = {start: 0}
    backward_visited = {goal: 0}
    forward_costs = {start: 0}
    backward_costs = {goal: 0}
    forward_parents = {start: None}
    backward_parents = {goal: None}

    while forward_queue and backward_queue:
        result, cost, forward_parents, backward_parents = star_search(
            forward_queue,
            forward_visited,
            forward_costs,
            forward_parents,
            goal,
            backward_visited,
            backward_parents,
            "forward",
        )
        if result:
            return reconstruct(result, forward_parents, backward_parents), cost
        result, cost, backward_parents, forward_parents = star_search(
            backward_queue,
            backward_visited,
            backward_costs,
            backward_parents,
            start,
            forward_visited,
            forward_parents,
            "backward",
        )
        if result:
            return reconstruct(result, forward_parents, backward_parents), cost

    return None, float("inf")


result, path_cost = bidirectional(cities, "Arad", "Bucharest", heuristic)
print(f"Path found: {result} with cost: {path_cost}")
