import math
import Util
import potential as pt
import heuristics as heu

def anytime_potential_search(grid, start, goal, initial_budget, cost_model, h, epsilon, time):
    best_path = None
    best_cost = math.inf
    best_open = None
    best_close = None
    budget = initial_budget

    while budget > 0 and time > 0:
        time -= 1
        path, open_set, closed_set, path_cost = pt.potential_search(grid, start, goal, budget, cost_model, h)

        if path is not None and path_cost < best_cost:
            best_path = path
            best_cost = path_cost
            best_open = open_set
            best_close = closed_set
            budget = path_cost - epsilon 
        else:
            break 

    return best_path, best_open, best_close, best_cost

if __name__ == "__main__":
    width, height = 20, 20
    grid = Util.Gridworld(width, height, 0.3, 10, connectivity=8)

    start = Util.Node((0, 0), None, 0)
    goal = (height - 1, width - 1)
    initial_budget = 200
    time = 500
    e = 10

    while not grid.path_exists(start, goal):
        grid = Util.Gridworld(width, height, 0.3, 10, connectivity=8)

    cost_model = pt.linear  # Using the linear cost model
    best_path, best_open, best_close, best_cost = anytime_potential_search(grid, start, goal, initial_budget, cost_model, heu.heuristic_manhattan, e, time)

    if best_path:
        print("Best Path Found:", best_path)
        print("Path Cost:", best_cost)
        grid.draw_grid(best_path, start.state, goal, best_open, best_close)
    else:
        print("No path found")
        grid.draw_grid(best_path, start.state, goal, best_open, best_close)
