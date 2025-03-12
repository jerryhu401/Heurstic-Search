import math
import heapq
from typing import Callable, List, Dict, Set, Tuple, Optional
import Util as Util

def g_score_DC(original: Util.Node, node: Util.Node) -> bool:
    return original.g_score <= node.g_score

class DominanceCheck():
    def __init__(self, dominate: Callable[[Util.Node, Util.Node], bool]) -> None:
        self.open: Set[Util.Node] = set()
        self.incons: Set[Util.Node] = set()
        self.nodes: Dict[str, Util.Node] = dict()
        self.closed: Set[str] = set()
        self.dominate = dominate

    def insert(self, node: Util.Node) -> None:
        self.open.add(node)

    def expand(self, node: Util.Node) -> None:
        self.open.remove(node)
        self.closed.add(node.state)

    def is_dominated(self, node: Util.Node) -> bool:
        og = self.nodes.get(node.state, None)
        if og is None or not self.dominate(og, node):
            self.nodes[node.state] = node
            if node.state not in self.closed:
                self.insert(node)
                return False
            else:
                self.incons.add(node)
        return True
    
    def clear(self) -> None:
        self.open = set()
        self.incons = set()
        self.closed = set()

    def get_incons(self) -> Set[Util.Node]:
        return self.incons
    
    def get_open(self) -> Set[Util.Node]:
        return self.open
    
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