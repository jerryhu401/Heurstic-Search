import math
import Queues as Q
import Priority as P
import Util as Util
import heuristics as heuristics
import DC as DC
from typing import Callable, List, Tuple, Optional

class GenericFrontier:
    def __init__(self, queue: Q.PriorityQueue, DC: DC.DominanceCheck, priority: P.Priority, grid: Util.Gridworld) -> None:
        self.queue = queue
        self.DC = DC
        self.priority = priority
        self.grid = grid

    def insert(self, node: Util.Node) -> None:
        priority: float = self.priority(node)
        self.queue.push(priority, node)
        self.DC.insert(node)

    def remove(self) -> Util.Node:
        node: Util.Node = self.queue.pop()
        self.DC.expand(node)
        return node

    def expand_node(self, node: Util.Node) -> None:
        for neighbor in self.grid.expand_node(node):
            if not self.DC.is_dominated(neighbor):
                priority: float = self.priority(neighbor)
                self.queue.push(priority, neighbor)
    
    def peek(self) -> Tuple[float, Util.Node]:
        return self.queue.peek()
    
    def is_empty(self) -> bool:
        return self.queue.is_empty()

    def restart(self) -> bool:
        if not self.priority.valid():
            return False
        
        open_set = self.DC.get_open()
        incons = self.DC.get_incons()
        new_open: List[Util.Node] = list(open_set | incons)
        self.queue.clear()
        self.DC.clear()
        
        for node in new_open:
            self.insert(node)
        
        self.priority.update()
        return True

class MultiFrontier:
    def __init__(self, queues: List[Q.PriorityQueue], DC: DC.DominanceCheck, priorities: List[P.Priority], grid: Util.Gridworld, w2: int = 5, e: int = 1) -> None:
        self.anchor = GenericFrontier(queues[0], DC, priorities[0], grid)
        self.inads: List[GenericFrontier] = [GenericFrontier(queues[i], DC.copy(), priorities[i], grid) for i in range(1, len(priorities))]
        self.w2 = w2
        self.e = e
        self.index = 0
        
    def chooseFrontier(self) -> GenericFrontier:
        return self.inads[self.index]
    
    def insert(self, node: Util.Node) -> None:
        self.anchor.insert(node)
        for F in self.inads:
            F.insert(node)

    def remove(self) -> Util.Node:
        F: GenericFrontier = self.chooseFrontier()
        if F.peek()[0] > self.w2 * self.anchor.peek()[0]:
            F = self.anchor
        else:
            self.index = (self.index + 1) % len(self.inads)
        return F.remove()
    
    def expand_node(self, node: Util.Node) -> None:
        self.anchor.expand_node(node)
        for F in self.inads:
            F.expand_node(node)
    
    def peek(self) -> Tuple[float, Util.Node]:
        return self.chooseFrontier().peek()

    def is_empty(self) -> bool:
        return self.anchor.is_empty()
    
    def restart(self) -> bool:
        if not self.anchor.restart():
            print("2")
            return False
        for F in self.inads:
            if not F.restart():
                print("3")
                return False
        self.w2 = max(self.w2 - self.e, 1)
        self.index = 0
        return True
        
def ARA(start: Util.Node, goal_check: Callable[[Util.Node], bool], frontier: MultiFrontier) -> Tuple[List[List[Tuple[int, int]]], List[float]]:
    frontier.insert(start)
    paths: List[List[Tuple[int, int]]] = []
    costs: List[float] = []
    while frontier.restart():
        curr: Optional[Util.Node] = None
        while not frontier.is_empty():
            curr = frontier.peek()[1]
            if goal_check(curr):
                paths.append(reconstruct_path(start, curr))
                costs.append(curr.g_score)
                break
            node = frontier.remove()
            frontier.expand_node(node)
    return paths, costs

def reconstruct_path(start: Util.Node, current: Util.Node) -> List[Tuple[int, int]]:
    path: List[Tuple[int, int]] = []
    while current != start:
        path.append(current.state)
        if current.parent is None:
            break  
        current = current.parent
    path.append(start.state)
    path.reverse()
    return path

if __name__ == "__main__":
    width: int = 20
    height: int = 20
    grid: Util.Gridworld = Util.Gridworld(width, height, 0.3, 10, connectivity=8)

    goal: Util.Node = Util.Node((height - 1, width - 1), None, math.inf, None)
    start: Util.Node = Util.Node((0, 0), None, 0, goal)

    while not (grid.path_exists(start, goal.state) and grid.is_traversable(*start.state) and grid.is_traversable(*goal.state)):
        grid = Util.Gridworld(width, height, 0.3, 10, connectivity=8)

    w1: int = 10
    e: int = 2
    t: int = 5
    h: List[Callable[[Util.Node], float]] = [
        heuristics.heuristic_euclidean,
        heuristics.heuristic_manhattan,
        heuristics.heuristic_chebyshev,
        heuristics.heuristic_octile
    ]

    p: List[P.Priority] = [P.Priority(h[i], w1, e, t) for i in range(len(h))]
    dc: DC.DominanceCheck = DC.DominanceCheck(DC.g_score_DC)
    queue: Q.PriorityQueue = Q.PriorityQueue()
    queues: List[Q.PriorityQueue] = [Q.PriorityQueue() for _ in range(len(h))]
    single: GenericFrontier = GenericFrontier(queue, dc, p[0], grid)
    multi: MultiFrontier = MultiFrontier(queues, dc, p, grid)
    
    def goal_check(node: Util.Node) -> bool:
        return node.state == goal.state

    res: Tuple[List[List[Tuple[int, int]]], List[float]] = ARA(start, goal_check, multi)
    
    paths, costs = res

    if len(paths) > 0:
        print("Best Path Found:", paths[-1])
        print("Path Cost:", costs[-1])
        grid.draw_grid(paths, costs)
    else:
        print("No path found")
        grid.draw_grid(None)
