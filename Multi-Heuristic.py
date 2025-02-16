import PQ
import Grid
import math

class Node:
    def __init__(self, state, parent, g_score):
        self.state = state
        self.parent = parent
        self.g_score = g_score

    def __hash__(self):
        return hash(self.state)

    def __eq__(self, other):
        return self.state == other.state

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

def heuristic_chebyshev(node, goal):
    return max(abs(node[0] - goal[0]), abs(node[1] - goal[1]))

def heuristic_octile(node, goal):
    dx = abs(node[0] - goal[0])
    dy = abs(node[1] - goal[1])
    return (dx + dy) + (math.sqrt(2) - 2) * min(dx, dy)

def imha_star(grid, start, goal, heuristics, w1, w2):
    """
    Independent Multi-Heuristic A*
    Each heuristic maintains its own independent search with its own g-values.
    """
    open = [PQ.PQ() for _ in range(len(heuristics))]  # n+1 priority queues
    open_sets = [set([start.state]) for _ in range(len(heuristics))]
    closed_set = [set() for _ in range(len(heuristics))]
    
    for i in range(len(heuristics)):
        open[i].push(start, heuristics[i](start.state, goal) * w1)
    
    while not open[0].isEmpty():
        for i in range(1, len(heuristics)):
            if not open[i].isEmpty() and open[i].peek()[0] <= w2 * open[0].peek()[0]:
                current = open[i].pop()
                open_sets[i].remove(current.state)
                closed_set[i].add(current.state)
                if current.state == goal:
                    return reconstruct_path(current, start, goal), open_sets[i], closed_set[i]
                for neighbor in current.expand_node(grid):
                    g = neighbor.g_score
                    if neighbor.state not in closed_set[i]:
                        h_score = heuristics[i](neighbor.state, goal)
                        f = h_score + g
                        open[i].update((neighbor), f)
                        open_sets[i].add(neighbor.state)
            else:
                current = open[0].pop()
                open_sets[0].remove(current.state)
                closed_set[0].add(current.state)
                if current.state == goal:
                    return reconstruct_path(current, start.state, goal), open_sets[0], closed_set[0]
                for neighbor in current.expand_node(grid):
                    g = neighbor.g_score
                    if neighbor.state not in closed_set[0]:
                        h_score = heuristics[0](neighbor.state, goal)
                        f = h_score + g
                        open[0].update((neighbor), f)
                        open_sets[0].add(neighbor.state)
    
    return None, open_sets[0], closed_set[0]

def smha_star(grid, start, goal, heuristics, w1, w2):
    open = [PQ.PQ() for _ in range(len(heuristics))]  # n+1 priority queues
    open_sets = [set([start.state]) for _ in range(len(heuristics))]
    closed_anchor = set()
    closed_inad = set()
    
    for i in range(len(heuristics)):
        open[i].push(start, heuristics[i](start.state, goal) * w1)
    
    while not open[0].isEmpty():
        for i in range(1, len(heuristics)):
            if not open[i].isEmpty() and open[i].peek()[0] <= w2 * open[0].peek()[0]:
                current = open[i].pop()
                open_sets[i].remove(current.state)
                closed_inad.add(current.state)
                if current.state == goal:
                    return reconstruct_path(current, start, goal), open_sets[i], closed_inad
                for neighbor in current.expand_node(grid):
                    g = neighbor.g_score
                    if neighbor.state not in closed_anchor:
                        h_score = heuristics[i](neighbor.state, goal)
                        f = h_score + g
                        open[0].update((neighbor), f)
                        open_sets[0].add(neighbor.state)
                        if neighbor.state not in closed_inad:
                            for i in range(1, len(heuristics)):
                                open[i].update((neighbor), f)
                                open_sets[i].add(neighbor.state)
            else:
                current = open[0].pop()
                open_sets[0].remove(current.state)
                closed_anchor.add(current.state)
                if current.state == goal:
                    return reconstruct_path(current, start.state, goal), open_sets[0], closed_anchor
                for neighbor in current.expand_node(grid):
                    g = neighbor.g_score
                    if neighbor.state not in closed_anchor:
                        h_score = heuristics[i](neighbor.state, goal)
                        f = h_score + g
                        open[0].update((neighbor), f)
                        open_sets[0].add(neighbor.state)
                        if neighbor.state not in closed_inad:
                            for i in range(1, len(heuristics)):
                                open[i].update((neighbor), f)
                                open_sets[i].add(neighbor.state)
    
    return None, open_sets[0], closed_anchor

def reconstruct_path(current, start, goal):
    """Reconstructs the path from start to goal."""
    path = []
    while current != start:
        path.append(current.state)
        current = current.parent
    path.append(start.state)
    path.reverse()
    return path

def run_search():
    width, height = 20, 20
    start = Node((0, 0), None, 0)
    grid = Grid.Gridworld(width, height, 0.3, 10, connectivity=8)
    goal = (height - 1, width - 1)
    heuristics = [heuristic_manhattan, heuristic_euclidean, heuristic_chebyshev, heuristic_octile]

    while not grid.path_exists(start, goal):
        grid = Grid.Gridworld(width, height, 0.3, 10, connectivity=8)
    
    path, open_set, closed_set = smha_star(grid, start, goal, heuristics, 3, 3)
    if path:
        print("Path found:", path)
        grid.draw_grid(path=path, start=start.state, goal=goal, open_list=open_set, closed_list=closed_set)
    else:
        print("No path found")
        grid.draw_grid(path=path, start=start.state, goal=goal, open_list=open_set, closed_list=closed_set)

if __name__ == "__main__":
    run_search()
