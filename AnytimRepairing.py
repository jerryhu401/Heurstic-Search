import Util
import math
import heuristics
import Queues as Q
from typing import List, Optional, Tuple

def reconstruct_path(node: Util.Node, start: Util.Node, current: Util.Node) -> List[Tuple[int, int]]:
    path: List[Tuple[int, int]] = []
    while current != start:
        path.append(current.state)
        if current.parent is None:
            break  
        current = current.parent
    path.append(start.state)
    path.reverse()
    return path

def ARA(start: Util.Node, open: Q.MultiQueue) -> Tuple[List[List[Tuple[int, int]]], List[float]]:
    paths: List[List[Tuple[int, int]]] = []
    costs: List[float] = []
    while open.restart():
        goal: Optional[Util.Node] = None
        while not open.is_empty():
            goal = open.check()
            if goal is not None:
                break
            open.iterate_queues()
        if goal is not None:
            paths.append(reconstruct_path(goal, start, goal))
            costs.append(goal.g_score)
    return paths, costs

if __name__ == "__main__":
    width: int = 20
    height: int = 20
    grid: Util.Gridworld = Util.Gridworld(width, height, 0.3, 10, connectivity=8)

    goal: Util.Node = Util.Node((height - 1, width - 1), None, math.inf, None)
    start: Util.Node = Util.Node((0, 0), None, 0, goal)

    while not (grid.path_exists(start, goal.state) and grid.is_traversable(*start.state) and grid.is_traversable(*goal.state)):
        grid = Util.Gridworld(width, height, 0.3, 10, connectivity=8)

    h: List = [
        heuristics.heuristic_euclidean,
        heuristics.heuristic_manhattan,
        heuristics.heuristic_chebyshev,
        heuristics.heuristic_octile,
    ]

    queue = Q.PriorityQueue(heuristics.heuristic_euclidean, start, grid)
    queues = Q.MultiQueue(h, start, grid)
    potentialQueue = Q.PotentialQueue(heuristics.heuristic_euclidean, start, grid)

    res = ARA(start, queues)

    paths, costs = res

    if len(paths) > 0:
        print("Best Path Found:", paths[-1])
        print("Path Cost:", costs[-1])
        grid.draw_grid(paths, costs)
    else:
        print("No path found")
        grid.draw_grid(None)
