import Util
import math

class Priority():
    def __init__(self, heuristic):
        self.heuristic = heuristic
        self.w1 = 1
        self.w2 = 1
        self.e = 0
        self.time = 1

    def valid(self):
        return self.w1 >= 1 and self.w2 >= 1 and self.time > 0
    
    def update(self, cost):
        self.w1 = max(self.w1 - self.e, 1)
        self.w2 -= max(self.w2 - self.e, 1)
        self.time -= 1

    def configure(self, w1, w2, e, time):
        self.w1 = w1
        self.w2 = w2
        self.e = e
        self.time = time

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
