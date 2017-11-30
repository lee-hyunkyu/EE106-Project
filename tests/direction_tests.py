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

        self.assertTrue(south == north.opposite())
        self.assertTrue(north == south.opposite())
        self.assertTrue(east  == west.opposite())
        self.assertTrue(west  == east.opposite())

        self.assertFalse(south == west.opposite())
        self.assertFalse(south == east.opposite())
        self.assertFalse(north == west.opposite())
        self.assertFalse(north == east.opposite())

        self.assertFalse(south.opposite() == west)
        self.assertFalse(south.opposite() == east)
        self.assertFalse(north.opposite() == west)
        self.assertFalse(north.opposite() == east)

if __name__ == '__main__':
    unittest.main()