from Graph import *

class Maze(Graph):
    def __init__(self, n, m):
        self._n = n
        self._m = m

    @staticmethod
    def create_random_maze(n, m):
        maze = Maze(n, m)
        # Define the walls of a maze
        return maze