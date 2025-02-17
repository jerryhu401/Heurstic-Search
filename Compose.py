import math
import Util
import MultiHeuristic as MH
import heuristics as heu

def heuristic_search_single(grid, start, goal, priority, weights):
    w1, w2, budget = weights
    open = Util.PQ()
    open_set = set([start.state])
    closed_anchor = set()
    open.push((start), priority(start.state, goal, start.g_score, (w1, budget)))
    
    while not open.isEmpty():
        current = open.pop()
        open_set.remove(current.state)
        closed_anchor.add(current.state)
        if current.state == goal:
            return reconstruct_path(current, start, goal), open_set, closed_anchor, current.g_score
        for neighbor in current.expand_node(grid):
            g = neighbor.g_score
            if neighbor.state not in closed_anchor:
                f = priority(neighbor.state, goal, g, (w1,budget))
                open.update((neighbor), f)
                open_set.add(neighbor.state)
    
    return None, open_set, closed_anchor, None

def heuristic_search_multi(grid, start, goal, priorities, weights):
    w1, w2, budget = weights
    open = [Util.PQ() for _ in range(len(priorities))]  # n+1 priority queues
    open_sets = [set([start.state]) for _ in range(len(priorities))]
    closed_anchor = set()
    closed_inad = set()
    
    for i in range(len(priorities)):
        open[i].push((start), priorities[i](start.state, goal, start.g_score, (w1, budget)))
    
    while not open[0].isEmpty():
        for i in range(1, len(priorities)):
            if not open[i].isEmpty() and open[i].peek()[0] <= w2 * open[0].peek()[0]:
                current = open[i].pop()
                open_sets[i].remove(current.state)
                closed_inad.add(current.state)
                if current.state == goal:
                    return reconstruct_path(current, start, goal), open_sets[i], closed_inad, current.g_score
                for neighbor in current.expand_node(grid):
                    g = neighbor.g_score
                    if neighbor.state not in closed_anchor:
                        f = priorities[i](neighbor.state, goal, g, (w1, budget))
                        open[0].update((neighbor), f)
                        open_sets[0].add(neighbor.state)
                        if neighbor.state not in closed_inad:
                            for i in range(1, len(priorities)):
                                open[i].update((neighbor), f)
                                open_sets[i].add(neighbor.state)
            else:
                current = open[0].pop()
                open_sets[0].remove(current.state)
                closed_anchor.add(current.state)
                if current.state == goal:
                    return reconstruct_path(current, start, goal), open_sets[0], closed_anchor, current.g_score
                for neighbor in current.expand_node(grid):
                    g = neighbor.g_score
                    if neighbor.state not in closed_anchor:
                        f = priorities[i](neighbor.state, goal, g, (1,budget))
                        open[0].update((neighbor), f)
                        open_sets[0].add(neighbor.state)
                        if neighbor.state not in closed_inad:
                            for i in range(1, len(priorities)):
                                open[i].update((neighbor), f)
                                open_sets[i].add(neighbor.state)
    
    return None, open_sets[0], closed_anchor, None

def reconstruct_path(current, start, goal):
    path = []
    while current != start:
        path.append(current.state)
        current = current.parent
    path.append(start.state)
    path.reverse()
    return path

def update_weight_MH(weight, p):
    w1, w2, b = weight
    return (max(w1 - 2, 1), max(w2 - 2, 1), b)

def valid_weight_MH(weight):
    w1, w2, b = weight
    return w1 >=1 and w2 >= 1

def update_weight_P(weight, p):
    w1, w2, budget = weight
    return (max(w1 - 2, 1), max(w2 - 2, 1), max(p - 10, 1))

def valid_weight_P(weight):
    w1, w2, budget = weight
    return valid_weight_MH(weight) and budget > 0

def search(grid, start, goal, heuristics, weight, update, valid, time):
    best_path = None
    best_cost = math.inf
    best_open = None
    best_close = None
    S = None
    
    if len(heuristics) > 1:
        S = heuristic_search_multi
        h = heuristics
    else:
        S = heuristic_search_single
        h = heuristics[0]

    while valid(weight) and time > 0:
        time -= 1
        path, open_set, closed_set, path_cost = S(grid, start, goal, h, weight)

        if path is not None:
            if path_cost < best_cost:
                best_path = path
                best_cost = path_cost
                best_open = open_set
                best_close = closed_set
            weight = update(weight, path_cost)
        else:
            break 

    return best_path, best_open, best_close, best_cost

if __name__ == "__main__":
    width, height = 20, 20
    grid = Util.Gridworld(width, height, 0.3, 10, connectivity=8)

    start = Util.Node((0, 0), None, 0)
    goal = (height - 1, width - 1)
    h = [heu.priority_manhattan, heu.priority_euclidean, heu.priority_chebyshev, heu.priority_octile]
    p = [heu.potential_manhattan, heu.potential_euclidean, heu.potential_chebyshev, heu.potential_octile]

    while not grid.path_exists(start, goal):
        grid = Util.Gridworld(width, height, 0.3, 10, connectivity=8)

    #normal astar
    #res = search(grid, start, goal, [heu.priority_manhattan], (1,1, None), update_weight_MH, valid_weight_MH, 1)
    
    #weighted astar
    #res = search(grid, start, goal, [heu.priority_manhattan], (3,1, None), update_weight_MH, valid_weight_MH, 1)
    
    #multi heuristic
    #res = search(grid, start, goal, h, (3,3, None), update_weight_MH, valid_weight_MH, 1)
    
    #anytime
    #res = search(grid, start, goal, [heu.priority_manhattan], (10,1,None), update_weight_MH, valid_weight_MH, 10)
    
    #anytime multi heuristic
    #res = search(grid, start, goal, h, (10,10, None), update_weight_MH, valid_weight_MH, 10)
    
    #normal potential search
    #res = search(grid, start, goal, [heu.potential_manhattan], (1,1, 150), update_weight_P, valid_weight_P, 1)
    
    #anytime potenial search
    #res = search(grid, start, goal, [heu.potential_manhattan], (1,1, 200), update_weight_P, valid_weight_P, 10)
    
    #multi heuristic potential search
    #res = search(grid, start, goal, p, (3,3,150), update_weight_P, valid_weight_P, 1)
    
    #anytime multi heuristic potential search
    res = search(grid, start, goal, p, (10,10,200), update_weight_P, valid_weight_P, 10)
    
    
    best_path, best_open, best_close, best_cost = res

    if best_path:
        print("Best Path Found:", best_path)
        print("Path Cost:", best_cost)
        grid.draw_grid(best_path, start.state, goal, best_open, best_close)
    else:
        print("No path found")
        grid.draw_grid(best_path, start.state, goal, best_open, best_close)
