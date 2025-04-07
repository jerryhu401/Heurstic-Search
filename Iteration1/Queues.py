import heapq
from typing import List, Tuple, TypeVar, Generic

T = TypeVar("T")

class PriorityQueue(Generic[T]): #wrapper for heapq
    def __init__(self) -> None:
        self.heap: List[Tuple[float, T]] = []

    def push(self, priority: float, node: T) -> None: #priority type can be generalized
        heapq.heappush(self.heap, (priority, node))

    def pop(self) -> T:
        return heapq.heappop(self.heap)[1]
    
    def peek(self) -> Tuple[float, T]:
        return self.heap[0]
    
    def is_empty(self) -> bool:
        return len(self.heap) == 0
    
    def clear(self) -> None:
        self.heap = []

