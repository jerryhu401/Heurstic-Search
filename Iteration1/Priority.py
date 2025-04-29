from abc import ABC, abstractmethod
from typing import Callable
import Util

class AbstractPriorityFunction(ABC):
    @abstractmethod
    def __call__(self, node: "Util.AbstractNode") -> float:
        pass

    @abstractmethod
    def valid(self) -> bool:
        pass

    @abstractmethod
    def update(self) -> None:
        pass


class Priority(AbstractPriorityFunction):
    def __init__(self, heuristic: Callable[["Util.AbstractNode", "Util.AbstractNode"], float], w1: float = 1, e: float = 0, time: int = 1):
        self.heuristic: Callable[[Util.AbstractNode, Util.AbstractNode], float] = heuristic
        self.w1: float = w1
        self.e: float = e
        self.time: int = time

    def valid(self) -> bool:
        return self.w1 >= 1 and self.time > 0

    def update(self) -> None:
        self.w1 = max(self.w1 - self.e, 1)
        self.time -= 1

    def __call__(self, node: Util.AbstractNode) -> float:
        g = node.g_score
        return self.w1 * self.heuristic(node, node.goal) + g
