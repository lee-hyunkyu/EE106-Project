from Graph import *

class msg_node:
    def __init__(self, index, directions, neighbor_indices):
        self.index = index
        self.directions = directions
        self.neighbor_indices = neighbor_indices

# Consider the numpad example
# 1 2 3
# 4 5 6
# 7 8 9 
g = Graph()
n1 = g.add_node()
n2 = g.add_node()
n3 = g.add_node()
n4 = g.add_node()
n5 = g.add_node()
n6 = g.add_node()
n7 = g.add_node()
n8 = g.add_node()
n9 = g.add_node()

# Imagine a configuration similar to a telephone numpad
north = Direction.NORTH()
east  = Direction.EAST()
south = Direction.SOUTH()
west  = Direction.WEST()
n1.add_neighbor(n2, east)
n1.add_neighbor(n4, south)
n2.add_neighbor(n1, west)
n2.add_neighbor(n3, east)
n2.add_neighbor(n5, south)
n3.add_neighbor(n2, west)
n3.add_neighbor(n6, south)
n4.add_neighbor(n1, north)
n4.add_neighbor(n5, east)
n4.add_neighbor(n7, south)
n5.add_neighbor(n4, west)
n5.add_neighbor(n2, north)
n5.add_neighbor(n6, east)
n5.add_neighbor(n8, south)
n6.add_neighbor(n3, north)
n6.add_neighbor(n5, west)
n6.add_neighbor(n9, south)
n7.add_neighbor(n4, north)
n7.add_neighbor(n8, east)
n8.add_neighbor(n7, west)
n8.add_neighbor(n5, north)
n8.add_neighbor(n9, east)
n9.add_neighbor(n8, west)
n9.add_neighbor(n6, north)

def convert_to_msg_nodes(graph):
    msg_nodes = []
    for index, node in graph.get_index_node():
        n = msg_node(index, [], [],)
        for direction, neighbor in node.neighbors.items():
            # import pdb; pdb.set_trace()
            n.directions += [direction.dir]
            n.neighbor_indices += [neighbor.index]
        msg_nodes += [n]
    return msg_nodes

num_nodes = 9

msg_nodes = convert_to_msg_nodes(g)

def convert_msg_node_to_graph(num_nodes, msg_nodes):
    g = Graph()
    for i in range(num_nodes):
        g.add_node()

    for mn in msg_nodes:
        node = g.get_node(mn.index)
        for direction, index in zip(mn.directions, mn.neighbor_indices):
            neighbor_node = g.get_node(index)
            node.add_neighbor(neighbor_node, Direction(direction))
    return g

g_ = convert_msg_node_to_graph(num_nodes, msg_nodes)

for index, node in g_.get_index_node():
    print(index)
    print("G_")
    print(node)
    print("G")
    node = g.get_node(index)
    print(node)
    