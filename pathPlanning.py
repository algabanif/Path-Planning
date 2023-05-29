# Define the initial and goal states
import math
import time

start_state = (0, 0)  # Initial state represented as (x, y)
goal_state = (9, 9)  # Goal state represented as (x, y)


# Define the successor function
def get_successors(state):
    x, y = state
    successors = []

    # Generate all possible successors
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue  # Skip current state

            new_x = x + dx
            new_y = y + dy

            # Check if the successor is within the grid boundaries
            if 0 <= new_x < 10 and 0 <= new_y < 10:
                successors.append((new_x, new_y))

    return successors


class Node:
    def __init__(self, state, cost, heuristic):
        self.state = state
        self.cost = cost
        self.heuristic = heuristic
        self.total_cost = cost + heuristic
        self.parent = None

    def __lt__(self, other):
        return self.total_cost < other.total_cost

    def __eq__(self, other):
        return self.total_cost == other.total_cost

    def __gt__(self, other):
        return self.total_cost > other.total_cost
import heapq

fringe = []  # Priority queue for the fringe

def add_to_fringe(node):
    heapq.heappush(fringe, (node.total_cost, node))

def get_from_fringe():
    _, node = heapq.heappop(fringe)
    return node

def is_fringe_empty():
    return len(fringe) == 0

def heuristic(state, goal_state):
    x1, y1 = state
    x2, y2 = goal_state
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def get_cost(state, successor_state):
    x1, y1 = state
    x2, y2 = successor_state

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    if dx == 1 and dy == 1:
        return math.sqrt(2)
    else:
        return 1

def A_star_search(start_state, goal_state):
    # Create the start node
    start_node = Node(start_state, 0, heuristic(start_state, goal_state))
    add_to_fringe(start_node)

    while not is_fringe_empty():
        current_node = get_from_fringe()

        if current_node.state == goal_state:
            # Goal reached, construct the path
            path = []
            while current_node:
                path.append(current_node.state)
                current_node = current_node.parent
            path.reverse()
            return path

        successors = get_successors(current_node.state)
        for successor_state in successors:
            # Calculate the cost and heuristic for the successor
            successor_cost = current_node.cost + get_cost(current_node.state, successor_state)
            successor_heuristic = heuristic(successor_state, goal_state)

            # Create the successor node
            successor_node = Node(successor_state, successor_cost, successor_heuristic)
            successor_node.parent = current_node

            add_to_fringe(successor_node)

    # No path found
    return None
import random

grid_size = 10
obstacle_percentage = 10

obstacle_count = int(grid_size * grid_size * obstacle_percentage / 100)
obstacles = random.sample(range(grid_size * grid_size), obstacle_count)
grid = [[1 if i * grid_size + j in obstacles else 0 for j in range(grid_size)] for i in range(grid_size)]

# Call the A* search function
path = A_star_search(start_state, goal_state)
if path:
    print("Path found:", path)
else:
    print("No path found.")
problem_tests = 20
obstacle_percentages = range(10, 100, 10)

results = []

for obstacle_percentage in obstacle_percentages:
    total_time = 0
    worst_case = float('-inf')
    best_case = float('inf')

    for _ in range(problem_tests):
        # Generate a random grid with obstacles
        obstacle_count = int(grid_size * grid_size * obstacle_percentage / 100)
        obstacles = random.sample(range(grid_size * grid_size), obstacle_count)
        grid = [[1 if i * grid_size + j in obstacles else 0 for j in range(grid_size)] for i in range(grid_size)]

        # Measure the execution time
        start_time = time.time()
        path = A_star_search(start_state, goal_state)
        end_time = time.time()

        if path:
            execution_time = end_time - start_time
            total_time += execution_time
            worst_case = max(worst_case, execution_time)
            best_case = min(best_case, execution_time)

    average_time = total_time / problem_tests
    results.append((obstacle_percentage, average_time, worst_case, best_case))

# Print the results as a table
print("Obstacle %   |     Average Time     |     Worst Case     |    Best Case     |     Total cost     |     Path solution     |")
for result in results:
    print("{:<12} | {:<12} | {:<10} | {:<9}".format(*result) )

