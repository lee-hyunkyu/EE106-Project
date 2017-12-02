from Graph import *
import unittest
import string
 
class TestGraph(unittest.TestCase):

    def setUp(self):
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
        n2.add_neighbor(n3, east)
        n2.add_neighbor(n5, south)
        n3.add_neighbor(n6, south)

        n4.add_neighbor(n5, east)
        n4.add_neighbor(n7, south)
        n5.add_neighbor(n6, east)
        n5.add_neighbor(n8, south)
        n6.add_neighbor(n9, south)

        n7.add_neighbor(n8, east)
        n8.add_neighbor(n5, north)
        n8.add_neighbor(n9, east)
        self.g = g

    def test_direction(self):
        south = Direction.SOUTH()
        east  = Direction.EAST()
        west  = Direction.WEST()
        north = Direction.NORTH()

        self.assertTrue(south.dir == Direction.SOUTH_VAL)
        self.assertTrue(east.dir == Direction.EAST_VAL)
        self.assertTrue(west.dir == Direction.WEST_VAL)
        self.assertTrue(north.dir == Direction.NORTH_VAL)

        self.assertTrue(south == north.opposite_direction())
        self.assertTrue(north == south.opposite_direction())
        self.assertTrue(east  == west.opposite_direction())
        self.assertTrue(west  == east.opposite_direction())

        self.assertFalse(south == west.opposite_direction())
        self.assertFalse(south == east.opposite_direction())
        self.assertFalse(north == west.opposite_direction())
        self.assertFalse(north == east.opposite_direction())

        self.assertFalse(south.opposite_direction() == west)
        self.assertFalse(south.opposite_direction() == east)
        self.assertFalse(north.opposite_direction() == west)
        self.assertFalse(north.opposite_direction() == east)

    def test_node_initialization(self):
        a = Node(0)
        b = Node(1)
        c = Node(2)

        self.assertTrue(a.index == 0)
        self.assertTrue(b.index == 1)
        self.assertTrue(c.index == 2)

        self.assertTrue(a.neighbors == {})
        self.assertTrue(b.neighbors == {})
        self.assertTrue(c.neighbors == {})

        self.assertFalse(a.is_end)
        self.assertFalse(b.is_end)
        self.assertFalse(c.is_end)

    def test_graph_initialization(self):
        graph = Graph()
        self.assertTrue(len(graph.V)     == 0)
        self.assertTrue(graph.next_index == 0)

    def test_add_node(self):
        g = Graph()
        n1 = g.add_node()
        n2 = g.add_node()
        n3 = g.add_node()
        n4 = g.add_node()

        self.assertTrue(len(g.V) == 4)

        for i in range(4):
            self.assertTrue(i in g.V)

        nodes = [n1, n2, n3, n4]

        for i, n in zip(range(4), nodes):
            self.assertTrue(g.V[i] is n)
            self.assertTrue(g.V[i] == n)

        self.assertTrue(g.next_index == 4)

    def test_get_node(self):
        g = Graph()
        n1 = g.add_node()
        n2 = g.add_node()
        n3 = g.add_node()
        n4 = g.add_node()

        nodes = [n1, n2, n3, n4]
        for i, n in zip(range(4), nodes):
            self.assertTrue(g.get_node(i) == n)
            self.assertTrue(g.get_node(i) is n)

    def test_add_neighbor(self):
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


        self.assertTrue(n1.add_neighbor(n2, east))
        self.assertTrue(n1.add_neighbor(n4, south))
        self.assertTrue(n2.add_neighbor(n1, west))
        self.assertTrue(n2.add_neighbor(n3, east))
        self.assertTrue(n2.add_neighbor(n5, south))
        self.assertTrue(n3.add_neighbor(n2, west))
        self.assertTrue(n3.add_neighbor(n6, south))

        self.assertTrue(n4.add_neighbor(n1, north))
        self.assertTrue(n4.add_neighbor(n5, east))
        self.assertTrue(n4.add_neighbor(n7, south))
        self.assertTrue(n5.add_neighbor(n4, west))
        self.assertTrue(n5.add_neighbor(n2, north))
        self.assertTrue(n5.add_neighbor(n6, east))
        self.assertTrue(n5.add_neighbor(n8, south))
        self.assertTrue(n6.add_neighbor(n3, north))
        self.assertTrue(n6.add_neighbor(n5, west))
        self.assertTrue(n6.add_neighbor(n9, south))


        self.assertTrue(n7.add_neighbor(n4, north))
        self.assertTrue(n7.add_neighbor(n8, east))
        self.assertTrue(n8.add_neighbor(n7, west))
        self.assertTrue(n8.add_neighbor(n5, north))
        self.assertTrue(n8.add_neighbor(n9, east))
        self.assertTrue(n9.add_neighbor(n8, west))
        self.assertTrue(n9.add_neighbor(n6, north))

        self.assertTrue(len(n1.neighbors) == 2)
        self.assertTrue(len(n2.neighbors) == 3)
        self.assertTrue(len(n3.neighbors) == 2)
        self.assertTrue(len(n4.neighbors) == 3)
        self.assertTrue(len(n5.neighbors) == 4)
        self.assertTrue(len(n6.neighbors) == 3)
        self.assertTrue(len(n7.neighbors) == 2)
        self.assertTrue(len(n8.neighbors) == 3)
        self.assertTrue(len(n9.neighbors) == 2)

        ####
        self.assertTrue(n1.get_neighbor(east)    is n2)
        self.assertTrue(n1.get_neighbor(south)   is n4)
        self.assertTrue(n2.get_neighbor(west)    is n1)
        self.assertTrue(n2.get_neighbor(south)   is n5)
        self.assertTrue(n2.get_neighbor(east)    is n3)
        self.assertTrue(n3.get_neighbor(west)    is n2)
        self.assertTrue(n3.get_neighbor(south)   is n6)
        self.assertTrue(n1.get_neighbor(north)   is 0)
        self.assertTrue(n1.get_neighbor(west)    is 0)
        self.assertTrue(n2.get_neighbor(north)   is 0)
        self.assertTrue(n3.get_neighbor(north)   is 0)
        self.assertTrue(n3.get_neighbor(east)    is 0)

        self.assertTrue(n4.get_neighbor(north)    is n1)
        self.assertTrue(n4.get_neighbor(east)     is n5)
        self.assertTrue(n4.get_neighbor(south)    is n7)
        self.assertTrue(n5.get_neighbor(north)    is n2)
        self.assertTrue(n5.get_neighbor(east)     is n6)
        self.assertTrue(n5.get_neighbor(south)    is n8)
        self.assertTrue(n5.get_neighbor(west)     is n4)
        self.assertTrue(n6.get_neighbor(north)    is n3)
        self.assertTrue(n6.get_neighbor(west)     is n5)
        self.assertTrue(n6.get_neighbor(south)    is n9)
        self.assertTrue(n4.get_neighbor(west)     is 0)
        self.assertTrue(n6.get_neighbor(east)     is 0)

        self.assertTrue(n7.get_neighbor(east)    is n8)
        self.assertTrue(n7.get_neighbor(north)   is n4)
        self.assertTrue(n8.get_neighbor(west)    is n7)
        self.assertTrue(n8.get_neighbor(north)   is n5)
        self.assertTrue(n8.get_neighbor(east)    is n9)
        self.assertTrue(n9.get_neighbor(west)    is n8)
        self.assertTrue(n9.get_neighbor(north)   is n6)
        self.assertTrue(n7.get_neighbor(south)   is 0)
        self.assertTrue(n7.get_neighbor(west)    is 0)
        self.assertTrue(n8.get_neighbor(south)   is 0)
        self.assertTrue(n9.get_neighbor(south)   is 0)
        self.assertTrue(n9.get_neighbor(east)    is 0)

    def test_add_neighbor(self):
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

        self.assertTrue(n1.add_neighbor(n2, east))
        self.assertTrue(n1.add_neighbor(n4, south))
        self.assertTrue(n2.add_neighbor(n3, east))
        self.assertTrue(n2.add_neighbor(n5, south))
        self.assertTrue(n3.add_neighbor(n6, south))

        self.assertTrue(n4.add_neighbor(n5, east))
        self.assertTrue(n4.add_neighbor(n7, south))
        self.assertTrue(n5.add_neighbor(n6, east))
        self.assertTrue(n5.add_neighbor(n8, south))
        self.assertTrue(n6.add_neighbor(n9, south))

        self.assertTrue(n7.add_neighbor(n8, east))
        self.assertTrue(n8.add_neighbor(n5, north))
        self.assertTrue(n8.add_neighbor(n9, east))

        self.assertTrue(len(n1.neighbors) == 2)
        self.assertTrue(len(n2.neighbors) == 3)
        self.assertTrue(len(n3.neighbors) == 2)
        self.assertTrue(len(n4.neighbors) == 3)
        self.assertTrue(len(n5.neighbors) == 4)
        self.assertTrue(len(n6.neighbors) == 3)
        self.assertTrue(len(n7.neighbors) == 2)
        self.assertTrue(len(n8.neighbors) == 3)
        self.assertTrue(len(n9.neighbors) == 2)

        ####
        self.assertTrue(n1.get_neighbor(east)    is n2)
        self.assertTrue(n1.get_neighbor(south)   is n4)
        self.assertTrue(n2.get_neighbor(west)    is n1)
        self.assertTrue(n2.get_neighbor(south)   is n5)
        self.assertTrue(n2.get_neighbor(east)    is n3)
        self.assertTrue(n3.get_neighbor(west)    is n2)
        self.assertTrue(n3.get_neighbor(south)   is n6)
        self.assertTrue(n1.get_neighbor(north)   is 0)
        self.assertTrue(n1.get_neighbor(west)    is 0)
        self.assertTrue(n2.get_neighbor(north)   is 0)
        self.assertTrue(n3.get_neighbor(north)   is 0)
        self.assertTrue(n3.get_neighbor(east)    is 0)

        self.assertTrue(n4.get_neighbor(north)    is n1)
        self.assertTrue(n4.get_neighbor(east)     is n5)
        self.assertTrue(n4.get_neighbor(south)    is n7)
        self.assertTrue(n5.get_neighbor(north)    is n2)
        self.assertTrue(n5.get_neighbor(east)     is n6)
        self.assertTrue(n5.get_neighbor(south)    is n8)
        self.assertTrue(n5.get_neighbor(west)     is n4)
        self.assertTrue(n6.get_neighbor(north)    is n3)
        self.assertTrue(n6.get_neighbor(west)     is n5)
        self.assertTrue(n6.get_neighbor(south)    is n9)
        self.assertTrue(n4.get_neighbor(west)     is 0)
        self.assertTrue(n6.get_neighbor(east)     is 0)

        self.assertTrue(n7.get_neighbor(east)    is n8)
        self.assertTrue(n7.get_neighbor(north)   is n4)
        self.assertTrue(n8.get_neighbor(west)    is n7)
        self.assertTrue(n8.get_neighbor(north)   is n5)
        self.assertTrue(n8.get_neighbor(east)    is n9)
        self.assertTrue(n9.get_neighbor(west)    is n8)
        self.assertTrue(n9.get_neighbor(north)   is n6)
        self.assertTrue(n7.get_neighbor(south)   is 0)
        self.assertTrue(n7.get_neighbor(west)    is 0)
        self.assertTrue(n8.get_neighbor(south)   is 0)
        self.assertTrue(n9.get_neighbor(south)   is 0)
        self.assertTrue(n9.get_neighbor(east)    is 0)

    # def test_breadth_first_search(self):
    #     pass

    def test_dijkstras(self):
        # Initialize graph
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

        # Run Dijkstra's
        nodes = [n1, n2, n3, n4, n5, n6, n7, n8, n9]
        distances, prevs = g.dijkstras(n1)
        self.assertTrue(distances[n1] == 0)
        self.assertTrue(distances[n2] == 1)
        self.assertTrue(distances[n3] == 2)
        self.assertTrue(distances[n4] == 1)
        self.assertTrue(distances[n5] == 2)
        self.assertTrue(distances[n6] == 3)
        self.assertTrue(distances[n7] == 2)
        self.assertTrue(distances[n8] == 3)
        self.assertTrue(distances[n9] == 4)

    # def test_find_min_path(self):
    #     pass

    def test_get_node_via_turns(self):
        north = Direction.NORTH()
        east  = Direction.EAST()
        south = Direction.SOUTH()
        west  = Direction.WEST()
        
        end_node = self.g.get_node_via_turns([east, south])
        self.assertTrue(self.g.get_node(4) == end_node)

        end_node = self.g.get_node_via_turns([east, south, south])
        self.assertTrue(self.g.get_node(7) == end_node)

        end_node = self.g.get_node_via_turns([east, south, east, south])
        self.assertTrue(self.g.get_node(8) == end_node)

        end_node = self.g.get_node_via_turns([east, south, north, north])
        self.assertTrue(end_node is None)

        end_node = self.g.get_node_via_turns([east, south, west, south, west, north, north, east, south, east, north], start=1)
        self.assertTrue(self.g.get_node(2) == end_node)

if __name__ == '__main__':
    unittest.main()