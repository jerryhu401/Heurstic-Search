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

def heuristic_manhattan(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def heuristic_euclidean(node, goal):
    return ((node[0] - goal[0]) ** 2 + (node[1] - goal[1]) ** 2) ** 0.5

def ara_star_with_animation(grid, start, goal, heuristic, initial_epsilon=2.5, epsilon_decay=0.1):
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}
    open_set = {start}
    closed_set = set()
    incons = set()

    epsilon = initial_epsilon

    fig, ax = plt.subplots(figsize=(10, 10))

    def update_visualization(current_node=None):
        grid_display = np.full_like(grid.grid, fill_value=0.0, dtype=float)

        for i in range(grid.height):
            for j in range(grid.width):
                if grid.grid[i, j] == -1:
                    grid_display[i, j] = 1.0  # Obstacles (black)

        ax.clear()
        ax.imshow(grid_display, cmap=plt.cm.binary, vmin=0, vmax=1)

        # Add grid weights as text
        for i in range(grid.height):
            for j in range(grid.width):
                if grid.grid[i, j] == -1:
                    ax.text(j, i, 'o', ha='center', va='center', color='red', fontsize=8)  # Obstacles
                else:
                    ax.text(j, i, str(grid.grid[i, j]), ha='center', va='center', color='black', fontsize=8)

        # Visualize open list (yellow), closed list (gray), and incons (orange)
        for node in open_set:
            ax.add_patch(plt.Rectangle((node[1] - 0.5, node[0] - 0.5), 1, 1, color='yellow', alpha=0.5))
        for node in closed_set:
            ax.add_patch(plt.Rectangle((node[1] - 0.5, node[0] - 0.5), 1, 1, color='gray', alpha=0.5))
        for node in incons:
            ax.add_patch(plt.Rectangle((node[1] - 0.5, node[0] - 0.5), 1, 1, color='orange', alpha=0.5))

        # Highlight current node in ImprovePath (green)
        if current_node:
            ax.add_patch(plt.Rectangle((current_node[1] - 0.5, current_node[0] - 0.5), 1, 1, color='lime', alpha=0.5))

        # Start and goal
        ax.add_patch(plt.Rectangle((start[1] - 0.5, start[0] - 0.5), 1, 1, color='blue', alpha=0.5))
        ax.add_patch(plt.Rectangle((goal[1] - 0.5, goal[0] - 0.5), 1, 1, color='red', alpha=0.5))

        ax.set_xticks([])
        ax.set_yticks([])
        ax.axis('off')
        plt.pause(0.1)

    def improve_path():
        """ImprovePath stops when the current best path to the goal is guaranteed 
        to be within the desired suboptimality bound ϵ. This happens when the 
        cost estimate of the best state in the open_list is greater than or equal 
        to the current cost of the goal state"""
        while open_list and g_score[goal] > open_list[0][0]:
            current_f, current_node = heapq.heappop(open_list)
            open_set.remove(current_node)
            closed_set.add(current_node)

            update_visualization(current_node)  # Highlight the current node being processed

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
                        """A node is considered locally inconsistent when its 
                        current g-value is lower than what was previously 
                        computed."""
                    came_from[neighbor] = current_node

    g_score[goal] = float('inf')

    while epsilon > 1.0:
        improve_path()
        epsilon = max(1.0, epsilon - epsilon_decay)
        for state in incons:
            heapq.heappush(open_list, (g_score[state] + epsilon * heuristic(state, goal), state))
            open_set.add(state)
        incons.clear()
        closed_set.clear()

    # Reconstruct the path
    if g_score[goal] < float('inf'):
        path = []
        current = goal
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()

        for (x, y) in path:
            if (x, y) != start and (x, y) != goal:
                ax.add_patch(plt.Rectangle((y - 0.5, x - 0.5), 1, 1, color='green', alpha=0.5))
        plt.pause(1)
        return path

    plt.pause(1)
    return None

if __name__ == "__main__":
    width, height = 20, 20
    obstacle_prob = 0.3
    max_cost = 10
    connectivity = 8

    grid = Gridworld(width, height, obstacle_prob, max_cost, connectivity)

    start = (0, 0)
    goal = (height - 1, width - 1)

    while not grid.is_traversable(*start) or not grid.is_traversable(*goal):
        grid = Gridworld(width, height, obstacle_prob, max_cost, connectivity)

    path = ara_star_with_animation(grid, start, goal, heuristic=heuristic_manhattan)

    if path:
        print("Path found:", path)
    else:
        print("No path found!")
