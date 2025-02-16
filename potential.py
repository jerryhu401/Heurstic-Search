import Util
import math
import heuristics as heu

def linear(C, h_n, g_n):
    if h_n == 0:
        return 0
    if ((C - g_n) <= 0):
        return math.inf
    return h_n/(C - g_n)

def additive(C, h_n, g_n):
    return h_n + g_n

def potential_search(grid, start, goal, budget, cost_model, h):
    """
    Potential Search with support for different cost models: additive, linear relative, and general invertible.
    """
    open_list = Util.PQ()
    open_list.push((start), 0)
    open_set = {start.state}
    closed_set = set()
    final_cost = None

    while not open_list.isEmpty():
        current_node = open_list.pop()
        open_set.remove(current_node.state)
        closed_set.add(current_node.state)

        if current_node.state == goal:
            path = []
            final_cost = current_node.g_score
            while current_node != start:
                path.append(current_node.state)
                current_node = current_node.parent
            path.append(start.state)
            path.reverse()
            return path, open_set, closed_set, final_cost

        for neighbor in current_node.expand_node(grid):
            g_score = neighbor.g_score

            if neighbor.state not in closed_set and neighbor.g_score <= budget:
                h_score = h(neighbor.state, goal)
                potential = cost_model(budget, h_score, g_score)
                open_list.update((neighbor), potential)
                open_set.add(neighbor.state)

    return None, open_set, closed_set, None


if __name__ == "__main__":
    width, height = 20, 20
    grid = Util.Gridworld(width, height, 0.3, 10, connectivity=8)

    start = Util.Node((0, 0),None,0)
    goal = (height - 1, width - 1)
    budget = 80

    while not grid.path_exists(start, goal):
        grid = Util.Gridworld(width, height, 0.3, 10, connectivity=8)

    cost_model = "linear_relative" 
    path, open_set, closed_set, C = potential_search(grid, start, goal, budget, linear, heu.heuristic_manhattan)

    if path:
        print(f"Path found with cost {C}:", path)
        grid.draw_grid(path=path, start=start.state, goal=goal, open_list=open_set, closed_list=closed_set)
    else:
        print("No path found")
        grid.draw_grid(path=path, start=start.state, goal=goal, open_list=open_set, closed_list=closed_set)
