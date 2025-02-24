import math
import Util

def heuristic_search_single(grid, start, goal, priority):
    open = Util.PQ()
    open_set = set([start.state])
    closed_anchor = set()
    open.push((start), priority(start))
    
    while not open.isEmpty():
        current = open.pop()
        open_set.remove(current.state)
        closed_anchor.add(current.state)
        if current.state == goal:
            return reconstruct_path(current, start, goal), open_set, closed_anchor, current.g_score
        for neighbor in current.expand_node(grid):
            g = neighbor.g_score
            if neighbor.state not in closed_anchor:
                open.update((neighbor), priority(neighbor))
                open_set.add(neighbor.state)
    
    return None, open_set, closed_anchor, None

def heuristic_search_multi(grid, start, goal, priorities):
    open = [Util.PQ() for _ in range(len(priorities))]
    open_sets = [set([start.state]) for _ in range(len(priorities))]
    closed_anchor = set()
    closed_inad = set()
    
    for i in range(len(priorities)):
        open[i].push((start), priorities[i](start))
    
    while not open[0].isEmpty():
        for i in range(1, len(priorities)):
            if not open[i].isEmpty() and open[i].peek()[0] <= priorities[0].w2 * open[0].peek()[0]:
                current = open[i].pop()
                open_sets[i].remove(current.state)
                closed_inad.add(current.state)
                if current.state == goal:
                    return reconstruct_path(current, start, goal), open_sets[i], closed_inad, current.g_score
                for neighbor in current.expand_node(grid):
                    g = neighbor.g_score
                    if neighbor.state not in closed_anchor:
                        open[0].update((neighbor), priorities[i](neighbor))
                        open_sets[0].add(neighbor.state)
                        if neighbor.state not in closed_inad:
                            for i in range(1, len(priorities)):
                                open[i].update((neighbor), priorities[i](neighbor))
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
                        open[0].update((neighbor), priorities[i](neighbor))
                        open_sets[0].add(neighbor.state)
                        if neighbor.state not in closed_inad:
                            for i in range(1, len(priorities)):
                                open[i].update((neighbor), priorities[i](neighbor))
                                open_sets[i].add(neighbor.state)
    
    return None, open_sets[0], closed_anchor, None

def search(grid, start, goal, heuristics):
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

    while heuristics[0].valid():
        path, open_set, closed_set, path_cost = S(grid, start, goal, h)

        if path is not None:
            if path_cost < best_cost:
                best_path = path
                best_cost = path_cost
                best_open = open_set
                best_close = closed_set
            for p in heuristics:
                p.update(path_cost)
        else:
            break 

    return best_path, best_open, best_close, best_cost

def reconstruct_path(current, start):
    path = []
    while current != start:
        path.append(current.state)
        current = current.parent
    path.append(start.state)
    path.reverse()
    return path