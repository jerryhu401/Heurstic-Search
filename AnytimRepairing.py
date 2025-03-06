import Util
import math
import heapq
import heuristics
import Queues as Q

def reconstruct_path(node, start, current):
    path = []
    while current != start:
        path.append(current.state)
        current = current.parent
    path.append(start.state)
    path.reverse()
    return path

def ARA(start, open):
    paths = []
    costs = []
    while open.restart():
        goal = None
        while not open.is_empty():
            if open.peek()[1].state == open.goal.state:
                goal = open.peek()[1]
                break
            open.iterate_queues()
        if goal != None:
            paths.append(reconstruct_path(goal, start, goal))
            costs.append(goal.g_score)
    return paths, costs

if __name__ == "__main__":
    width, height = 20, 20
    grid = Util.Gridworld(width, height, 0.3, 10, connectivity=8)

    goal = Util.Node((height - 1, width - 1), None, math.inf, None)
    start = Util.Node((0, 0), None, 0, goal)

    while not (grid.path_exists(start, goal.state) and grid.is_traversable(*(start.state)) and grid.is_traversable(*(goal.state))):
        grid = Util.Gridworld(width, height, 0.3, 10, connectivity=8)

    queue = Q.PriorityQueue(heuristics.heuristic_euclidean, start, grid)
    res = ARA(start, queue)
    
    
    paths, costs = res

    if len(paths)>0:
        print("Best Path Found:", paths[-1])
        print("Path Cost:", costs[-1])
        grid.draw_grid(paths, costs)
    else:
        print("No path found")
        grid.draw_grid(None)