import math
import Util
import heuristics as heu

def ARA_star(grid, start, goal, h, weight, epsilon, time):
    open_set = set()
    open_set.add(start.state)
    open_list = Util.PQ()
    open_list.push((start), 0)
    closed_set = set()
    incons_set = set()
    best_path = None
    best_cost = math.inf
    g_scores = {start.state: 0}
    g_scores[goal] = float('inf')

    while weight >= 1 and time > 0:
        time -= 1
        current_node = improved_A_star(grid, start, goal, h, weight, open_list, g_scores, closed_set, incons_set, open_set)
        if current_node == None:
            break

        if g_scores[goal] < float('inf'):
            path = []
            path_cost = current_node.g_score
            while current_node != start:
                path.append(current_node.state)
                current_node = current_node.parent
            path.append(start.state)
            path.reverse()
            if path_cost < best_cost:
                best_path = path
                best_cost = path_cost
        weight = max(1, weight - epsilon)
        for node in incons_set:
            open_list.push((node), g_scores[node.state] + weight * h(node.state, goal))
            open_set.add(node.state)
        incons_set.clear()
        closed_set.clear()
    
    return best_path, open_set, closed_set, best_cost

def improved_A_star(grid, start, goal, h, weight, open_list, g_scores, closed_set, incons_set, open_set):
    print("here")
    current_node = None
    while not open_list.isEmpty() and g_scores[goal]>open_list.peek()[0]:
        current_node = open_list.pop()
        closed_set.add(current_node.state)
        open_set.remove(current_node.state)

        for neighbor in current_node.expand_node(grid):
            g_score = neighbor.g_score
            
            if neighbor.state not in closed_set or g_score < g_scores[neighbor.state]:
                g_scores[neighbor.state] = g_score
                f_score = g_score + weight * h(neighbor.state, goal)
                open_list.update((neighbor), f_score)
                open_set.add(neighbor.state)
                
                if neighbor.state in closed_set:
                    incons_set.add(neighbor)
    
    return current_node

if __name__ == "__main__":
    width, height = 20, 20
    grid = Util.Gridworld(width, height, 0.3, 10, connectivity=8)
    
    start = Util.Node((0, 0), None, 0)
    goal = (height - 1, width - 1)
    weight = 10
    epsilon = 1
    h = heu.heuristic_manhattan
    time = 10

    while not grid.path_exists(start, goal):
        grid = Util.Gridworld(width, height, 0.3, 10, connectivity=8)
    
    best_path, best_open, best_close, best_cost = ARA_star(grid, start, goal, h, weight, epsilon, time)
    
    if best_path:
        print("Best Path Found:", best_path)
        print("Path Cost:", best_cost)
        grid.draw_grid(best_path, start.state, goal, best_open, best_close)
    else:
        print("No path found")
        grid.draw_grid(best_path, start.state, goal, best_open, best_close)
