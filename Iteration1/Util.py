import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import logging
import heapq
from typing import Optional, Tuple, List, Dict, Set


class PQ:
    def __init__(self) -> None:
        self.queue: List[Tuple[int, int, object]] = []
        self.count: int = 0

    def push(self, node: object, priority: int) -> None:
        heapq.heappush(self.queue, (priority, self.count, node))
        self.count += 1

    def peek(self) -> Tuple[int, int, object]:
        return self.queue[0]

    def pop(self) -> object:
        return heapq.heappop(self.queue)[-1]

    def isEmpty(self) -> bool:
        return len(self.queue) == 0


class PQWithUpdate:
    def __init__(self) -> None:
        self.heap: List[Tuple[int, int, object]] = []
        self.count: int = 0
        self.size: int = 0
        self.entry_finder: Dict[object, List] = {}
        self.REMOVED: str = "<removed-task>"
        self.log_filename: str = "queue_log.txt"

        open(self.log_filename, "w").close()  # wipes content

        logging.basicConfig(
            filename=self.log_filename,
            level=logging.INFO,
            format="%(asctime)s - %(message)s"
        )

    def peek(self) -> Optional[Tuple[int, int, object]]:
        while self.heap:
            priority, count, task = self.heap[0]
            if task is not self.REMOVED:
                return priority, count, task
            heapq.heappop(self.heap)
        return None

    def isEmpty(self) -> bool:
        return self.size == 0

    def push(self, item: object, priority: int) -> None:
        entry = [priority, self.count, item]
        heapq.heappush(self.heap, entry)
        self.entry_finder[item] = entry
        self.count += 1
        self.size += 1

    def pop(self) -> object:
        while self.heap:
            priority, count, item = heapq.heappop(self.heap)
            if item is not self.REMOVED:
                del self.entry_finder[item]
                self.size -= 1
                return item
        raise KeyError("pop from an empty priority queue")

    def update(self, item: object, priority: int) -> None:
        val = self.entry_finder.get(item, 0)
        if val != 0:
            p, c, i = val
            if p > priority:
                entry = self.entry_finder.pop(i)
                entry[-1] = self.REMOVED
                self.size -= 1
                self.push(item, priority)
        else:
            self.push(item, priority)

    def log_queue(self) -> None:
        queue_elements: Set[object] = {entry[2] for entry in self.heap if entry[2] != self.REMOVED}

        with open(self.log_filename, "a") as log_file:
            log_file.write(f"Current Queue Set: {queue_elements}\n")

        logging.info(f"Priority queue contents logged as set: {queue_elements}")


class Node:
    def __init__(self, state: Tuple[int, int], parent: Optional["Node"], g_score: int, goal: Tuple[int, int]) -> None:
        self.state: Tuple[int, int] = state
        self.parent: Optional["Node"] = parent
        self.g_score: int = g_score
        self.goal: Tuple[int, int] = goal

    def __hash__(self) -> int:
        if self.parent is None:
            return hash(self.state) + hash(self.g_score)
        return hash(self.state) + hash(self.g_score) + hash(self.parent.state)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Node) and self.state == other.state

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other: "Node") -> bool:
        return self.g_score < other.g_score

    def __gt__(self, other: "Node") -> bool:
        return self.g_score > other.g_score

class Gridworld:
    def __init__(self, width: int, height: int, obstacle_prob: float, max_cost: int, connectivity: int) -> None:
        self.width: int = width
        self.height: int = height
        self.grid: np.ndarray = np.random.randint(1, max_cost + 1, (height, width))
        self.connectivity: int = connectivity
        self.grid[np.random.rand(height, width) < obstacle_prob] = 0
        self.log_filename: str = "grid_log.txt"

        open(self.log_filename, "w").close()

        logging.basicConfig(
            filename=self.log_filename,
            level=logging.INFO,
            format="%(asctime)s - %(message)s"
        )

    def is_within_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.height and 0 <= y < self.width

    def is_traversable(self, x: int, y: int) -> bool:
        return self.is_within_bounds(x, y) and self.grid[x, y] != 0

    def expand_node(self, node: Node) -> List["Node"]:
        x, y = node.state
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        if self.connectivity == 8:
            directions.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)])

        result: List[Node] = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.is_traversable(nx, ny):
                result.append(Node((nx, ny), node, node.g_score + self.grid[x][y], node.goal))

        return result

    def draw_grid(self, paths: List[List[Tuple[int, int]]], costs: List[int]) -> None:
        if not paths:
            raise ValueError("No paths provided.")

        num_paths: int = len(paths)
        fig, axes = plt.subplots(1, num_paths, figsize=(10 * num_paths, 10))
        if num_paths == 1:
            axes = [axes]

        colors = plt.cm.viridis(np.linspace(1, 0, 11))
        colors[0] = [0, 0, 0, 1]
        cmap = mcolors.ListedColormap(colors)
        bounds = np.linspace(0, np.max(self.grid), 11)
        norm = mcolors.BoundaryNorm(bounds, cmap.N)

        for i, (ax, path) in enumerate(zip(axes, paths)):
            cost = costs[i]
            grid_display = np.copy(self.grid).astype(float)
            img = ax.imshow(grid_display, cmap=cmap, norm=norm)

            if path:
                path_x = [x for x, y in path]
                path_y = [y for x, y in path]
                ax.plot(path_y, path_x, color="red", linewidth=2, marker="o", markersize=5, markerfacecolor="red")

            ax.set_xticks([])
            ax.set_yticks([])
            ax.axis("off")
            ax.set_title(f"Path Cost: {cost}")

        plt.colorbar(img, ax=axes, label="Traversal Cost", orientation="vertical")
        plt.show()

    def path_exists(self, start: Tuple[int, int], goal: Tuple[int, int]) -> bool:
        open_list = PQWithUpdate()
        open_list.push(start, 1)
        closed_set: Set[Tuple[int, int]] = set()

        while not open_list.isEmpty():
            current_node = open_list.pop()
            closed_set.add(current_node.state)

            if current_node.state == goal:
                return True

            for neighbor in self.expand_node(current_node):
                if neighbor.state not in closed_set:
                    open_list.update(neighbor, 1)

        return False
    
    def log(self, elems, message): 
        with open(self.log_filename, "a") as log_file:
            log_file.write(f"{message} {elems}\n")
