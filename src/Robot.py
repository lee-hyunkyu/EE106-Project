from Graph import *

class Robot:

    def __init__(self):
        self._heading = Direction.NORTH()

    @property
    def heading(self):
        return self._heading

    def turn(self, heading):
        curr_heading = self.heading

        turned_heading = curr_heading
        number_of_clockwise_turns = 0
        while turned_heading != curr_heading:
            number_of_clockwise_turns += 1
            turned_heading = turned_heading.clockwise_turn_direction()
        degrees_to_turn = number_of_clockwise_turns * 90
        # TODO: send command to actually turn the robot

        self.curr_heading = heading
        return self.curr_heading
    
    # def is_node(homograph):
    #     detect corners via harris corner detection
    #     use homograph to detect distance b/w corners
    #     Allow some error however, in general, they should be a fixed distance apart
    #         Not sure if this is something I need to do. 
    #         I will have to figure out how well corner harris detection works
    #     Case 1: T intersection (2-4 corners)
    #         return True
    #     Case 2: Four way (4-8 corners)
    #         return True
    #     Case 3: Left/right True (2-4 corners)
    #         return True 
    #     Case 4: No corner (0 corners)
    #         return False