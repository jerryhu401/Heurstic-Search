import Util
import math
import heuristics as heu

def imha_star(grid, start, goal, heuristics, weights):
    w1, w2 = weights
    open = [Util.PQ() for _ in range(len(heuristics))]  # n+1 priority queues
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
                        h_score = w1*heuristics[i](neighbor.state, goal)
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
                        h_score = w1*heuristics[0](neighbor.state, goal)
                        f = h_score + g
                        open[0].update((neighbor), f)
                        open_sets[0].add(neighbor.state)
    
    return None, open_sets[0], closed_set[0]

def smha_star(grid, start, goal, heuristics, weights):
    w1, w2 = weights
    open = [Util.PQ() for _ in range(len(heuristics))]  # n+1 priority queues
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
                        h_score = w1*heuristics[i](neighbor.state, goal)
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
                        h_score = w1*heuristics[i](neighbor.state, goal)
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
    start = Util.Node((0, 0), None, 0)
    grid = Util.Gridworld(width, height, 0.3, 10, connectivity=8)
    goal = (height - 1, width - 1)
    heuristics = [heu.heuristic_manhattan, heu.heuristic_euclidean, heu.heuristic_chebyshev, heu.heuristic_octile]

    while not grid.path_exists(start, goal):
        grid = Util.Gridworld(width, height, 0.3, 10, connectivity=8)
    
    weights = (3,3)
    path, open_set, closed_set = smha_star(grid, start, goal, heuristics, weights)
    if path:
        print("Path found:", path)
        grid.draw_grid(path=path, start=start.state, goal=goal, open_list=open_set, closed_list=closed_set)
    else:
        print("No path found")
        grid.draw_grid(path=path, start=start.state, goal=goal, open_list=open_set, closed_list=closed_set)

if __name__ == "__main__":
    run_search()
