import Grid
import math
import PQ

class Node:
    def __init__(self, state, parent, g_score):
        self.state = state
        self.parent = parent
        self.g_score = g_score

    def __hash__(self):
        return hash(self.state)

    def __eq__(self, other):
        return self.state == other.state

    def __ne__(self, other):
        return self.state != other.state
    
    def expand_node(self, grid):
        x, y = self.state
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        if grid.connectivity == 8:
            directions.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)]) 

        result = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if grid.is_traversable(nx, ny):
                result.append(Node((nx, ny), self, self.g_score + grid.grid[x][y]))

        return result

def heuristic_manhattan(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def heuristic_euclidean(node, goal):
    return ((node[0] - goal[0]) ** 2 + (node[1] - goal[1]) ** 2) ** 0.5

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
    open_list = PQ.PQ()
    open_list.push((start), 0)
    open_set = {start.state}
    closed_set = set()

    while not open_list.isEmpty():
        current_node = open_list.pop()
        open_set.remove(current_node.state)
        closed_set.add(current_node.state)

        if current_node.state == goal:
            path = []
            while current_node != start:
                path.append(current_node.state)
                current_node = current_node.parent
            path.append(start.state)
            path.reverse()
            return path, open_set, closed_set

        for neighbor in current_node.expand_node(grid):
            g_score = neighbor.g_score

            if neighbor.state not in closed_set:
                h_score = h(neighbor.state, goal)
                potential = cost_model(budget, h_score, g_score)
                open_list.update((neighbor), potential)
                open_set.add(neighbor.state)

    return None, open_set, closed_set  # No path found


if __name__ == "__main__":
    width, height = 20, 20
    grid = Grid.Gridworld(width, height, 0.3, 10, connectivity=8)

    start = Node((0, 0),None,0)
    goal = (height - 1, width - 1)
    budget = 80

    while not grid.path_exists(start, goal):
        grid = Grid.Gridworld(width, height, 0.3, 10, connectivity=8)

    cost_model = "linear_relative" 
    path, open_set, closed_set = potential_search(grid, start, goal, budget, linear, heuristic_manhattan)

    if path:
        print("Path found:", path)
        grid.draw_grid(path=path, start=start.state, goal=goal, open_list=open_set, closed_list=closed_set)
    else:
        print("No path found")
        grid.draw_grid(path=path, start=start.state, goal=goal, open_list=open_set, closed_list=closed_set)
