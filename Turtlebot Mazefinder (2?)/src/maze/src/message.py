from Graph import *

class node_message:
    def __init__(self, index, directions, neighbor_indices):
        self.index = index
        self.directions = directions
        self.neighbor_indices = neighbor_indices

    def __eq__(self, other):
        return self.index == other.index and self.directions == other.directions and self.neighbor_indices == other.neighbor_indices  

class graph_message:
    def __init__(self, num_nodes, node_msgs):
        self.num_nodes = num_nodes
        self.node_msgs = node_msgs

    def __eq__(self, other):
        is_equal = self.num_nodes == other.num_nodes
        is_equal = is_equal and len(self.node_msgs) == len(other.node_msgs)
        for n1, n2 in zip(self.node_msgs, other.node_msgs):
            is_equal = is_equal and n1 == n2
        return is_equal

def convert_node_to_node_msg(node):
    node_msg = node_message(0, [], [])
    node_msg.index = node.index
    for dir, neighbor_node in node.neighbors.items():
        node_msg.directions += [dir.dir]
        node_msg.neighbor_indices += [neighbor_node.index]
    return node_msg


def convert_graph_to_graph_msg(graph):
    graph_msg = graph_message(0, [])
    graph_msg.num_nodes = len(graph.V)
    for node in graph.get_nodes():
        graph_msg.node_msgs += [convert_node_to_node_msg(node)]
    return graph_msg

def convert_graph_msg_to_graph(graph_msg):
    g = Graph()
    for i in range(graph_msg.num_nodes):
        g.add_node()

    for node_msg in graph_msg.node_msgs:
        index = node_msg.index
        node  = g.get_node(index)

        # Add the neighbors to node
        for dir, neighbor_indices in zip(node_msg.directions, node_msg.neighbor_indices):
            direction = Direction(dir)
            neighbor_node = g.get_node(neighbor_indices)
            node.add_neighbor(neighbor_node, direction)

    return g