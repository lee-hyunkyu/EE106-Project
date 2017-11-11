class Node:
    def __init__(self, name, index):
        self._name  = name 
        self._index = index # Based only on when added to Graph

class Edge:
    def __init__(self, length, node1, node2):
        self._length = length 
        self._node1  = node1 
        self._node2  = node2

class Graph: 
    def __init__(self, V=[], E={}, nextIndex=0):
        self._nextIndex = nextIndex
        self._V = V # Dictionary of {Name:Node}

        '''
        if (u, v) is an edge
            _E[u.index][v.index] = E
        else
            _E[u.index][v.index] = None
        '''
        self._E = E # 2D Dictionary. 

    def add_node(self, node):
        pass

    def add_edge(self, node1, node2):
        pass

    def get_neighbors(self, node):
        pass

    def get_edge(self, node1, node2):
        pass

    def breadth_first_search(self):
        pass

    def dijkstras(self):
        pass

    def find_min_path(self, node1, node2):
        pass
