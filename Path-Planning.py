import pygame
import math
import random

pygame.init()
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 60
GRID_WIDTH = 10
GRID_HEIGHT = 10
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Algorithm")
BLACK = (30, 30, 30)
WHITE = (220, 220, 220)
RED = (255, 60, 60)
GREEN = (75, 255, 75)
BLUE = (75, 75, 255)
GRAY = (160, 160, 160)
EMPTY = 0
OBSTACLE = 1
START = 2
END = 3
OPEN = 4
CLOSED = 5
PATH = 6
NO_PATH = 77
HORIZONTAL_VERTICAL_COST = 1
DIAGONAL_COST = 1.41
grid = [[EMPTY] * GRID_HEIGHT for _ in range(GRID_WIDTH)]
start_pos = (0, 9)
end_pos = (6, 0)
grid[start_pos[0]][start_pos[1]] = START
grid[end_pos[0]][end_pos[1]] = END

def generate_random_problem(obstacle_percentage):
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if (x, y) != start_pos and (x, y) != end_pos:
                grid[x][y] = EMPTY

    num_obstacles = int(GRID_WIDTH * GRID_HEIGHT * obstacle_percentage / 100)
    obstacle_coords = random.sample(range(GRID_WIDTH * GRID_HEIGHT), num_obstacles)
    for coord in obstacle_coords:
        x = coord // GRID_WIDTH
        y = coord % GRID_HEIGHT
        if (x, y) != start_pos and (x, y) != end_pos:
            grid[x][y] = OBSTACLE

def h_func(node_pos):
    dx = abs(node_pos[0] - end_pos[0])
    dy = abs(node_pos[1] - end_pos[1])
    return math.sqrt(dx ** 2 + dy ** 2)

def get_neighbors(node_pos, closed_set):
    x, y = node_pos
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            new_x = x + dx
            new_y = y + dy
            if new_x >= 0 and new_x < GRID_WIDTH and new_y >= 0 and new_y < GRID_HEIGHT:
                if dx == 0 or dy == 0:
                    cost = HORIZONTAL_VERTICAL_COST
                else:
                    cost = DIAGONAL_COST
                if (new_x, new_y) not in closed_set and grid[new_x][new_y] != OBSTACLE:
                    neighbors.append((new_x, new_y, cost))
    return neighbors


def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

def astar_algorithm():
    start_node = (start_pos[0], start_pos[1], 0, h_func(start_pos))
    open_set = {start_node}
    closed_set = set()
    global pathcost
    g_score = {start_node: 0}
    f_score = {start_node: start_node[3]}
    came_from = {}

    while open_set:
        current = min(open_set, key=lambda node: f_score[node])

        if (current[0], current[1]) == end_pos:
            path = reconstruct_path(came_from, current)
            for node in path:
                grid[node[0]][node[1]] = PATH
            print("Path cost:", g_score[current])
            pathcost = g_score[current]
            return True

        open_set.remove(current)
        closed_set.add((current[0], current[1]))

        neighbors = get_neighbors((current[0], current[1]), closed_set)
        if neighbors == NO_PATH:
            return NO_PATH

        for neighbor in neighbors:
            neighbor = (neighbor[0], neighbor[1], current[2] + neighbor[2], h_func((neighbor[0], neighbor[1])))
            if neighbor not in g_score or neighbor[2] < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = neighbor[2]
                f_score[neighbor] = neighbor[2] + neighbor[3]

                if neighbor[:2] != start_pos and neighbor[:2] != end_pos:
                    grid[neighbor[0]][neighbor[1]] = OPEN

                if neighbor not in open_set:
                    open_set.add(neighbor)
    return NO_PATH

def draw_grid():
    WIN.fill(BLACK)
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            cell_type = grid[x][y]
            color = WHITE
            if cell_type == OBSTACLE:
                color = BLACK
            elif cell_type == START:
                pygame.draw.circle(WIN, GREEN, (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2),
                                   GRID_SIZE // 4)
            elif cell_type == END:
                pygame.draw.circle(WIN, RED, (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2),
                                   GRID_SIZE // 4)
            elif cell_type == OPEN:
                color = BLUE
            elif cell_type == CLOSED:
                color = GRAY
            elif cell_type == PATH:
                color = GREEN
            elif cell_type == NO_PATH:
                color = RED
            pygame.draw.rect(WIN, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(WIN, BLACK, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
    pygame.display.update()

def main():
    running = True
    obstacle_counts = list(range(10, 100, 10))
    num_runs = 20

    for obstacle_count in obstacle_counts:
    
        path_found_counter = 0  
        total_path_cost = 0  
        best_path_cost = float('inf')  
        worst_path_cost = 0  
        for _ in range(num_runs):
            generate_random_problem(obstacle_count)
            draw_grid()
            
            path_found = astar_algorithm()
            draw_grid()
            pygame.time.delay(300)

            if path_found == NO_PATH:
                print("No path found")
                continue
            elif path_found:
                path_found_counter += 1
                path_cost = pathcost
                total_path_cost += path_cost
                if path_cost < best_path_cost:
                    best_path_cost = path_cost
                if  path_cost > worst_path_cost:
                    worst_path_cost = path_cost

        average_path_cost = total_path_cost / path_found_counter if path_found_counter > 0 else 0
    
        if path_found_counter == 0:

            best_path_cost = "No Path Found"
            average_path_cost = "No Path Found"       
            
        if path_found_counter == 20:                       
            print(f"Obstacle Count: {obstacle_count}")
            print(f"Path Found: {path_found_counter}/{num_runs}")
            print(f"Best Case: {best_path_cost}")
            print(f"Worst Case: {worst_path_cost}")
            print(f"Average Case: {average_path_cost}")
            print("")
        else:
            print(f"Obstacle Count: {obstacle_count}")
            print(f"Path Found: {path_found_counter}/{num_runs}")
            print(f"Best Case: {best_path_cost}")
            print(f"Worst Case: No Path Found")
            print(f"Average Case: {average_path_cost}")
            print("")
        
    pygame.quit()
    running = False

if __name__ == '__main__':
    main()

