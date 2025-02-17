import math

def heuristic_manhattan(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def heuristic_euclidean(node, goal):
    return ((node[0] - goal[0]) ** 2 + (node[1] - goal[1]) ** 2) ** 0.5

def heuristic_chebyshev(node, goal):
    return max(abs(node[0] - goal[0]), abs(node[1] - goal[1]))

def heuristic_octile(node, goal):
    dx = abs(node[0] - goal[0])
    dy = abs(node[1] - goal[1])
    return (dx + dy) + (math.sqrt(2) - 2) * min(dx, dy)

def linear(C, h_n, g_n):
    if h_n == 0:
        return 0
    if ((C - g_n) <= 0):
        return math.inf
    return h_n/(C - g_n)

def priority_manhattan(node, goal, g, w):
    w1, w2 = w
    return g + w1*heuristic_manhattan(node, goal)

def priority_euclidean(node, goal, g, w):
    w1, w2 = w
    return g + w1*heuristic_euclidean(node, goal)

def priority_chebyshev(node, goal, g, w):
    w1, w2 = w
    return g + w1*heuristic_chebyshev(node, goal)

def priority_octile(node, goal, g, w):
    w1, w2 = w
    return g + w1*heuristic_octile(node, goal)

def potential_manhattan(node, goal, g, w):
    w1, budget = w
    h_score = heuristic_manhattan(node, goal)
    potential = linear(budget, h_score, g)
    return w1*potential

def potential_euclidean(node, goal, g, w):
    w1, budget = w
    h_score = heuristic_euclidean(node, goal)
    potential = linear(budget, h_score, g)
    return w1*potential

def potential_chebyshev(node, goal, g, w):
    w1, budget = w
    h_score = heuristic_chebyshev(node, goal)
    potential = linear(budget, h_score, g)
    return w1*potential

def potential_octile(node, goal, g, w):
    w1, budget = w
    h_score = heuristic_octile(node, goal)
    potential = linear(budget, h_score, g)
    return w1*potential
