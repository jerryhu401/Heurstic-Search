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


    def insert(self, node: Util.Node) -> None:
        key = self.getKey(node)
        self.keyToNode[key] = node 

    def is_dominated(self, node: Util.Node) -> bool:
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
    
