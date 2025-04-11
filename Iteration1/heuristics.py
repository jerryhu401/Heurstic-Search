import math
import Util as Util
from typing import Tuple

def heuristic_manhattan(node: Util.Node, goal: Util.Node) -> int:
    return abs(node.state[0] - goal.state[0]) + abs(node.state[1] - goal.state[1])

def heuristic_euclidean(node: Util.Node, goal: Util.Node) -> float:
    return ((node.state[0] - goal.state[0]) ** 2 + (node.state[1] - goal.state[1]) ** 2) ** 0.5

def heuristic_chebyshev(node: Util.Node, goal: Util.Node) -> int:
    return max(abs(node.state[0] - goal.state[0]), abs(node.state[1] - goal.state[1]))

def heuristic_octile(node: Util.Node, goal: Util.Node) -> float:
    dx = abs(node.state[0] - goal.state[0])
    dy = abs(node.state[1] - goal.state[1])
    return (dx + dy) + (math.sqrt(2) - 2) * min(dx, dy)

def linear(C: float, h_n: float, g_n: float) -> float:
    if h_n == 0:
        return 0
    if (C - g_n) <= 0:
        return math.inf
    return h_n / (C - g_n)
