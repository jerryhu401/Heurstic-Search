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

