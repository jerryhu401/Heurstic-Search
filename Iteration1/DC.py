import math
import heapq
from typing import Callable, List, Dict, Set, Tuple, Optional
import Util as Util

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
    
    def copy(self):
        return DominanceCheck(self.dominate)
    
class MultiDomianceCheck():
    def __init__(self, dominate, num_inads, w2 = 10, e = 2):
        self.open_anchor = set()
        self.incons_anchor = set()
        self.closed_anchor = set()
        self.open_inad = [set() for _ in range(num_inads)]
        self.incons_inad = set()
        self.closed_inad = set()
        self.nodes = dict()
        self.num_inads = num_inads
        self.w2 = w2
        self.e = e
        self.dominate = dominate
    
    def insert_anchor(self, node):
        self.open_anchor.add(node)

    def expand_anchor(self, node):
        self.open_anchor.remove(node)
        self.closed_anchor.add(node.state)

    def insert_inad(self, node, i):
        self.open_inad[i].add(node)

    def expand_inad(self, node, i):
        self.open_inad[i].remove(node)
        self.closed_inad.add(node.state)

    def clear(self):
        self.open_anchor = set()
        self.incons_anchor = set()
        self.closed_anchor = set()
        self.open_inad = [set() for _ in range(self.num_inads)]
        self.incons_inad = set()
        self.closed_inad = set()
        self.w2 = max(self.w2 - self.e, 1)

    
