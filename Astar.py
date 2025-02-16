import Util
import math

def heuristic_manhattan(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def heuristic_euclidean(node, goal):
    return ((node[0] - goal[0]) ** 2 + (node[1] - goal[1]) ** 2) ** 0.5

def A_star(grid, start, goal, h, weight):
    open_list = Util.PQ()
    open_list.push((start), 0)
    open_set = {start.state}
    closed_set = set()
    final_cost = None

    while not open_list.isEmpty():
        current_node = open_list.pop()
        open_set.remove(current_node.state)
        closed_set.add(current_node.state)

        if current_node.state == goal:
            path = []
            final_cost = current_node.g_score
            while current_node != start:
                path.append(current_node.state)
                current_node = current_node.parent
            path.append(start.state)
            path.reverse()
            return path, open_set, closed_set, final_cost

        for neighbor in current_node.expand_node(grid):
            g_score = neighbor.g_score

            if neighbor.state not in closed_set:
                h_score = h(neighbor.state, goal)
                f_score = g_score + weight*h_score
                open_list.update((neighbor), f_score)
                open_set.add(neighbor.state)

    return None, open_set, closed_set, None


if __name__ == "__main__":
    width, height = 20, 20
    grid = Util.Gridworld(width, height, 0.3, 10, connectivity=8)

    start = Util.Node((0, 0),None,0)
    goal = (height - 1, width - 1)

    while not grid.path_exists(start, goal):
        grid = Util.Gridworld(width, height, 0.3, 10, connectivity=8)

    path, open_set, closed_set, C = A_star(grid, start, goal, heuristic_manhattan, 1)

    if path:
        print(f"Path found:", path)
        grid.draw_grid(path=path, start=start.state, goal=goal, open_list=open_set, closed_list=closed_set)
    else:
        print("No path found")
        grid.draw_grid(path=path, start=start.state, goal=goal, open_list=open_set, closed_list=closed_set)
