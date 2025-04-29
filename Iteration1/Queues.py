import heapq
from typing import List, Tuple, TypeVar, Generic

T = TypeVar("T")

class PriorityQueue(Generic[T]): #take in priority function, add a get nodes function
    def __init__(self, priority) -> None:
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

