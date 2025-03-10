import math
import heapq
from typing import Callable, List, Dict, Set, Tuple, Optional
import Util

def g_score_DC(original, node):
    return original.g_score <= node.g_score

class DominanceCheck():
    def __init__(self, dominate):
        self.open = set()
        self.incons = set()
        self.nodes = dict()
        self.closed = set()
        self.dominate = dominate

    def insert(self, node):
        self.open.add(node)

    def expand(self, node):
        self.open.remove(node)
        self.closed.add(node.state)

    def is_dominated(self,node):
        og = self.nodes.get(node.state, None)
        if og == None or not self.dominate(og, node):
            self.nodes[node.state] = node
            if node.state not in self.closed:
                self.insert(node)
                return False
            else:
                self.incons.add(node)
        return True
    
    def clear(self):
        self.open = set()
        self.incons = set()
        self.closed = set()

    def get_incons(self):
        return self.incons
    
    def get_open(self):
        return self.open
