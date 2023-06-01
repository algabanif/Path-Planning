# Path-Planning
Path Planning is a fundamental problem in robotics. It aims to find an optimal 
free-obstacle path for a robot from a starting position to a given destination

# Main Goals
The purpose of this project is to design and implement the
A* search algorithm to address the path planning problem
in a grid-based environment. The environment in which
the robot operates is represented by a grid map, where
the initial (S) and goal (G) states are explicitly marked.
Some of the cells on the map contain obstacles that the
robot cannot traverse, preventing a direct path to the
goal. The robot can move one step horizontally, vertically,
or diagonally from one cell to an adjacent, unoccupied
cell. This implies that the maximum number of reachable
neighboring cells in a single move is eight.

# Requirements
Formulate the searching problem
Define a data structure
Write a Python function implementing A* Algorithm
Generate random module to test the program randomly
Generate GUI to represent the output
Draw a figure summarizing the average time, the worst case, the best case
