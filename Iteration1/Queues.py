from abc import ABC, abstractmethod
from typing import List, Tuple, TypeVar, Generic, Callable
import heapq

T = TypeVar("T")

class AbstractPriorityQueue(ABC, Generic[T]):
    @abstractmethod
    def push(self, node: T) -> None:
        pass

    @abstractmethod
    def pop(self) -> T:
        pass

    @abstractmethod
    def peek(self) -> Tuple[float, T]:
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

    @abstractmethod
    def get_nodes(self) -> List[T]:
        pass


class PriorityQueue(AbstractPriorityQueue[T]):
    def __init__(self, priority: Callable[[T], float]) -> None:
        self.heap: List[Tuple[float, T]] = []
        self.priority = priority

    def push(self, node: T) -> None:
        priority: float = self.priority(node)
        heapq.heappush(self.heap, (priority, node))

    def pop(self) -> T:
        return heapq.heappop(self.heap)[1]
    
    def peek(self) -> Tuple[float, T]:
        return self.heap[0]
    
    def is_empty(self) -> bool:
        return len(self.heap) == 0
    
    def clear(self) -> None:
        self.heap = []

    def get_nodes(self) -> List[T]:
        return [node for _, node in self.heap]
