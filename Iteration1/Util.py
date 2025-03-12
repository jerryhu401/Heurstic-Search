import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import logging
import heapq

class PQ:
    def __init__(self):
        self.queue = []
        self.count = 0

    def push(self, node, priority):
        heapq.heappush(self.queue, (priority, self.count, node))
        self.count += 1

    def peek(self):
        return self.queue[0]
    
    def pop(self):
        return heapq.heappop(self.queue)[-1]

    def isEmpty(self):
        return len(self.queue) == 0




class PQWithUpdate:
    def __init__(self):
        self.heap = []
        self.count = 0
        self.size = 0
        self.entry_finder = {}
        self.REMOVED = '<removed-task>' 
        self.log_filename = "queue_log.txt"

        open(self.log_filename, "w").close() #wipes content

        logging.basicConfig(
            filename=self.log_filename,
            level=logging.INFO,
            format="%(asctime)s - %(message)s"
        )

    def peek(self):
        while self.heap:
            priority, count, task = self.heap[0]
            if task is not self.REMOVED:
                return priority, count, task
            heapq.heappop(self.heap)
        return None

    def isEmpty(self):
        return self.size == 0

    def push(self, item, priority):
        entry = [priority, self.count, item]
        heapq.heappush(self.heap, entry)
        self.entry_finder[item] = entry
        self.count += 1
        self.size += 1
    
    def pop(self):
        while self.heap:
            priority, count, item = heapq.heappop(self.heap)
            if item is not self.REMOVED:
                del self.entry_finder[item]
                self.size -= 1
                return item
        raise KeyError('pop from an empty priority queue')

    def update(self, item, priority):
        val = self.entry_finder.get(item, 0)
        if val != 0:
            [p, c, i] = val
            if p > priority:
                entry = self.entry_finder.pop(i)
                entry[-1] = self.REMOVED
                self.size -= 1
                PQWithUpdate.push(self, item, priority)
        else:
            PQWithUpdate.push(self, item, priority)

    def log_queue(self):
        queue_elements = {entry[2] for entry in self.heap if entry[2] != self.REMOVED}
        
        with open(self.log_filename, "a") as log_file:
            log_file.write(f"Current Queue Set: {queue_elements}\n")
        
        logging.info(f"Priority queue contents logged as set: {queue_elements}")

class Node:
    def __init__(self, state, parent, g_score, goal):
        self.state = state
        self.parent = parent
        self.g_score = g_score
        self.goal = goal

    def __hash__(self):
        if self.parent == None:
            return hash(self.state) + hash(self.g_score)
        return hash(self.state) + hash(self.g_score) + hash(self.parent.state)

    def __eq__(self, other):
        return other != None and self.state == other.state

    def __ne__(self, other):
        return other == None or self.state != other.state
    
    def __lt__(self, other):
        return self.g_score < other.g_score

    def __gt__(self, other):
        return self.g_score > other.g_score
    
    def expand_node(self, grid):
        x, y = self.state
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        if grid.connectivity == 8:
            directions.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)]) 

        result = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if grid.is_traversable(nx, ny):
                result.append(Node((nx, ny), self, self.g_score + grid.grid[x][y], self.goal))

        return result

class Gridworld:
    def __init__(self, width, height, obstacle_prob, max_cost, connectivity):
        self.width = width
        self.height = height
        self.grid = np.random.randint(1, max_cost + 1, (height, width))
        self.connectivity = connectivity
        self.grid[np.random.rand(height, width) < obstacle_prob] = 0
        self.log_filename = "grid_log.txt"

        open(self.log_filename, "w").close()

        logging.basicConfig(
            filename=self.log_filename,
            level=logging.INFO,
            format="%(asctime)s - %(message)s"
        )

    def is_within_bounds(self, x, y):
        return 0 <= x < self.height and 0 <= y < self.width
    
    def is_traversable(self, x, y):
        return self.is_within_bounds(x, y) and self.grid[x, y] != 0

    def draw_grid(self, paths=None, costs=None):
        if paths is None or len(paths) == 0:
            raise ValueError("No paths provided.")
        
        num_paths = len(paths)
        fig, axes = plt.subplots(1, num_paths, figsize=(10 * num_paths, 10))
        if num_paths == 1:
            axes = [axes]
        
        colors = plt.cm.viridis(np.linspace(1, 0, 11))
        colors[0] = [0, 0, 0, 1]
        cmap = mcolors.ListedColormap(colors)
        bounds = np.linspace(0, np.max(self.grid), 11)
        norm = mcolors.BoundaryNorm(bounds, cmap.N)
        
        i = 0
        for ax, path in zip(axes, paths):
            cost = costs[i]
            i += 1
            grid_display = np.copy(self.grid).astype(float)
            img = ax.imshow(grid_display, cmap=cmap, norm=norm)
            
            if path:
                self.log(path, "Path:")
                path_x = [x for x, y in path]
                path_y = [y for x, y in path]
                ax.plot(path_y, path_x, color='red', linewidth=2, marker='o', markersize=5, markerfacecolor='red')
            
            ax.set_xticks([])
            ax.set_yticks([])
            ax.axis('off')
            ax.set_title("Path Cost: " + str(cost))
        
        plt.colorbar(img, ax=axes, label='Traversal Cost', orientation='vertical')
        plt.show()


    def path_exists(self, start, goal):
        open_list = PQWithUpdate()
        open_list.push((start), 1)
        closed_set = set()

        while not open_list.isEmpty():
            current_node = open_list.pop()
            closed_set.add(current_node.state)

            if current_node.state == goal:
                return True

            for neighbor in current_node.expand_node(self):

                if neighbor.state not in closed_set:
                    h_score = 1
                    open_list.update((neighbor), h_score)

        return False
    
    def log(self, elems, message): 
        with open(self.log_filename, "a") as log_file:
            log_file.write(f"{message} {elems}\n")