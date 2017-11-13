class Node:
    def __init__(self, name, index, root=None):
        self._name  = name 
        self._index = index # Based only on when added to Graph
        if root:
            self._root  = root 
        else:
            self._root  = self

    @property
    def name(self):
        return self._name
    @property
    def index(self):
        return self._index

    @property
    def root(self):
        if self._root is not self:
            return self._root.root()
        return self

class Edge:
    def __init__(self, length, node1, node2):
        self._length = length 
        self._node1  = node1 
        self._node2  = node2

    @property
    def length(self):
        return self._lengths
    @property
    def node1(self):
        return self._node1s
    @property
    def node2(self):
        return self._node2s

class Graph: 
    def __init__(self, V={}, E={}, v_names={}, nextIndex=0):
        self._nextIndex = nextIndex
        self._V        = V          # Dictionary of {Index:Node} 
        self._V_names  = v_names    # Dictionary of {Name :Node}

        '''
        if (u, v) is an edge
            _E[u.index][v.index] = E
        else
            _E[u.index][v.index] = E with length 0 or None
        '''
        self._E = E # 2D Dictionary. 

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

    def add_node(self, name):
        node                     = Node(name, self.nextIndex) 
        self._V[node.index]      = node
        self._V_names[node.name] = node
        self._nextIndex          += 1
        return node

    def add_edge(self, node1, node2, length):
        self._E[node1.index][node2.index] = Edge(length, node1, node2)
        self._E[node2.index][node1.index] = Edge(length, node2, node1)

    def remove_edge(self, node1, node2):
        self._E[node1.index][node2.index] = Edge(0, node1, node2)
        self._E[node2.index][node1.index] = Edge(0, node2, node1)

    def get_neighbors(self, node):
        neighbors = []
        for edge in self.E[node.index]:
            if edge.length > 0:
                neighbors += edge.node2
        return neighbors

    def get_edge(self, node1, node2):
        return self.E[node1.index][node2.index]

    def get_node(self, name):
        return self._V_names.get(name)

    def breadth_first_search(self):
        pass

    def dijkstras(self):
        pass

    def find_min_path(self, node1, node2):
        pass
