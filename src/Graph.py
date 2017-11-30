class Direction:
    # Represents a cardinal direction 
    # 1: NORTH
    # -1: SOUTH
    # 2: EAST
    # -2: WEST
    NORTH_VAL   = 1
    SOUTH_VAL   = -1
    EAST_VAL    = 2
    WEST_VAL    = -2

    def __init__(self, dir):
        self._dir = dir

    def __str__(self):
        if self._dir is 1:
            return 'NORTH'
        if self._dir is -1:
            return 'SOUTH'
        if self._dir is 2:
            return 'EAST'
        if self._dir is -2:
            return 'WEST'
        return 'INVALID'

    def opposite_direction(self):
        return Direction(-self._dir)

    @classmethod
    def NORTH():
        return Direction(Direction.NORTH_VAL)
    @classmethod
    def SOUTH():
        return Direction(Direction.SOUTH_VAL)
    @classmethod
    def EAST():
        return Direction(Direction.EAST_VAL)
    @classmethod
    def WEST():
        return Direction(Direction.WEST_VAL)


class Node:
    def __init__(self, name, index):
        self._name  = name 
        self._index = index # Based only on when added to Graph

    @property
    def name(self):
        return self._name
    @property
    def index(self):
        return self._index

    def __eq__(self, other):
        return self.name == other.name and self.index == other.index

    def __lt__(self, other):
        return self.index < other.index

    def __gt__(self, other):
        return self.index > other.index

class Edge:
    def __init__(self, length, node1, node2):
        self._length = length 
        self._node1  = node1 
        self._node2  = node2

    @property
    def length(self):
        return self._length
    @property
    def node1(self):
        return self._node1
    @property
    def node2(self):
        return self._node2

    def __eq__(self, other):
        return other.length == self.length and other.node1 == self.node1 and other.node2 == self.node2

class Graph: 
    def __init__(self, V=None, E=None, v_names=None, nextIndex=0):
        self._nextIndex = nextIndex
        if V is None:
            self._V         = {}
        else:
            self._V         = V          # Dictionary of {Index:Node} 
        if v_names is None:
            self._V_names   = {}
        else:
            self._V_names   = v_names    # Dictionary of {Name :Node}
        if E is None:
            self._E         = []         
        else:
            self._E         = E          # List of Edge(u, v), u.index < v.index (always)

    @property
    def nextIndex(self):
        return self._nextIndex
    @property
    def V(self):
        return self._V
    @property
    def E(self):
        return self._E

    @property
    def V_names(self):
        return self._V_names

    # Pass in the name of the node or a node to add to the graph
    def add_node(self, arg=None):
        if isinstance(arg, Node):
            node = arg
        else:
            name = arg
            node                     = Node(name, self.nextIndex) 
        self._V[node.index]      = node
        self._V_names[node.name] = node
        self._nextIndex          += 1
        return node

    def add_edge(self, node1, node2, length):
        if node1.index < node2.index:
            self._E += [Edge(length, node1, node2)]
        else:
            self._E += [Edge(length, node2, node1)]
        return self._E[-1] # The last added edge

    def remove_edge(self, node1, node2):
        edge = self.get_edge(node1, node2)
        self._E.remove(edge)

    def get_neighbors(self, node):
        neighbors = []
        for edge in self.E:
            if node == edge.node1:
                neighbors += [edge.node2]
            elif node == edge.node2:
                neighbors += [edge.node1]
        return neighbors

    def get_edge(self, node1, node2):
        smaller_node = min(node1, node2)
        larger_node  = max(node1, node2)
        for edge, i in zip(self._E, range(len(self._E))) :
            if edge.node1 is smaller_node and edge.node2 is larger_node:
                return edge

    def get_node(self, name):
        return self._V_names.get(name)

    def breadth_first_search(self):
        pass

    def dijkstras(self):
        pass

    def find_min_path(self, node1, node2):
        pass

if __name__ == '__main__':
    a = Graph()