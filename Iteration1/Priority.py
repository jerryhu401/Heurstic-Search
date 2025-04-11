import Util as Util
import math
from typing import Callable, List, Dict, Set, Tuple, Optional

class Priority:
    def __init__(self, heuristic: Callable[[Util.Node], float], w1: float = 1, e: float = 0, time: int = 1):
        self.heuristic: Callable[[Util.Node], float] = heuristic
        self.w1: float = w1
        self.e: float = e
        self.time: int = time

    def valid(self) -> bool:
        return self.w1 >= 1 and self.time > 0
    
    def update(self) -> None:
        self.w1 = max(self.w1 - self.e, 1)
        self.time -= 1

    def __call__(self, node: Util.Node) -> float:
        state = node.state
        g = node.g_score
        goal = node.goal
        return self.w1 * self.heuristic(node, goal) + g
    

class PriorityPotential:
    def __init__(self, heuristic: callable):
        self.heuristic: callable = heuristic
        self.w1: float = 1
        self.w2: float = 1
        self.budget: float = 200
        self.e: float = 0
        self.time: int = 1

    def valid(self) -> bool:
        return self.w1 >= 1 and self.w2 >= 1 and self.budget > 0 and self.time > 0
    
    def update(self, cost: float) -> None:
        self.budget = cost - 15
        self.w1 = max(self.w1 - self.e, 1)
        self.w2 = max(self.w2 - self.e, 1)
        self.time -= 1

    def configure(self, w1: float, w2: float, budget: float, e: float, time: int) -> None:
        self.w1 = w1
        self.w2 = w2
        self.budget = budget
        self.e = e
        self.time = time

    def __call__(self, node: Util.Node) -> float:
        state = node.state
        g = node.g_score
        goal = node.goal
        h = self.w1 * self.heuristic(node, goal)
        if h == 0:
            return 0
        if (self.budget - g) <= 0:
            return math.inf
        return h / (self.budget - g)
