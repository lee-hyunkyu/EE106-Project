# Maze Project

## Path Finding 

More formally: **Given a map, can a robot find a way out**. Suppose I have a simple map of nodes and edges. This is fairly trivial. However a problem comes up. If I'm a robot, how do I know which way is which? For example, supose I have the following. 

~~~
    /------ C1
V   ------  C2
    \-----  C3
~~~

If I'm at V, how do I know which path to go to get to C1? This is fairly simple, when making the connection from V -> C1, just remember to tell V which directino C1 was in. **Not Relative** but with absolute coordinates (i.e. North/South/etc)

And from there, it's just a series of NORTH -> SOUTH -> WEST -> etc. directions and the robot has to follow that. 

## Maze Building

So this is directly related to the path finding. In pseudocode, here it is:

~~~
# Creates a graph using DFS search starting from robot's current position
def create_graph_dfs(robot, v=None): 

    # Initialization
    reset encoder value

    # Initialize graph if necessary
    if not node:
        g = Graph()
        v = g.add_node() # No name but an index is automatically given

    directions = v.determine_possible_directions()
    # Deadend has been reached
    if len(direction) == 0: 
        robot.turn_around()
        robot.move_until_node_reached()
        return None
    if end has been reached: 
        return 'Complete'

    entering_heading = robot.heading # Heading when robot entered the node
    opposite_of_entering_heading = opposite_heading(entering_heading)

    # The robot should be at v
    for dir in directions:
        if dir is current_heading.opposite(): # Makes sure it doesn't go backward
            continue                          # The connection should already be made!!!
        robot.turn(dir)

        # Robot still at start node
        robot.move_forward_until_node()
        
        # Robot now at a neighbor of v. Create correct connections
        u = g.add_node()
        v.neighbor[dir] = u
        u.neighbor[opposite_dir] = v

        # Recursive call
        done = create_graph_dfs(robot, u)
        if done == 'Complete':
            return g

        # Robot should still be at the neighbor of v (u)
        # Now I have to return to v
        robot.turn(dir.opposite_direction())
        robot.move_forward_until_node()
    return g
~~~

### Finding nodes

I refeer to some functions above. Here is how I might go about implementing them.

~~~
# returns all possible directions you could go from NODE (including backward)
def determine_possible_directions(node):

~~~

## Robot

Robot needs some kind of understanding of heading. Without it, it won't know which direction it's facing (NORTH, SOUTH, EAST, WEST). This way, it can quickly orient itself. 

A couple functions (i.e. turnLeft(), turnRight()) should be able to fix that. Or just ones that refer directory to the direction. (i.e. turn(direction) where direction = NORTH, SOUTH, EAST, WEST)

The robot also must be the one to determine whether or not it is at a node

~~~
def is_node(homograph):
    detect corners via harris corner detection
    use homograph to detect distance b/w corners
    Allow some error however, in general, they should be a fixed distance apart
        Not sure if this is something I need to do. 
        I will have to figure out how well corner harris detection works
    Case 1: T intersection (2-4 corners)
        return True
    Case 2: Four way (4-8 corners)
        return True
    Case 3: Left/right True (2-4 corners)
        return True 
    Case 4: No corner (0 corners)
        return False
~~~