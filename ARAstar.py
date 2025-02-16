import heapq
import random
import matplotlib.pyplot as plt
import numpy as np

class Gridworld:
    def __init__(self, width, height, obstacle_prob, max_cost, connectivity):
        self.width = width
        self.height = height
        self.grid = np.random.randint(1, max_cost + 1, (height, width))
        self.connectivity = connectivity

        # Add obstacles
        for i in range(height):
            for j in range(width):
                if random.random() < obstacle_prob:
                    self.grid[i, j] = -1  # -1 represents an obstacle

    def is_within_bounds(self, x, y):
        return 0 <= x < self.height and 0 <= y < self.width

    def is_traversable(self, x, y):
        return self.is_within_bounds(x, y) and self.grid[x, y] != -1

    def expand_node(self, node):
        x, y = node
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        if self.connectivity == 8:
            directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        result = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.is_traversable(nx, ny):
                result.append((nx, ny))

        return result

    def draw_grid(self, path=None, start=None, goal=None, open_list=None, closed_list=None):
        fig, ax = plt.subplots(figsize=(10, 10))
        grid_display = np.full_like(self.grid, fill_value=0.0, dtype=float)  # All cells white

        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i, j] == -1:
                    grid_display[i, j] = 1.0  # Obstacles (black)

        ax.imshow(grid_display, cmap=plt.cm.binary, vmin=0, vmax=1)  # Binary colormap (0 -> white, 1 -> black)

        # Overlay path cells with green
        if path:
            for (x, y) in path:
                if (x, y) != start and (x, y) != goal:
                    ax.add_patch(plt.Rectangle((y - 0.5, x - 0.5), 1, 1, color='green', alpha=0.5))  # Path in green
                elif (x, y) == start:
                    ax.add_patch(plt.Rectangle((y - 0.5, x - 0.5), 1, 1, color='blue', alpha=0.5))  # start in blue
                else:
                    ax.add_patch(plt.Rectangle((y - 0.5, x - 0.5), 1, 1, color='red', alpha=0.5))  # goal in red

        # Overlay open list cells with yellow
        if open_list:
            for (x, y) in open_list:
                ax.add_patch(plt.Rectangle((y - 0.5, x - 0.5), 1, 1, color='yellow', alpha=0.5))

        # Overlay closed list cells with gray
        if closed_list:
            for (x, y) in closed_list:
                ax.add_patch(plt.Rectangle((y - 0.5, x - 0.5), 1, 1, color='gray', alpha=0.5))

        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i, j] == -1:
                    ax.text(j, i, 'o', ha='center', va='center', color='red', fontsize=8)  # Obstacles
                else:
                    ax.text(j, i, int(self.grid[i, j]), ha='center', va='center', color='black', fontsize=8)

        ax.set_xticks([])
        ax.set_yticks([])
        ax.axis('off')
        plt.show()

def heuristic_manhattan(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def heuristic_euclidean(node, goal):
    return ((node[0] - goal[0]) ** 2 + (node[1] - goal[1]) ** 2) ** 0.5

def ara_star(grid, start, goal, heuristic, initial_epsilon=2.5, epsilon_decay=0.1):
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}
    open_set = {start}
    closed_set = set()
    incons = set()

    epsilon = initial_epsilon
    g_score[goal] = float('inf')

    def improve_path():
        while open_list and g_score[goal] > open_list[0][0]:
            current_f, current_node = heapq.heappop(open_list)
            open_set.remove(current_node)
            closed_set.add(current_node)

            for neighbor in grid.expand_node(current_node):
                tentative_g = g_score[current_node] + grid.grid[neighbor]
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + epsilon * heuristic(neighbor, goal)
                    if neighbor not in open_set and neighbor not in closed_set:
                        heapq.heappush(open_list, (f_score, neighbor))
                        open_set.add(neighbor)
                    elif neighbor in closed_set:
                        incons.add(neighbor)
                    came_from[neighbor] = current_node

    paths = []
    open_sets = []
    closed_sets = []

    while epsilon > 1.0:
        improve_path()
        epsilon = max(1.0, epsilon - epsilon_decay)
        for state in incons:
            heapq.heappush(open_list, (g_score[state] + epsilon * heuristic(state, goal), state))
            open_set.add(state)
        incons.clear()

        if g_score[goal] < float('inf'):
            path = []
            current = goal
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            paths.append(path)
            open_sets.append(set(open_set))
            closed_sets.append(set(closed_set))

    return paths[-1] if paths else None, open_sets[-1] if open_sets else set(), closed_sets[-1] if closed_sets else set()

if __name__ == "__main__":
    width, height = 20, 20
    grid = Gridworld(width, height, 0.3, 10, connectivity=8)

    start = (0, 0)
    goal = (height - 1, width - 1)

    while not grid.is_traversable(*start) or not grid.is_traversable(*goal):
        grid = Gridworld(width, height, 0.3, 10, connectivity=8)

    path, open_set, closed_set = ara_star(grid, start, goal, heuristic=heuristic_manhattan)

    if path:
        print("Path found:", path)
        grid.draw_grid(path=path, start=start, goal=goal, open_list=open_set, closed_list=closed_set)
    else:
        print("No path found!")
