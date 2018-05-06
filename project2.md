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

def create_graph(robot, start_node): 
    reset encoder value

    v = create_node(start_node)
    directions = start_node.determine_possible_directions()
    entering_heading = robot.heading # Heading when robot entered the node
    opposite_of_entering_heading = opposite_heading(entering_heading)

    v.possible_directions = directions
    '''
    Something to consider here is that I'm not sure if I want v.children = directions to be a thing.
    And yet a complete map should be able to determine what all children are, including the one you came from. 
    '''

    v.neighbors = {dir: SomeNode(v, dir) for dir in directions} # Says how to get to SomeNode from v
                                                                # But every node should then be able to tell you            
                                                                # how to get from SomeNode to v

    for dir in directions:
        if dir is current_heading.opposite():
            continue
        robot.turn(dir)
        
















    if node is found: 
        create_new_node s_ # The robot is currently at s_
        create edge from s to s_ of length edge_length 
        turn left 
        left    = create_graph(s_)
        turn right 
        right   = create_graph(s_)
        turn forward
        forward = create_graph(s_)

    go back to s 
    '''
    I need to return to where I came from! 
    So the assumption after each create create_graph(t) is that I am back at t
    So after each create_graph (s_) I'm back at s_
    So to return back to s is to just make a 180' and go backward
    '''

    return;

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

