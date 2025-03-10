import Util
import math
import heapq

class Priority():
    def __init__(self, heuristic, w1 = 1, e = 0, time = 1):
        self.heuristic = heuristic
        self.w1 = w1
        self.e = e
        self.time = time

    def valid(self):
        return self.w1 >= 1 and self.time > 0
    
    def update(self):
        self.w1 = max(self.w1 - self.e, 1)
        self.time -= 1

    def __call__(self, node : Util.Node):
        state = node.state
        g = node.g_score
        goal_state = node.goal.state
        p = self.w1*self.heuristic(state, goal_state) + g
        return p
    

class PriorityPotential():
    def __init__(self, heuristic):
        self.heuristic = heuristic
        self.w1 = 1
        self.w2 = 1
        self.budget = 200
        self.e = 0
        self.time = 1

    def valid(self):
        return self.w1 >= 1 and self.w2 >= 1 and self.budget > 0 and self.time > 0
    
    def update(self, cost):
        self.budget = cost - 15
        self.w1 = max(self.w1 - self.e, 1)
        self.w2 -= max(self.w2 - self.e, 1)
        self.time -= 1

    def configure(self, w1, w2, budget, e, time):
        self.w1 = w1
        self.w2 = w2
        self.budget = budget
        self.e = e
        self.time = time

    def __call__(self, node : Util.Node):
        state = node.state
        g = node.g_score
        goal_state = node.goal.state
        h = self.w1*self.heuristic(state, goal_state) 
        if h == 0:
            return 0
        if ((self.budget - g) <= 0):
            return math.inf
        return h/(self.budget - g)


class PriorityQueue():
    def __init__(self, heuristic, grid):
        self.heuristic = heuristic
        self.queue = []
        self.count = 0
        self.g_scores = {}
        self.open_set = set()
        self.closed_set = set()
        self.incons_set = set()
        self.w1 = 1
        self.grid = grid
    
    def push(self, node):
        if node.g_score < self.g_scores.get(node.state, math.inf):
            self.g_scores[node.state] = node.g_score
            if node.state not in self.closed_set:
                priority = node.g_score + self.w1 * self.heuristic(node.state, node.goal.state)
                heapq.heappush(self.heap, (priority, node))
                self.open_set.add(node)
            else:
                self.incons_set.add(node)

    def expand_node(self, node):
        self.open_set.remove(node)
        self.closed_set.add(node.state)
        for neighbor in node.expand_node(self.grid):
            self.push(neighbor)
    
    def pop(self):
        if self.is_empty():
            raise IndexError("pop from an empty priority queue")
        return heapq.heappop(self.heap)[1]
    
    def peek(self):
        if self.is_empty():
            raise IndexError("peek from an empty priority queue")
        return self.heap[0][1]
    
    def is_empty(self):
        return len(self.heap) == 0
    
    def size(self):
        return len(self.heap)