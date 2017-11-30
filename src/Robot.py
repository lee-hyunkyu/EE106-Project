from Graph import *

class Robot:

    def __init__(self):
        self._heading      = Direction.NORTH()
        self._current_node = None

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
        if degrees_to_turn == 270:
            degrees_to_turn = -90
        # TODO: send command to actually turn the robot

        self.curr_heading = heading
        return self.curr_heading

    # TODO: 
    # This function is to determine if I am near a node i.e.
    # The camera can see corners or a wall that's in front
    def is_near_node(self):
        pass

    # TODO
    def move_to_node(self, node):
        pass

    # TODO
    def move_forward_until_next_node(self):
        while not self.is_near_node():
            # TODO: send command to actually move forward
            pass
        # Do some checks to make sure you're positioned correctly
        # i.e. make sure you're not at a dead end
        # if not positino yourself s.t the paths are all able to be seen if turned
        return True

    def create_graph_dfs(robot, v=None): 

        # Initialization
        # TODO reset encoder value

        # Initialize graph if necessary
        if not v:
            g = Graph()
            v = g.add_node()


        entering_direction = self.heading # Heading when robot entered the node
        opposite_of_entering_heading = entering_direction.opposite_direction()

        # Assume that the robot is at node v
        self._current_node = v
        directions = self.determine_possible_directions()
        # Deadend has been reached
        if len(direction) == 1: # Backwards only 
            self.turn(opposite_of_entering_heading)
            node = v.get_neighbor(opposite_of_entering_heading)
            self.move_to_node(node)
            return None
        # TODO
        # if end has been reached: 
            # return 'Complete'

        # The robot should be at v
        for dir in directions:
            if dir is current_heading.opposite_direction(): # Makes sure it doesn't go backward
                continue                                    # The connection should already be made!!!
            self.turn(dir)

            # Robot still at start node
            self.move_forward_until_next_node()
            
            # Robot now at a neighbor of v. Create correct connections
            u = g.add_node()
            v.add_neighbor(u, dir) # The neighbor of u is also update automatically

            # Recursive call
            done = create_graph_dfs(robot, u)
            if done == 'Complete': # End has been reached
                return g

            # Robot should still be at the neighbor of v (u)
            # Now I have to return to v
            self.move_to_node(v)

        return g
    
    def determine_possible_directions(self):
        heading = self.heading
        possible_directions = []
        for i in range(4):
            print(i, heading)
            if not self.wall_in_front():
                possible_directions += [heading]
            heading = heading.clockwise_turn_direction()
            self.turn(heading)
        return possible_directions

    # Use opencv?
    def wall_in_front(self):
        pass


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

if __name__ == '__main__':
    r = Robot()
    r.determine_possible_directions()