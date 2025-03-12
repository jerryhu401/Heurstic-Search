import math
import Queues as Q
import Priority as P
import Util as Util
import heuristics as heuristics
import DC as DC

class GenericFrontier():
    def __init__(self, queue, DC, priority, grid):
        self.queue = queue
        self.DC = DC
        self.priority = priority
        self.grid = grid

    def insert(self, node):
        priority = self.priority(node)
        self.queue.push(priority, node)
        self.DC.insert(node)

    def remove(self):
        node = self.queue.pop()
        self.DC.expand(node)
        return node

    def expand_node(self, node):
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


class MultiFrontier():
    def __init__(self, queues, DC, priorities, grid, w2 = 5, e = 1):
        self.anchor = GenericFrontier(queues[0], DC, priorities[0], grid)
        self.inads = []
        for i in range(1, len(priorities)):
            new = GenericFrontier(queues[i], DC.copy(), priorities[i], grid)
            self.inads.append(new)
        self.w2 = w2
        self.e = e
        self.index = 0
        
    def chooseFrontier(self):
        i = self.index
        return self.inads[i]
    
    def insert(self, node):
        self.anchor.insert(node)
        for F in self.inads:
            F.insert(node)

    def remove(self):
        F = self.chooseFrontier()
        if F.peek()[0] > self.w2 * self.anchor.peek()[0]:
            F = self.anchor
        else:
            self.index = (self.index + 1) % len(self.inads)
        node = F.remove()
        return node
    
    def expand_node(self, node):
        self.anchor.expand_node(node)
        for F in self.inads:
            F.expand_node(node)
    
    def peek(self):
        F = self.chooseFrontier()
        return F.peek()

    def is_empty(self):
        return self.anchor.is_empty()
    
    def restart(self):
        if not self.anchor.restart():
            print("2")
            return False
        for F in self.inads:
            if not F.restart():
                print("3")
                return False
        self.w2 = max(self.w2 - self.e, 1)
        self.index = 0
        return True
        
def ARA(start, goal_check, frontier):
    frontier.insert(start)
    paths = []
    costs = []
    while frontier.restart():
        curr = None
        while not frontier.is_empty():
            curr = frontier.peek()[1]
            if goal_check(curr):
                paths.append(reconstruct_path(start, curr))
                costs.append(curr.g_score)
                break
            node = frontier.remove()
            frontier.expand_node(node)
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
    t = 5
    h = [
        heuristics.heuristic_euclidean,
        heuristics.heuristic_manhattan,
        heuristics.heuristic_chebyshev,
        heuristics.heuristic_octile
    ]

    p = [P.Priority(h[i], w1, e, t) for i in range(len(h))]
    dc = DC.DominanceCheck(DC.g_score_DC)
    queue = Q.PriorityQueue()
    queues = [Q.PriorityQueue() for _ in range(len(h))]
    single = GenericFrontier(queue, dc, p[0], grid)
    multi = MultiFrontier(queues, dc, p, grid)
    def goal_check(node):
        return node.state == goal.state

    res = ARA(start, goal_check, multi)

    paths, costs = res

    if len(paths) > 0:
        print("Best Path Found:", paths[-1])
        print("Path Cost:", costs[-1])
        grid.draw_grid(paths, costs)
    else:
        print("No path found")
        grid.draw_grid(None)