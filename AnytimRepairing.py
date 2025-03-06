import Util
import math
import heapq
import heuristics

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
        self.g_scores[goal.state] = math.inf
    
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

def reconstruct_path(node, start, current):
    path = []
    while current != start:
        path.append(current.state)
        current = current.parent
    path.append(start.state)
    path.reverse()
    return path

def ARA(start, open):
    paths = []
    costs = []
    while open.restart():
        goal = None
        while not open.is_empty():
            if open.peek()[1].state == open.goal.state:
                goal = open.peek()[1]
                break
            open.iterate_queues()
        if goal != None:
            paths.append(reconstruct_path(goal, start, goal))
            costs.append(goal.g_score)
    return paths, costs

if __name__ == "__main__":
    width, height = 20, 20
    grid = Util.Gridworld(width, height, 0.3, 10, connectivity=8)

    goal = Util.Node((height - 1, width - 1), None, math.inf, None)
    start = Util.Node((0, 0), None, 0, goal)


    while not (grid.path_exists(start, goal.state) and grid.is_traversable(*(start.state)) and grid.is_traversable(*(goal.state))):
        grid = Util.Gridworld(width, height, 0.3, 10, connectivity=8)

    queue = PriorityQueue(heuristics.heuristic_euclidean, start, grid)
    res = ARA(start, queue)
    
    
    paths, costs = res

    if len(paths)>0:
        print("Best Path Found:", paths[-1])
        print("Path Cost:", costs[-1])
        grid.draw_grid(paths, costs)
    else:
        print("No path found")
        grid.draw_grid(None)