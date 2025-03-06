import Util
import math
import heapq

class PriorityQueue():
    def __init__(self, heuristic, start, grid):
        self.heuristic = heuristic
        self.queue = []
        self.g_scores = {}
        self.closed_set = set()
        self.incons_set = set()
        self.w1 = 10
        self.grid = grid
        self.push(start)
        self.goal = start.goal
        self.g_scores[self.goal.state] = math.inf
    
    def push(self, node):
        if node.g_score < self.g_scores.get(node.state, math.inf):
            self.g_scores[node.state] = node.g_score
            if node.state not in self.closed_set:
                priority = node.g_score + self.w1 * self.heuristic(node.state, node.goal.state)
                heapq.heappush(self.queue, (priority, node))
            else:
                self.incons_set.add(node)

    def expand_node(self):
        node = self.pop()
        self.closed_set.add(node.state)
        for neighbor in node.expand_node(self.grid):
            self.push(neighbor)
    
    def iterate_queues(self):
        self.expand_node()

    def restart(self):
        if self.w1 <= 1:
            return False
        new_queue = []
        for i in range(len(self.queue)):
            node = self.queue[i][1]
            new_priority = node.g_score + self.w1 * self.heuristic(node.state, node.goal.state)
            heapq.heappush(new_queue, (new_priority, node))
        for node in self.incons_set:
            priority = node.g_score + self.w1 * self.heuristic(node.state, node.goal.state)
            heapq.heappush(new_queue, (priority, node))
        self.queue = new_queue
        self.incons_set = set()
        self.closed_set = set()
        self.w1 -= 2
        return True
    
    def pop(self):
        if self.is_empty():
            raise IndexError("pop from an empty priority queue")
        return heapq.heappop(self.queue)[1]
    
    def peek(self):
        if self.is_empty():
            raise IndexError("peek from an empty priority queue")
        return self.queue[0]
    
    def is_empty(self):
        return len(self.queue) == 0
    
    def size(self):
        return len(self.queue)