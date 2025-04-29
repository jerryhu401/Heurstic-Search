import math
import heapq
from typing import Callable, List, Dict, Set, Tuple, Optional
import Util as Util
from abc import ABC, abstractmethod

# ---------- Utility Functions ----------

def g_score_DC(original: Util.AbstractNode, node: Util.AbstractNode) -> bool:
    return original.g_score <= node.g_score

def key(node: Util.AbstractNode) -> str:
    return node.state

# ---------- Abstract Class ----------

class AbstractDominanceCheck(ABC):
    @abstractmethod
    def insert(self, node: Util.AbstractNode) -> None: pass

    @abstractmethod
    def is_dominated(self, node: Util.AbstractNode) -> bool: pass

    @abstractmethod
    def clear(self) -> None: pass

    @abstractmethod
    def get_incons(self) -> Set[Util.AbstractNode]: pass

    @abstractmethod
    def get_open(self) -> Set[Util.AbstractNode]: pass

    @abstractmethod
    def copy(self) -> "AbstractDominanceCheck": pass

# ---------- Concrete Implementation ----------

class DominanceCheck(AbstractDominanceCheck):
    def __init__(self, dominate: Callable[[Util.AbstractNode, Util.AbstractNode], bool], getKey) -> None:
        self.incons: List[Util.AbstractNode] = []
        self.keyToNode: Dict[str, Util.AbstractNode] = dict()
        self.dominate = dominate
        self.getKey = getKey

    def insert(self, node: Util.AbstractNode) -> None:
        key = self.getKey(node)
        self.keyToNode[key] = node

    def is_dominated(self, node: Util.AbstractNode) -> bool:
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

    def get_incons(self) -> Set[Util.AbstractNode]:
        return self.incons

    def get_open(self) -> Set[Util.AbstractNode]:
        return list(self.keyToNode.values())

    def copy(self) -> "DominanceCheck":
        return DominanceCheck(self.dominate, self.getKey)
