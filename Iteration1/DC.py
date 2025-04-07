import math
import heapq
from typing import Callable, List, Dict, Set, Tuple, Optional
import Util as Util

def g_score_DC(original: Util.Node, node: Util.Node) -> bool:
    return original.g_score <= node.g_score

def key(node: Util.Node) -> str:
    return node.state

class DominanceCheck():
    #key function for node to not use state
    def __init__(self, dominate: Callable[[Util.Node, Util.Node], bool], getKey = key) -> None:
        self.incons = []
        self.keyToNode: Dict[str, Util.Node] = dict()
        self.dominate = dominate
        self.getKey = getKey 


    def insert(self, node: Util.Node) -> None: #rename this to insert
        key = self.getKey(node)
        self.keyToNode[key] = node 

    def is_dominated(self, node: Util.Node) -> bool:
        #use code base logic
        #DC does not care about open 
        key = self.getKey(node)
        if key in self.keyToNode:
            existingNode = self.keyToNode[key]
            if not self.dominate(existingNode, node):
                self.incons.append(node)
            return True
        return False
    
    def clear(self) -> None:
        self.incons = []
        self.keyToNode = dict()

    def get_incons(self) -> Set[Util.Node]:
        return self.incons
    
    def get_open(self) -> Set[Util.Node]:
        return list(self.keyToNode.values())
    
    def copy(self) -> 'DominanceCheck':
        return DominanceCheck(self.dominate)
    
class MultiDomianceCheck():
    def __init__(self, dominate: Callable[[Util.Node, Util.Node], bool], num_inads: int, w2: int = 10, e: int = 2) -> None:
        self.open_anchor: Set[Util.Node] = set()
        self.incons_anchor: Set[Util.Node] = set()
        self.closed_anchor: Set[str] = set()
        self.open_inad: List[Set[Util.Node]] = [set() for _ in range(num_inads)]
        self.incons_inad: Set[Util.Node] = set()
        self.closed_inad: Set[str] = set()
        self.nodes: Dict[str, Util.Node] = dict()
        self.num_inads = num_inads
        self.w2 = w2
        self.e = e
        self.dominate = dominate
    
    def insert_anchor(self, node: Util.Node) -> None:
        self.open_anchor.add(node)

    def expand_anchor(self, node: Util.Node) -> None:
        self.open_anchor.remove(node)
        self.closed_anchor.add(node.state)

    def insert_inad(self, node: Util.Node, i: int) -> None:
        self.open_inad[i].add(node)

    def expand_inad(self, node: Util.Node, i: int) -> None:
        self.open_inad[i].remove(node)
        self.closed_inad.add(node.state)

    def clear(self) -> None:
        self.open_anchor = set()
        self.incons_anchor = set()
        self.closed_anchor = set()
        self.open_inad = [set() for _ in range(self.num_inads)]
        self.incons_inad = set()
        self.closed_inad = set()
        self.w2 = max(self.w2 - self.e, 1)