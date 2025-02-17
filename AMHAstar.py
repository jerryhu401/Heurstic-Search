import math
import Util
import MultiHeuristic as MH
import heuristics as heu

def update_weight(weight):
    w1, w2 = weight
    return (max(w1 - 2, 1), max(w2 - 2, 1))

def valid_weight(weight):
    w1, w2 = weight
    return w1 >=1 and w2 >= 1

def anytime(grid, start, goal, h, weight, update, valid, time):
    best_path = None
    best_cost = math.inf
    best_open = None
    best_close = None

    while valid(weight) and time > 0:
        time -= 1
        path, open_set, closed_set, path_cost = MH.smha_star(grid, start, goal, h, weight)

        if path is not None:
            if path_cost < best_cost:
                best_path = path
                best_cost = path_cost
                best_open = open_set
                best_close = closed_set
            weight = update(weight)
        else:
            break 

    return best_path, best_open, best_close, best_cost

if __name__ == "__main__":
    width, height = 20, 20
    grid = Util.Gridworld(width, height, 0.3, 10, connectivity=8)

    start = Util.Node((0, 0), None, 0)
    goal = (height - 1, width - 1)
    weight = (10, 10)
    h = [heu.heuristic_manhattan, heu.heuristic_euclidean, heu.heuristic_chebyshev, heu.heuristic_octile]
    time = 10

    while not grid.path_exists(start, goal):
        grid = Util.Gridworld(width, height, 0.3, 10, connectivity=8)

    best_path, best_open, best_close, best_cost = anytime(grid, start, goal, h, weight, update_weight, valid_weight, time)

    if best_path:
        print("Best Path Found:", best_path)
        print("Path Cost:", best_cost)
        grid.draw_grid(best_path, start.state, goal, best_open, best_close)
    else:
        print("No path found")
        grid.draw_grid(best_path, start.state, goal, best_open, best_close)
