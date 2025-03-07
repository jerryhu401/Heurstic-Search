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
    
    def add(self, node):
        priority = node.g_score + self.w1 * self.heuristic(node.state, node.goal.state)
        heapq.heappush(self.queue, (priority, node))
    
    def push(self, node):
        if node.g_score < self.g_scores.get(node.state, math.inf):
            self.g_scores[node.state] = node.g_score
            if node.state not in self.closed_set:
                self.add(node)
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
    
    def check(self):
        if self.peek()[1].state == self.goal.state:
            return self.peek()[1]
        return None
    
    def is_empty(self):
        return len(self.queue) == 0
    
    def size(self):
        return len(self.queue)
    

class MultiQueue():
    def __init__(self, heuristics, start, grid):
        self.queues = [PriorityQueue(heuristic, start, grid) for heuristic in heuristics]
        self.anchor_queue = self.queues[0]
        self.inad_queues = self.queues[1:]
        self.w1 = 10
        self.w2 = 10
        self.grid = grid
        self.goal = start.goal
    
    def push(self, node):
        self.anchor_queue.push(node)
        for queue in self.inad_queues:
            queue.push(node)

    def expand_node(self, queue):
        node = queue.pop()
        if queue == self.anchor_queue:
            queue.closed_set.add(node.state)
        else:
            for queue in self.inad_queues:
                queue.closed_set.add(node.state)
        for neighbor in node.expand_node(self.grid):
            self.push(neighbor)
    
    def iterate_queues(self):
        for queue in self.inad_queues:
            if self.check() != None:
                return
            if queue.peek()[0] <= self.w2 * self.anchor_queue.peek()[0]:
                self.expand_node(queue)
            else:
                self.expand_node(self.anchor_queue)

    def restart(self):
        if self.w1 <= 1 or self.w2 <= 1:
            return False
        for queue in self.queues:
            queue.restart()
        self.w1 -= 2
        self.w2 -= 2
        return True
    
    def pop(self):
        if self.is_empty():
            raise IndexError("pop from an empty priority queue")
        return heapq.heappop(self.queue)[1]
    
    def peek(self):
        if self.is_empty():
            raise IndexError("peek from an empty priority queue")
        return self.queue[0]
    
    def check(self):
        for queue in self.queues:
            if queue.peek()[1].state == self.goal.state:
                return queue.peek()[1]
        return None
    
    def is_empty(self):
        return self.anchor_queue.is_empty()