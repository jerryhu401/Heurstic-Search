import math
import heapq
import Priority 

class PriorityQueue():
    def __init__(self):
        self.heap = []

    def push(self, priority, node):
        heapq.heappush(self.heap, (priority, node))

    def pop(self):
        return heapq.heappop(self.heap)[1]
    
    def peek(self):
        return self.heap[0][1]
    
    def is_empty(self):
        return len(self.heap) == 0
    
    def clear(self):
        self.heap = []
    
class GenericFrontier():
    def __init__(self, queue, DC, priority):
        self.heap = []
        self.queue = queue
        self.DC = DC
        self.priority = priority

    def expand_node(self, node):
        node = self.queue.pop()
        self.DC.expand(node)
        for neighbor in node.expand_node(self.grid):
            if not self.DC.is_dominated(neighbor):
                priority = self.priority(neighbor)
                self.queue.push(priority, neighbor)
    
    def peek(self):
        return self.queue.peek()
    
    def is_empty(self):
        return self.queue.is_empty()

    def restart(self):
        if not self.priority.valid():
            return False
        
        open = self.DC.get_open()
        incons = self.DC.get_incons()
        new_open = list(open | incons)
        self.queue.clear()
        self.DC.clear()
        
        for node in new_open:
            priority = self.priority(node)
            self.queue.push(priority, node)
            self.DC.insert(node)
        
        self.priority.update()
        return True

    
