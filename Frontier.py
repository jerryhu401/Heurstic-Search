import math
import heapq
import Priority as P
import Util
import heuristics
import DC

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
    def __init__(self, queue, DC, priority, grid):
        self.heap = []
        self.queue = queue
        self.DC = DC
        self.priority = priority
        self.grid = grid

    def insert(self, node):
        priority = self.priority(node)
        self.queue.push(priority, node)
        self.DC.insert(node)

    def expand_node(self):
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
            self.insert(node)
        
        self.priority.update()
        return True

def ARA(start, goal_check, frontier):
    frontier.insert(start)
    paths = []
    costs = []
    while frontier.restart():
        curr = None
        while not frontier.is_empty():
            curr = frontier.peek()
            if goal_check(curr):
                paths.append(reconstruct_path(start, curr))
                costs.append(curr.g_score)
                break
            frontier.expand_node()
    return paths, costs

def reconstruct_path(start, current):
    path = []
    while current != start:
        path.append(current.state)
        if current.parent is None:
            break  
        current = current.parent
    path.append(start.state)
    path.reverse()
    return path

if __name__ == "__main__":
    width = 20
    height = 20
    grid = Util.Gridworld(width, height, 0.3, 10, connectivity=8)

    goal = Util.Node((height - 1, width - 1), None, math.inf, None)
    start = Util.Node((0, 0), None, 0, goal)

    while not (grid.path_exists(start, goal.state) and grid.is_traversable(*start.state) and grid.is_traversable(*goal.state)):
        grid = Util.Gridworld(width, height, 0.3, 10, connectivity=8)

    w1 = 10
    e = 2
    time = 5
    h = [
        heuristics.heuristic_euclidean,
        heuristics.heuristic_manhattan,
        heuristics.heuristic_chebyshev,
        heuristics.heuristic_octile,
    ]

    p = [P.Priority(h[i], w1, e, time) for i in range(len(h))]
    dc = DC.DominanceCheck(DC.g_score_DC)
    queue = PriorityQueue()
    frontier = GenericFrontier(queue, dc, p[0], grid)
    def goal_check(node):
        return node.state == goal.state

    res = ARA(start, goal_check, frontier)

    paths, costs = res

    if len(paths) > 0:
        print("Best Path Found:", paths[-1])
        print("Path Cost:", costs[-1])
        grid.draw_grid(paths, costs)
    else:
        print("No path found")
        grid.draw_grid(None)