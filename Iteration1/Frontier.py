import math
import Queues as Q
import Priority as P
import Util as Util
import heuristics as heuristics
import DC as DC
import User
from typing import Callable, List, Tuple, Optional
from abc import ABC, abstractmethod

class AbstractSuccessorGenerator(ABC):
    @abstractmethod
    def __call__(self, node: "Util.Node") -> List["Util.Node"]:
        pass


class AbstractFrontier(ABC):
    @abstractmethod
    def insert(self, node: "Util.Node") -> None:
        pass

    @abstractmethod
    def remove(self) -> "Util.Node":
        pass

    @abstractmethod
    def expand_node(self, node: "Util.Node") -> None:
        pass

    @abstractmethod
    def peek(self) -> Tuple[float, "Util.Node"]:
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass


class AbstractFrontierPicker(ABC):
    @abstractmethod
    def chooseFrontier(self) -> AbstractFrontier:
        pass

    @abstractmethod
    def update(self) -> None:
        pass


class AbstractMultiFrontier(ABC):
    @abstractmethod
    def insert(self, node: "Util.Node") -> None:
        pass

    @abstractmethod
    def remove(self) -> "Util.Node":
        pass

    @abstractmethod
    def expand_node(self, node: "Util.Node") -> None:
        pass

    @abstractmethod
    def peek(self) -> Tuple[float, "Util.Node"]:
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass


class successorGenerator(AbstractSuccessorGenerator):
    def __init__(self, grid: Util.Gridworld) -> None:
        self.grid = grid

    def __call__(self, node: Util.Node) -> List[Util.Node]:
        x, y = node.state
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        if self.grid.connectivity == 8:
            directions.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)])

        result: List[Util.Node] = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.grid.is_traversable(nx, ny):
                result.append(Util.Node((nx, ny), node, node.g_score + self.grid.grid[x][y], node.goal))

        return result

class GenericFrontier(AbstractFrontier):
    def __init__(self, queue: Q.PriorityQueue, DC: DC.DominanceCheck, getSucc: AbstractSuccessorGenerator) -> None:
        self.queue = queue
        self.DC = DC
        self.getSucc = getSucc

    def insert(self, node: Util.Node) -> None:
        self.queue.push(node)

    def remove(self) -> Util.Node:
        node: Util.Node = self.queue.pop()
        self.DC.insert(node)
        return node

    def expand_node(self, node: Util.Node) -> None:
        for neighbor in self.getSucc(node):
            if not self.DC.is_dominated(neighbor):
                self.queue.push(neighbor)

    def peek(self) -> Tuple[float, Util.Node]:
        return self.queue.peek()

    def is_empty(self) -> bool:
        return self.queue.is_empty()


class FrontierPicker(AbstractFrontierPicker):
    def __init__(self, frontiers: List[AbstractFrontier], w2: float = 5, e: float = 1) -> None:
        self.anchor = frontiers[0]
        self.inads = frontiers[1:]
        self.w2 = w2
        self.e = e
        self.index = 0

    def chooseFrontier(self) -> AbstractFrontier:
        frontier = self.inads[self.index]
        if frontier.peek()[0] > self.w2 * self.anchor.peek()[0]:
            frontier = self.anchor
        else:
            self.index = (self.index + 1) % len(self.inads)
        return frontier

    def update(self) -> None:
        self.w2 = max(self.w2 - self.e, 1)
        self.index = 0


class MultiFrontier(AbstractMultiFrontier):
    def __init__(self, frontiers: List[AbstractFrontier], frontierPicker: AbstractFrontierPicker) -> None:
        self.anchor = frontiers[0]
        self.inads = frontiers[1:]
        self.picker = frontierPicker
        self.current = self.anchor

    def insert(self, node: Util.Node) -> None:
        self.anchor.insert(node)
        for F in self.inads:
            F.insert(node)

    def remove(self) -> Util.Node:
        F: AbstractFrontier = self.current
        return F.remove()

    def expand_node(self, node: Util.Node) -> None:
        self.anchor.expand_node(node)
        for F in self.inads:
            F.expand_node(node)

    def peek(self) -> Tuple[float, Util.Node]:
        self.current = self.picker.chooseFrontier()
        return self.current.peek()

    def is_empty(self) -> bool:
        return self.anchor.is_empty()
    
        
def search(start: Util.Node, goal_check: Callable[[Util.Node], bool], frontier: MultiFrontier, 
        checkStop = User.checkStop, update = User.updateGeneric) -> Tuple[List[List[Tuple[int, int]]], List[float]]:
    frontier.insert(start)
    paths: List[List[Tuple[int, int]]] = []
    costs: List[float] = []
    while checkStop(frontier):
        curr: Optional[Util.Node] = None
        while not frontier.is_empty():
            curr = frontier.peek()[1]
            if goal_check(curr):
                paths.append(reconstruct_path(start, curr))
                costs.append(curr.g_score)
                break
            node = frontier.remove()
            frontier.expand_node(node)
        update(frontier)
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

    successorGen: successorGenerator = successorGenerator(grid)

    p: List[P.Priority] = [P.Priority(h[i], w1, e, t) for i in range(len(h))]
    dc: DC.DominanceCheck = DC.DominanceCheck(DC.g_score_DC, DC.key)
    queue: Q.PriorityQueue = Q.PriorityQueue(p[0])
    queues: List[Q.PriorityQueue] = [Q.PriorityQueue(p[i]) for i in range(len(h))]
    frontiers: List[GenericFrontier] = [GenericFrontier(queues[i], dc.copy(), successorGen) for i in range(len(h))]
    frontierPicker: FrontierPicker = FrontierPicker(frontiers, 5, 1)
    single: GenericFrontier = GenericFrontier(queue, dc, successorGen)
    multi: MultiFrontier = MultiFrontier(frontiers, frontierPicker)
    
    def goal_check(node: Util.Node) -> bool:
        return node.state == goal.state

    #res: Tuple[List[List[Tuple[int, int]]], List[float]] = search(start, goal_check, single)
    res: Tuple[List[List[Tuple[int, int]]], List[float]] = search(start, goal_check, multi, User.checkStopMulti, User.updateMulti)
    
    paths, costs = res

    if len(paths) > 0:
        print("Best Path Found:", paths[-1])
        print("Path Cost:", costs[-1])
        grid.draw_grid(paths, costs)
    else:
        print("No path found")
        grid.draw_grid(None, None)