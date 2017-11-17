from Graph import *
from enum import Enum

class Direction(Enum):
    LEFT  = -1
    UP    =  0
    RIGHT =  1

class MazeNode(Node):
    def __init__(self, name, index, parent=None, root=None):
        super().__init__(name, index)
        self._parent    = parent
        self._root      = root if root else self
        self._direction = dir
    
    @property
    def parent(self):
        return self._parent
    
    @property
    def root(self):
        return self._root    
    
    @property
    def direction(self):
        return self._direction


'''
A Maze will build upon the Graph class. 

1) A sense of direction. This will tell the robot how to turn
2) A disjoint datasturcutre for the Nodes 
'''

class Maze(Graph):
    def find(self, node):
        if node.root is not node:
            node.root = find(node.parent)
        return node.root

    def union(self, node1, node2):
        root1 = find(node1)
        root2 = find(node2)

        node2.root = root1
        find(node2) # Update all the values inside node2
        return root1

    def add_node(self, name, parent=None, root=None):
        node        = MazeNode(name, self.nextIndex, parent=parent, root=root)
        super().add_node(node)
        return node

    def add_edge(self, node1, node2, length):
        pass

m = Maze()
print(m.add_node('hello'))
