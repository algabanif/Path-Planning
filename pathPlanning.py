import heapq
from math import sqrt

ROW = 9
COL = 10

class Cell:
    def __init__(self):
        self.parent_i = 0
        self.parent_j = 0
        self.f = 0
        self.g = 0
        self.h = 0

def is_valid(row, col):
    return 0 <= row < ROW and 0 <= col < COL

def is_unblocked(grid, row, col):
    return grid[row][col] == 1

def is_destination(row, col, dest):
    return row == dest[0] and col == dest[1]

def calculate_h_value(row, col, dest):
    return sqrt((row - dest[0])**2 + (col - dest[1])**2)

def trace_path(cell_details, dest):
    print("The Path is:")
    row, col = dest
    path = []

    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
        path.append((row, col))
        row, col = cell_details[row][col].parent_i, cell_details[row][col].parent_j

    path.append((row, col))

    for p in reversed(path):
        if p[0] == 2 or p[0] == 1:
            print(f"-> ({p[0]}, {p[1] - 1})")
        else:
            print(f"-> ({p[0]}, {p[1]})")

def a_star_search(grid, src, dest):
    if not is_valid(src[0], src[1]):
        print("Source is invalid")
        return

    if not is_valid(dest[0], dest[1]):
        print("Destination is invalid")
        return

    if not is_unblocked(grid, src[0], src[1]) or not is_unblocked(grid, dest[0], dest[1]):
        print("Source or the destination is blocked")
        return

    if is_destination(src[0], src[1], dest):
        print("We are already at the destination")
        return

    cell_details = [[Cell() for _ in range(COL)] for _ in range(ROW)]

    i, j = src
    cell_details[i][j].f = 0
    cell_details[i][j].g = 0
    cell_details[i][j].h = 0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j

    open_list = []

    heapq.heappush(open_list, (0.0, (i, j)))

    found_dest = False

    while open_list:
        current = heapq.heappop(open_list)
        i, j = current[1]

        cell_details[i][j].f = current[0]

        for k in range(-1, 2):
            for l in range(-1, 2):
                if is_valid(i + k, j + l):
                    if is_destination(i + k, j + l, dest):
                        cell_details[i + k][j + l].parent_i = i
                        cell_details[i + k][j + l].parent_j = j
                        trace_path(cell_details, dest)
                        found_dest = True
                        return

                    elif not cell_details[i + k][j + l].f and is_unblocked(grid, i + k, j + l):
                        g_new = cell_details[i][j].g + 1
                        h_new = calculate_h_value(i + k, j + l, dest)
                        f_new = g_new + h_new

                        if cell_details[i + k][j + l].f > f_new or cell_details[i + k][j + l].f == 0:
                            heapq.heappush(open_list, (f_new, (i + k, j + l)))
                            cell_details[i + k][j + l].f = f_new
                            cell_details[i + k][j + l].g = g_new
                            cell_details[i + k][j + l].h = h_new
                            cell_details[i + k][j + l].parent_i = i
                            cell_details[i + k][j + l].parent_j = j

    if not found_dest:
        print("Destination not found")

    
grid = [[ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
        [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
        [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
        [ 1, 0, 0, 0, 0, 0, 0, 1, 1, 1 ],
        [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
        [ 0, 0, 1, 0, 0, 0, 0, 0, 1, 1 ],
        [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
        [ 1, 0, 1, 1, 1, 1, 1, 1, 1, 1 ],            
        [ 1, 0, 1, 1, 1, 1, 1, 1, 1, 1 ]]
 
src = [8, 0]
 
dest = [0, 6]
a_star_search(grid, src, dest)