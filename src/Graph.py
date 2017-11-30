from collections import *
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

    @property
    def dir(self):
        return self._dir

    def opposite_direction(self):
        return Direction(-self._dir)

    @classmethod
    def NORTH(cls):
        return Direction(Direction.NORTH_VAL)
    @classmethod
    def SOUTH(cls):
        return Direction(Direction.SOUTH_VAL)
    @classmethod
    def EAST(cls):
        return Direction(Direction.EAST_VAL)
    @classmethod
    def WEST(cls):
        return Direction(Direction.WEST_VAL)

    # Returns the direction if one turned 90 degrees clockwise
    def clockwise_turn_direction(self):
        if self._dir is 1:
            return Direction.EAST()
        if self._dir is 2:
            return Direction.SOUTH()
        if self._dir is -1:
            return Direction.WEST()
        if self._dir is -2:
            return Direction.NORTH()
        return None

    def __eq__(self, other):
        return self.dir == other.dir

    def __hash__(self):
        return self.dir

class Node:
    def __init__(self, index, name=None):
        self._name  = name   # Not really important
        self._index = index  # Based only on when added to Graph
        self._neighbors   = defaultdict(int) # {Direction: Node}
        self._is_end      = False

    @property
    def name(self):
        return self._name
    @property
    def index(self):
        return self._index
    @property
    def neighbors(self):
        return self._neighbors
    @property
    def is_end(self):
        return self._is_end

    def set_as_end(self):
        self._is_end = True
        return self

    def get_neighbor(self, dir):
        return self._neighbors[dir]

    # Adds V as a neighbor of SELF
    # You go from SELF to V by going in DIRECTION
    # i.e. if V is north of SELF, DIRECTION == NORTH
    def add_neighbor(self, v, direction):
        # If it does not exist in the dict or the neighbor matches
        if not self._neighbors[direction] or self._neighbors[direction] == v:
            self._neighbors[direction] = v
            v._neighbors[direction.opposite_direction()] = self
            return True
        else:
            return False # A neighbor already exists. This shouldn't be possible

    def is_deadend(self):
        return len(neighbors) == 1 # Can only go backwards

    def __eq__(self, other):
        return self.index == other.index and self.neighbors == other.neighbors

    def __str__(self):
        return '{0}: {1}'.format(self.index, str(self.neighbors))

class Graph: 
    def __init__(self, V=None, next_index=0):
        self._next_index = next_index
        if V:
            self._V      = V
        else:
            self._V      = {} # Annoying quirk of python forces this check

    @property
    def nextIndex(self):
        return self._next_index
    @property
    def V(self):
        return self._V
    @property
    def next_index(self):
        return self._next_index

    # Pass in the name of the node or a node to add to the graph
    def add_node(self):
        node = Node(self.next_index)
        self._V[self.next_index] = node
        self._next_index += 1
        return node

    def get_node(self, index):
        return self.V[index]

    def get_neighbors(self, node):
        return node.neighbors

    def breadth_first_search(self):
        pass

    def dijkstras(self):
        pass

    def find_min_path(self, node1, node2):
        pass

if __name__ == '__main__':
    a = Graph()