import random
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
import time


class MazeGenerator:
    def __init__(self, width, height, path_density=0.15):
        self.width = width
        self.height = height
        self.path_density = path_density
        self.maze = np.ones((height, width), dtype=int)
        self.start = (1, 1)
        self.end = (height - 2, width - 2)

    def generate(self):
        for i in range(self.height):
            for j in range(self.width):
                self.maze[i, j] = 1

        self._carve_passages(1, 1)
        self.maze[self.start] = 0
        self.maze[self.end] = 0
        self._add_additional_paths()

        return self.maze

    def _carve_passages(self, x, y):
        self.maze[y, x] = 0

        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy

            if (0 < new_x < self.width - 1 and 0 < new_y < self.height - 1 and
                    self.maze[new_y, new_x] == 1):
                self.maze[y + dy // 2, x + dx // 2] = 0
                self._carve_passages(new_x, new_y)

    def _add_additional_paths(self):
        internal_walls = [(y, x) for y in range(1, self.height - 1) for x in range(1, self.width - 1)
                          if self.maze[y, x] == 1]
        walls_to_remove = int(len(internal_walls) * self.path_density)

        random.shuffle(internal_walls)
        for y, x in internal_walls[:walls_to_remove]:
            if 0 < y < self.height - 1 and 0 < x < self.width - 1:
                if (self.maze[y - 1, x] == 0 or self.maze[y + 1, x] == 0 or
                        self.maze[y, x - 1] == 0 or self.maze[y, x + 1] == 0):
                    self.maze[y, x] = 0

    def display(self):
        plt.figure(figsize=(10, 10))
        plt.imshow(self.maze, cmap='binary')
        plt.plot(self.start[1], self.start[0], 'go', markersize=10)
        plt.plot(self.end[1], self.end[0], 'ro', markersize=10)
        plt.title("Random Maze with Multiple Paths")
        plt.axis('off')
        plt.show()


class MazeSolver:
    def __init__(self, maze, start, end):
        self.maze = maze
        self.height, self.width = maze.shape
        self.start = start
        self.end = end

    def solve_bfs(self):
        queue = deque([(self.start, [])])
        visited = {self.start}
        nodes_explored = 0

        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        while queue:
            (y, x), path = queue.popleft()
            nodes_explored += 1

            if (y, x) == self.end:
                return path + [(y, x)], nodes_explored

            for dy, dx in moves:
                new_y, new_x = y + dy, x + dx

                if self.height > new_y >= 0 == self.maze[new_y, new_x] and 0 <= new_x < self.width and (
                        new_y, new_x) not in visited:
                    queue.append(((new_y, new_x), path + [(y, x)]))
                    visited.add((new_y, new_x))

        return None, nodes_explored

    def solve_dfs(self):
        stack = [(self.start, [])]
        visited = {self.start}
        nodes_explored = 0

        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        while stack:
            (y, x), path = stack.pop()
            nodes_explored += 1

            if (y, x) == self.end:
                return path + [(y, x)], nodes_explored

            for dy, dx in moves:
                new_y, new_x = y + dy, x + dx

                if self.height > new_y >= 0 == self.maze[new_y, new_x] and 0 <= new_x < self.width and (
                        new_y, new_x) not in visited:
                    stack.append(((new_y, new_x), path + [(y, x)]))
                    visited.add((new_y, new_x))

        return None, nodes_explored

    def solve_astar(self):
        start_node = (self.start, [], 0, self.manhattan_distance(self.start))
        open_set = [start_node]
        closed_set = set()
        nodes_explored = 0

        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        while open_set:
            open_set.sort(key=lambda xz: xz[3])
            (y, x), path, g_score, f_score = open_set.pop(0)
            nodes_explored += 1

            if (y, x) == self.end:
                return path + [(y, x)], nodes_explored

            closed_set.add((y, x))

            for dy, dx in moves:
                new_y, new_x = y + dy, x + dx
                new_pos = (new_y, new_x)

                if (
                        self.height > new_y >= 0 == self.maze[
                    new_y, new_x] and 0 <= new_x < self.width and new_pos not in closed_set):

                    new_g_score = g_score + 1
                    new_f_score = new_g_score + self.manhattan_distance(new_pos)

                    if any(pos == new_pos and fs > new_f_score for pos, _, _, fs in open_set):
                        continue

                    open_set.append((new_pos, path + [(y, x)], new_g_score, new_f_score))

        return None, nodes_explored

    def manhattan_distance(self, pos):
        y, x = pos
        end_y, end_x = self.end
        return abs(y - end_y) + abs(x - end_x)

    def display_solution(self, path, algorithm_name):
        if path is None:
            print("No solution found")
            return

        solution_maze = np.copy(self.maze)

        for y, x in path:
            solution_maze[y, x] = 2

        plt.figure(figsize=(10, 10))

        cmap = plt.cm.colors.ListedColormap(['white', 'black', 'red'])

        plt.imshow(solution_maze, cmap=cmap)
        plt.plot(self.start[1], self.start[0], 'go', markersize=10)
        plt.plot(self.end[1], self.end[0], 'bo', markersize=10)
        plt.title(f"Maze Solution - {algorithm_name}")
        plt.axis('off')
        plt.show()


def main():
    # random.seed(42)

    maze_width, maze_height = 41, 41
    maze_gen = MazeGenerator(maze_width, maze_height, path_density=0.15)
    maze = maze_gen.generate()

    maze_gen.display()

    start = maze_gen.start
    end = maze_gen.end
    solver = MazeSolver(maze, start, end)

    start_time = time.time()
    bfs_path, bfs_nodes = solver.solve_bfs()
    bfs_time = time.time() - start_time
    print(f"BFS: Found solution in {bfs_time:.4f} seconds, explored {bfs_nodes} nodes, path length: {len(bfs_path)}")
    solver.display_solution(bfs_path, "BFS")

    start_time = time.time()
    dfs_path, dfs_nodes = solver.solve_dfs()
    dfs_time = time.time() - start_time
    print(f"DFS: Found solution in {dfs_time:.4f} seconds, explored {dfs_nodes} nodes, path length: {len(dfs_path)}")
    solver.display_solution(dfs_path, "DFS")

    start_time = time.time()
    astar_path, astar_nodes = solver.solve_astar()
    astar_time = time.time() - start_time
    print(
        f"A*: Found solution in {astar_time:.4f} seconds, explored {astar_nodes} nodes, path length: {len(astar_path)}")
    solver.display_solution(astar_path, "A*")


if __name__ == "__main__":
    main()

"""
კოდის ახსნა:
ეს პროგრამა ქმნის შემთხვევით ლაბირინთს და შემდეგ იყენებს სამ განსხვავებულ ალგორითმს მის გადასაჭრელად. პროგრამა შედგება ორი მთავარი კლასისგან:
MazeGenerator და MazeSolver.

MazeGenerator კლასი ქმნის ლაბირინთს შემდეგი პროცესით:

თავდაპირველად, იქმნება ბადე, რომელიც მთლიანად კედლებისგან შედგება (წარმოდგენილია 1-ებით)
შემდეგ, რეკურსიული DFS (Depth-First Search) ალგორითმი იწყებს გზების ფორმირებას (წარმოდგენილია 0-ებით)
ბოლოს, ემატება დამატებითი გზები (_add_additional_paths მეთოდით), რაც იძლევა მრავალი გადაწყვეტის გზის შესაძლებლობას


MazeSolver კლასი იყენებს სამ განსხვავებულ ალგორითმს ლაბირინთის გადასაჭრელად:

BFS (Breadth-First Search) - იყენებს რიგს და პოულობს უმოკლეს გზას
DFS (Depth-First Search) - იყენებს სტეკს და პოულობს პირველივე შესაძლებელ გზას
A ძიება* - იყენებს პრიორიტეტულ რიგს და ევრისტიკას (მანჰეტენის მანძილს) ოპტიმალური გზის საპოვნელად



თითოეული ალგორითმი ახორციელებს ლაბირინთის გავლას განსხვავებული სტრატეგიით:

BFS იკვლევს ყველა უჯრას ერთ სიღრმეზე, სანამ გადავა შემდეგზე, რაც უზრუნველყოფს უმოკლესი გზის პოვნას
DFS იკვლევს ერთ გზას რაც შეიძლება ღრმად, შემდეგ უბრუნდება უკან; ეს ხშირად უფრო სწრაფია, მაგრამ ვერ უზრუნველყოფს უმოკლესი გზის პოვნას
A* აბალანსებს სიღრმესა და სიგანეს ევრისტიკის გამოყენებით, რაც ხშირად გვაძლევს ეფექტურ და ოპტიმალურ შედეგს

ლაბირინთის გენერირების შემდეგ, პროგრამა ვიზუალურად აჩვენებს ლაბირინთს. შემდეგ, ის იყენებს სამივე ალგორითმს გადაწყვეტის გზის საპოვნელად,
ზომავს შესრულების დროს და აჩვენებს შედეგებს. ყოველი გადაწყვეტის გზა ნაჩვენებია წითელი ფერით, ხოლო საწყისი და საბოლოო წერტილები მწვანე
და ლურჯი წერტილებით. ამ გზით შეგვიძლია შევადაროთ სხვადასხვა ალგორითმის ეფექტურობა და ნაპოვნი გზების განსხვავება.
"""
