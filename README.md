Maze Generator and Solver
This Python program generates a random maze and solves it using three different algorithms: Breadth-First Search (BFS), Depth-First Search (DFS), and A* Search. It consists of two main classes: MazeGenerator and MazeSolver.
Program Overview
The program creates a random maze with walls and paths, then applies three maze-solving algorithms to find paths from a start point to an end point. The solutions are visualized, with performance metrics (execution time) and path differences displayed for comparison.
MazeGenerator Class

Purpose: Generates a random maze with multiple possible solution paths.
Process:
Initializes a grid filled with walls (represented by 1s).
Uses a recursive Depth-First Search (DFS) algorithm to carve out paths (represented by 0s).
Adds extra paths via the _add_additional_paths method to create multiple possible solutions.


Output: A maze with a start point, end point, and navigable paths.

MazeSolver Class

Purpose: Solves the generated maze using three algorithms.
Algorithms:
Breadth-First Search (BFS):
Uses a queue to explore all cells at the current depth before moving deeper.
Guarantees the shortest path to the end point.


Depth-First Search (DFS):
Uses a stack to explore one path as deeply as possible before backtracking.
Faster in some cases but does not guarantee the shortest path.


A Search*:
Uses a priority queue with a Manhattan distance heuristic to balance exploration and efficiency.
Finds an optimal path efficiently in most cases.





Visualization

Displays the maze with:
Walls (black or solid blocks).
Paths (white or open spaces).
Start point (green dot).
End point (blue dot).
Solution paths (red lines, one for each algorithm).


Shows execution time for each algorithm.
Highlights differences in paths and efficiency between BFS, DFS, and A*.

Features

Random Maze Generation: Creates varied mazes with multiple solution paths.
Multiple Algorithms: Compares BFS, DFS, and A* for pathfinding.
Visual Output: Clearly displays the maze and solution paths.
Performance Metrics: Measures and reports execution time for each algorithm.

Requirements

Python 3.x
Standard libraries: queue, heapq, random, time
Visualization library (e.g., matplotlib, tkinter, or similar, depending on implementation)

Usage

Run the Python script.
A random maze is generated and displayed.
The MazeSolver applies BFS, DFS, and A* to find solution paths.
Results are visualized:
Solution paths are shown in red.
Start and end points are marked in green and blue.
Execution times are printed for each algorithm.



Pros

Generates complex mazes with multiple solutions.
Allows comparison of different pathfinding algorithms.
Clear visualization aids in understanding algorithm behavior.
A* provides efficient and optimal solutions.

Cons

DFS may produce longer paths than necessary.
Large mazes increase computation time, especially for BFS and A*.
Visualization may require additional dependencies (e.g., matplotlib).

Complexity

Time:
BFS: O(V + E), where V is the number of cells and E is the number of edges.
DFS: O(V + E), but may explore more nodes than necessary.
A*: O(V log V) with a priority queue, depending on the heuristic.


Space:
BFS: O(V) for the queue.
DFS: O(V) for the stack (via recursion or explicit stack).
A*: O(V) for the priority queue and visited set.



Example Output

A generated maze is shown with walls, paths, start, and end points.
Three solution paths (BFS, DFS, A*) are overlaid in red.
Execution times (e.g., BFS: 0.05s, DFS: 0.03s, A*: 0.04s) are displayed.
Visual comparison highlights path length and algorithm efficiency.

