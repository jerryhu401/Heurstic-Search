import math
import Util
import heuristics as heu
import Priority as P

def improve_path(grid, goal, priority, open_set, g_scores):
    open_set = open_set[0]
    open = Util.PQWithUpdate()
    closed = set()
    incons = set()
    for node in open_set:
        open.push((node), priority(node))
        g_scores[node.state] = node.g_score
    
    while not open.isEmpty() and g_scores[goal] > open.peek()[0]:
        current = open.pop()
        open_set.remove(current)
        closed.add(current.state)
        
        for neighbor in current.expand_node(grid):
            g_score = neighbor.g_score
            
            if g_score < g_scores.get(neighbor.state, math.inf):
                g_scores[neighbor.state] = g_score
                if neighbor.state not in closed:
                    open.update((neighbor), priority(neighbor))
                    open_set.add(neighbor)
                else:
                    incons.add(neighbor)
    
    res = None
    if g_scores[goal] == open.peek()[0]:
        res = open.peek()[-1]

    return [open_set], closed, [incons], res, g_scores

def improve_path_multi(grid, goal, priority, open_set, gs):
    open = [Util.PQWithUpdate() for _ in range(len(priorities))]
    open_anchor: set[Util.Node] = open_set[0]
    open_inad = open_set[1]
    closed_anchor = set()
    closed_inad = set()
    incons_anchor = set()
    incons_inad = set()
    incons = [incons_anchor, incons_inad]
    for node in open_inad:
        for i in range(1, len(priorities)):
            open[i].push((node), priority[i](node))
        gs[1][node.state] = node.g_score
        open_inad.add(node)
    for node in open_anchor:
        open[0].push((node), priority[0](node))
        open_anchor.add(node)
        gs[0][node.state] = node.g_score
    
    while not open[0].isEmpty():
        for i in range(1, len(priorities)):
            if not open[i].isEmpty() and open[i].peek()[0] <= priorities[0].w2 * open[0].peek()[0]:
                g_scores = gs[1]
                if g_scores[goal] <= open[i].peek()[0] and open[i].peek()[-1].state == goal: #why this works???
                    return open_set, closed_inad, incons, open[i].peek()[-1], g_scores
                current = open[i].pop()
                open_inad.remove(current)
                closed_inad.add(current.state)
            else:
                g_scores = gs[0]
                if g_scores[goal] <= open[0].peek()[0] and open[i].peek()[-1].state == goal:
                    return open_set, closed_anchor, incons, open[0].peek()[-1], g_scores
                current = open[0].pop()
                open_anchor.remove(current)
                closed_anchor.add(current.state)
            for neighbor in current.expand_node(grid):
                g_score = neighbor.g_score
                if g_score < g_scores.get(neighbor.state, math.inf):
                    g_scores[neighbor.state] = g_score
                    if neighbor.state not in closed_anchor:
                        open[0].update((neighbor), priorities[i](neighbor))
                        open_anchor.add(neighbor)
                        if neighbor.state not in closed_inad:
                            for i in range(1, len(priorities)):
                                open[i].update((neighbor), priorities[i](neighbor))
                            open_inad.add(neighbor)
                        else:
                            incons_inad.add(neighbor)
                    else:
                        incons_anchor.add(neighbor)
    
    return open_anchor, closed_anchor, incons_anchor, None


def ARA(grid, start, goal, heuristics):
    best_path = None
    best_cost = math.inf
    res = []
    
    if len(heuristics) > 1:
        improve = improve_path_multi
        h = heuristics
        g_scores = []
        g_score_anchor = {goal : math.inf}
        g_score_inad = {goal : math.inf}
        g_scores = [g_score_anchor, g_score_inad]
        open = [set([start]) for _ in range(2)]
    else:
        improve = improve_path
        h = heuristics[0]
        g_scores = {}
        g_scores[goal] = math.inf
        open = [set([start])]

    while heuristics[0].valid():
        open_set, closed_set, incons_set, node, g = improve(grid, goal, h, open, g_scores)

        for i in range(len(open_set)):
            open[i] = open_set[i] | incons_set[i]
        if node != None:
            path_cost = g[goal]
            if g[goal] < best_cost:
                best_path = reconstruct_path(node, start)
                best_cost = path_cost
                res.append((best_path, best_cost))
            for p in heuristics:
                p.update(path_cost)
        else:
            break 
    

    return res

def reconstruct_path(current, start):
    path = []
    while current != start:
        path.append(current.state)
        current = current.parent
    path.append(start.state)
    path.reverse()
    return path

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


    while not (grid.path_exists(start, goal.state) and grid.is_traversable(*(start.state)) and grid.is_traversable(*(goal.state))):
        grid = Util.Gridworld(width, height, 0.3, 10, connectivity=8)

    #anytime
    res = ARA(grid, start, goal.state, [anytimeP[0]])
    #anytime multi heuristic
    #res = ARA(grid, start, goal.state, anytimeP)
    #potential
    
    best_path, best_cost = res[-1]

    if best_path:
        print("Best Path Found:", best_path)
        print("Path Cost:", best_cost)
        grid.draw_grid(best_path)
    else:
        print("No path found")
        grid.draw_grid(best_path)