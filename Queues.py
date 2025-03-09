import math
import heapq
from typing import Callable, List, Dict, Set, Tuple, Optional
import Util

#priority functions instead of heuristics
#pass in expander function(knows what grid is), abstract class
"""
class frontier:
    takes in a dominance check, a priority queue, and a successor function
    is_empty(depends on if single or multi)
    pick_queue(moves through the inad queues one at a time)
    peek(depends on if single or multi)
    pop(depends on if single or multi)
    push(depends on if single or multi)
        if dominance check is true, push to all queues
    if multi, choose one queue to expand, and update internal counter for queue to expand
    can have w2, budget, and time
    warm restart function

class dominance_check:
    has open set, closed set, incons set, and g_scores
    basically maintains meta data and invariants for the frontier
    each time nodes are expanded, update the sets and g_scores

class priority_queue:
    only sorts, takes in a priority function

Search function takes in goal check and use it with frontier.peek()
    
"""
class PriorityQueueOld:
    def __init__(self, heuristic: Callable[[any, any], float], start: Util.Node, grid: any) -> None:
        self.heuristic: Callable[[any, any], float] = heuristic
        self.queue: List[Tuple[float, Util.Node]] = []
        self.g_scores: Dict[any, float] = {}
        self.closed_set: Set[any] = set()
        self.incons_set: Set[Util.Node] = set()
        self.w1: int = 10
        self.grid = grid
        self.push(start)
        self.goal: Util.Node = start.goal
        self.g_scores[self.goal.state] = math.inf
    
    def insert(self, node: Util.Node, queue: List[Tuple[float, Util.Node]]) -> None:
        priority = node.g_score + self.w1 * self.heuristic(node.state, node.goal.state)
        heapq.heappush(queue, (priority, node))
    
    def push(self, node: Util.Node) -> None:
        if node.g_score < self.g_scores.get(node.state, math.inf):
            self.g_scores[node.state] = node.g_score
            if node.state not in self.closed_set:
                self.insert(node, self.queue)
            else:
                self.incons_set.add(node)

    def expand_node(self) -> None:
        node = self.pop()
        self.closed_set.add(node.state)
        for neighbor in node.expand_node(self.grid):
            self.push(neighbor)
    
    def iterate_queues(self) -> None:
        self.expand_node()

    def restart(self) -> bool:
        if self.w1 <= 1:
            return False
        new_queue: List[Tuple[float, Util.Node]] = []
        for _, node in self.queue:
            self.insert(node, new_queue)
        for node in self.incons_set:
            self.insert(node, new_queue)
        self.queue = new_queue
        self.incons_set = set()
        self.closed_set = set()
        self.w1 -= 2
        return True
    
    def pop(self) -> Util.Node:
        if self.is_empty():
            raise IndexError("pop from an empty priority queue")
        return heapq.heappop(self.queue)[1]
    
    def peek(self) -> Tuple[float, Util.Node]:
        if self.is_empty():
            raise IndexError("peek from an empty priority queue")
        return self.queue[0]
    
    def check(self) -> Optional[Util.Node]:
        if self.peek()[1].state == self.goal.state:
            return self.peek()[1]
        return None
    
    def is_empty(self) -> bool:
        return len(self.queue) == 0
    

class MultiQueue:
    def __init__(self, heuristics: List[Callable[[any, any], float]], start: Util.Node, grid: any) -> None:
        self.queues: List[PriorityQueue] = [PriorityQueue(heuristic, start, grid) for heuristic in heuristics]
        self.anchor_queue: PriorityQueue = self.queues[0]
        self.inad_queues: List[PriorityQueue] = self.queues[1:]
        self.w1: int = 10
        self.w2: int = 10
        self.grid = grid
        self.goal: Util.Node = start.goal
    
    def push(self, node: Util.Node) -> None:
        self.anchor_queue.push(node)
        for queue in self.inad_queues:
            queue.push(node)

    def expand_node(self, queue: PriorityQueue) -> None:
        node = queue.pop()
        if queue == self.anchor_queue:
            queue.closed_set.add(node.state)
        else:
            for queue in self.inad_queues:
                queue.closed_set.add(node.state)
        for neighbor in node.expand_node(self.grid):
            self.push(neighbor)
    
    def iterate_queues(self) -> None:
        for queue in self.inad_queues:
            if self.check() is not None:
                return
            if queue.peek()[0] <= self.w2 * self.anchor_queue.peek()[0]:
                self.expand_node(queue)
            else:
                self.expand_node(self.anchor_queue)

    def restart(self) -> bool:
        if self.w1 <= 1 or self.w2 <= 1:
            return False
        for queue in self.queues:
            queue.restart()
        self.w1 -= 2
        self.w2 -= 2
        return True
    
    def peek(self) -> Tuple[float, Util.Node]:
        if self.is_empty():
            raise IndexError("peek from an empty priority queue")
        return self.queue[0]
    
    def check(self) -> Optional[Util.Node]:
        for queue in self.queues:
            if queue.peek()[1].state == self.goal.state:
                return queue.peek()[1]
        return None
    
    def is_empty(self) -> bool:
        return self.anchor_queue.is_empty()
    

class PotentialQueue(PriorityQueue):
    def __init__(self, heuristic: Callable[[any, any], float], start: Util.Node, grid: any) -> None:
        self.budget: int = 150
        super().__init__(heuristic, start, grid)

    def insert(self, node: Util.Node, queue: List[Tuple[float, Util.Node]]) -> None:
        if (self.budget - node.g_score) <= 0:
            return
        priority = self.w1 * self.heuristic(node.state, node.goal.state) / (self.budget - node.g_score)
        heapq.heappush(queue, (priority, node))
    
    def restart(self) -> bool:
        if self.budget <= 0:
            return False
        if not super().restart():
            return False
        if self.check() is not None:
            self.budget = self.check().g_score - 10
        return True
