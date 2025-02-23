import math
import Util
import heuristics as heu
import Priority as P

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

def reconstruct_path(current, start, goal):
    path = []
    while current != start:
        path.append(current.state)
        current = current.parent
    path.append(start.state)
    path.reverse()
    return path

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

if __name__ == "__main__":
    width, height = 20, 20
    grid = Util.Gridworld(width, height, 0.3, 10, connectivity=8)

    goal = Util.Node((height - 1, width - 1), None, math.inf, None)
    start = Util.Node((0, 0), None, 0, goal)
    heuristics = [heu.heuristic_manhattan, heu.heuristic_manhattan, heu.heuristic_manhattan, heu.heuristic_manhattan]

    priorities = []
    anytimeP = []
    potentials = []
    anytimePotentials = []

    for h in heuristics:
        p = P.Priority(h)
        p2 = P.Priority(h)
        p3 = P.PriorityPotential(h)
        p4 = P.PriorityPotential(h)
        p.configure(3, 3, 0, 1)
        p2.configure(12, 12, 2, 10)
        p3.configure(3,3, 200, 0, 1)
        p4.configure(12, 12, 200, 2, 10)
        priorities.append(p)
        anytimeP.append(p2)
        potentials.append(p3)
        anytimePotentials.append(p4)


    while not grid.path_exists(start, goal.state):
        grid = Util.Gridworld(width, height, 0.3, 10, connectivity=8)

    #weighted astar
    #res = search(grid, start, goal.state, [priorities[0]])
    
    #multi heuristic
    #res = search(grid, start, goal.state, priorities)
    
    #anytime
    #res = search(grid, start, goal.state, [anytimeP[0]])
    
    #anytime multi heuristic
    #res = search(grid, start, goal.state, anytimeP)
    
    #normal potential search
    #res = search(grid, start, goal.state, [P.PriorityPotential(heu.heuristic_manhattan)])
    
    #anytime potenial search
    #res = search(grid, start, goal.state, [anytimePotentials[0]])
    
    #anytime multi heuristic potential search
    res = search(grid, start, goal.state, anytimePotentials)
    
    
    best_path, best_open, best_close, best_cost = res

    if best_path:
        print("Best Path Found:", best_path)
        print("Path Cost:", best_cost)
        grid.draw_grid(best_path, start.state, goal.state, best_open, best_close)
    else:
        print("No path found")
        grid.draw_grid(best_path, start.state, goal.state, best_open, best_close)
