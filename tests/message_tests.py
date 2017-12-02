import unittest
from collections import *
from Graph import *
from message import *
 
class ConstraintTest(unittest.TestCase):
    
    def setUp(self):
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
        self.g = g

    def test_convert_node_to_node_msg(self):
        north = Direction.NORTH()
        east = Direction.EAST()
        south = Direction.SOUTH()
        west = Direction.WEST()

        n1 = self.g.get_node(0)
        n2 = self.g.get_node(1)
        n3 = self.g.get_node(2)

        node_msg_1 = convert_node_to_node_msg(n1)
        node_msg_2 = convert_node_to_node_msg(n2)
        node_msg_3 = convert_node_to_node_msg(n3)

        self.assertTrue(n1.index == node_msg_1.index)
        self.assertTrue(n2.index == node_msg_2.index)
        self.assertTrue(n3.index == node_msg_3.index)

        self.assertTrue(len(node_msg_1.directions) == 2)
        self.assertTrue(north.dir not in node_msg_1.directions)
        self.assertTrue(west.dir not in node_msg_1.directions)
        self.assertTrue(south.dir in node_msg_1.directions)
        self.assertTrue(east.dir in node_msg_1.directions)

        self.assertTrue(len(node_msg_2.directions) == 3)
        self.assertTrue(north.dir not in node_msg_2.directions)
        self.assertTrue(west.dir  in node_msg_2.directions)
        self.assertTrue(south.dir in node_msg_2.directions)
        self.assertTrue(east.dir in node_msg_2.directions)

        self.assertTrue(len(node_msg_3.directions) == 2)
        self.assertTrue(north.dir not in node_msg_3.directions)
        self.assertTrue(west.dir in node_msg_3.directions)
        self.assertTrue(south.dir in node_msg_3.directions)
        self.assertTrue(east.dir not in node_msg_3.directions)

    def test_convert_graph_to_graph_msg(self):
        graph_msg = convert_graph_to_graph_msg(self.g)

        for node_msg in graph_msg.node_msgs:
            index = node_msg.index
            node  = self.g.get_node(index)
            node_msg_from_graph = convert_node_to_node_msg(node)
            self.assertTrue(node_msg == node_msg_from_graph)

    def test_convert_graph_msg_to_graph(self):
        graph_msg = convert_graph_to_graph_msg(self.g)
        new_g = convert_graph_msg_to_graph(graph_msg)
        new_g_msg = convert_graph_to_graph_msg(new_g)

        self.assertTrue(graph_msg == new_g_msg)


if __name__ == '__main__':
    unittest.main()