import heapq
from typing import Callable, List, Dict, Set, Tuple, Optional
import Util as Util

class PriorityQueue():
    def __init__(self):
        self.heap = []

    def push(self, priority, node):
        heapq.heappush(self.heap, (priority, node))

    def pop(self):
        return heapq.heappop(self.heap)[1]
    
    def peek(self):
        return self.heap[0]
    
    def is_empty(self):
        return len(self.heap) == 0
    
    def clear(self):
        self.heap = []
