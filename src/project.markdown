#!/usr/bin/env python

# Path Finding
# S is the node I'm starting from and is of type Node? 
def create_graph(s): 
    reset encoder value
    Assume one direction forward in the very beginning!
    Go forward until another node is found


    edge_length = read encoder value
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

'''
The function here may be too complicated. In the create_graph, I do turn left/right and look forward. 
I can simply look to see if there is a 'wall' in front of me or not. 
This could simply be a check for corners. What we could do is color code the edges.? 
'''
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