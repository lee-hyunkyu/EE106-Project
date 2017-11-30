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

    def test_clockwise_turn_direction(self):
        north = Direction.NORTH()

        turned = north.clockwise_turn_direction()
        self.assertTrue(turned == Direction.EAST())
        turned = turned.clockwise_turn_direction()
        self.assertTrue(turned == Direction.SOUTH())
        turned = turned.clockwise_turn_direction()
        self.assertTrue(turned == Direction.WEST())
        turned = turned.clockwise_turn_direction()
        self.assertTrue(turned == Direction.NORTH())

if __name__ == '__main__':
    unittest.main()