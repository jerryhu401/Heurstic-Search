import math
import heapq
from typing import Callable, List, Dict, Set, Tuple, Optional
import Util

class DominanceCheck():
    def __init__(self, dominate):
        self.open = set()
        self.incons = set()
        self.nodes = dict()
        self.dominate = dominate

    def insert(self, node):
        self.nodes[node.state] = node
        self.open.add(node)

    def expand(self, node):
        self.nodes[node.state] = node
        self.open.remove(node)

    def is_dominated(self,node):
        state = node.state
        if state in self.nodes:
            original = self.nodes[state]
            if not self.dominate(original, node):
                self.nodes[state] = node
                self.incons.add(original)
            return True
        self.open.add(node)
        return False
    
    def clear(self):
        self.open = set()
        self.incons = set()
        self.nodes = dict()

    def get_incons(self):
        return self.incons
    
    def get_open(self):
        return self.open
