from Graph import *
import unittest
import string
 
class TestGraph(unittest.TestCase):

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
        self.graph = Graph()
        self.assertTrue(len(self.graph.V)     == 0)
        self.assertTrue(self.next_index       == 0)

    def test_add_node(self):
        pass

    def test_get_node(self):
        pass

    def test_get_neighbors(self):
        pass
    # def test_breadth_first_search(self):
    #     pass

    # def test_dijkstras(self):
    #     pass

    # def test_find_min_path(self):
    #     pass

if __name__ == '__main__':
    unittest.main()