# Introduction

Our goal was to have a Turtlebot autonomously navigate a maze from beginning to end and eventually teach another turtlebot to do the same by publishing a message. 

We felt that this would solve search and rescue problems by allowing a robot to autonomously navigate an unknown area but also send data about the area to speed up other robots working in the same area. 


# Design

## Design Criteria

1. The robot must be able to navigate a maze
    1.1 The robot must be able to move consistently
    1.2 The robot has to be able to turn consisntently
    1.3 The robot has to be able to plan where to go at each time step
2. The robot must be able to create a graph of the maze
3. The robot must be able to recieve and send information about the maze

## Our Design

Our design was related mosly to the look of the maze. As we were going to use an RGB camera to navigate the maze, how the maze looked would determine the feasibility moving through it. The maze went through several iterations. At first, we considered building a maze lined by wood. However, due to the constraints that this would bring (specifically cost and flexibility), we considered having a maze outline the walls of the maze. In the end, we landed on having bright blue tape outline the paths of the maze.

## Relation to Real-World Criteria

However, in order for this robot to be useful in a real-world applicaiton, we would need to improve its speed and versatility. 

For one, the robot is very slow in navigating the maze. While we were able to optimize and significantly speed up the processing time when analyzing images, unfortunately, no fast control system was implemented and as such a lot of time was spent on ensuring smooth motion.

Moreover, as the maze was built to have a blue line outline the maze, rather than have walls, means that this robot cannot currently accurately detect 'walls' and instead relies on the location of a known object. In the real world, it would be more ideal for a robot to do the former. 

# Implementation

## Sensing

We relied on the Turtlebot's RGB camera and its encoders. The camera was required to determine the paths outlined by the maze. The encoder data allowed for constant correction and ensure that the robot did not stray too far from the wanted path. 

## Planning

### Follow the Wall

If caught in a maze, one way to ensure that you do not get lost and that you exit successfully is to keep one hand on one wall and follow the wall. This is what we did for the robot. 

~~~
If you can take a left:
    take the left
If you can go forward: 
    go forward
If you can take a right
    go right
Turn around
~~~

In order to implement this, we needed to be able to determine which directions could be possible. Rather than having the robot determine this at the intersection, we decided instead to have the robot determine these directions **1 node away**. This is because if we were to try to determine this at the intersection would require a 360 degree turn at every node which would slow donw the robot considerably. 

To determine these directions, we took an image and filtered out all of the color that was not the correct shade of blue using OpenCV. We then cropped the image into three parts: the "left", the "right", and the "forward". With these portions, it was trivial to determine if blue tape indicating the maze existed. In full, our planning became

~~~
If you can take a left:
    go forward to the node
    take the left
else If you can go forward: 
    go forward to the node
    go forward
else If you can take a right
    go forward to the node
    go right
else
    Turn around
~~~

### Accurate movement

A challenge quickly presented itself: error accumulated despite the use of encoders. This accumulation presented itself when the robot was moving linearly and when it was rotating in place. We solved these problems in three part. 

#### Heading

When turning, we noticed that simply adding/subtracting 90 degrees to the current heading read by the sensors lead to significant drift as at each turn the turtlebot overshot. Instead in the beginning, we saved the heading value for all four cardinal directions. We would have the turtlebot turn to match these heading values. 

#### Orientation

That however did not fix the overshooting problem. It merely ensured that error would not grow. 

After any movement, the turtlebot would 'orient' itself by determining the location of the blue line in front. It would then rotate appropriately to center the blue line as best as possible. 

#### Correction

While these two fixes ensured that the turtlebot was facing the right way, it didn't ensure that the turtlebot move forward the correct number of inches. When given a constant encoder value to reach (i.e. 42 ticks above the current value), the turtlebot would both overshoot and undershoot randomly. While this wasn't too important when the turtlebot was moving in a straight line, when the turtlebot appraoched a corner this became a big problem. Afterall, by not having the turtlebot land properly at the intersection meant that after a 90 degree turn, the turtlebot would not be able to see the blue line as it would too far to the right or left. We fixed this when determinig the possible directions. 

As this was only a problem when there was a left or right turn, we first looked to see if a turn existed. If so, we determined how far away the intersection was and dynamically changed the encoder value the robot would move to. As this was an unexact science, this required several iterations of experimenting with values to get an adequate feedback gain. 

### The Complete System

Therefore, at every step, the robot

1. Takes a picture and uses it to orient himself to the blue line
2. Determine if a left or right turns needs to be taken with the same picture
3. Move forward and turns (or doesn't turn) based on its analysis in the previous step. 
    3.1 If a left turns is available, take it. 
    3.2 If not but you can move forward, take it.
    3.3 If not but a right turn is available, take it. 
    3.4 If none of these are available, turn around. 
4. Repeat until the end is found. 

**Topics used**:
- `/camera/rgb/image_color`
- `/mobile_base/commands/velocity`
- `/mobile_base/sensors/imu_data`
- `/odom`

**Libraries used**: 
- numpy
- opencv


## Results

With these feedback control systems, the robot was able move through the maze, albeit slowly. 

[Add video here]

[Add link to Github here]

## Team

Joseph Kroeger

Michael Lee. 

Michael Lee is a third-year undergrad in Electrical Engineering and Computer Science at UC Berkeley. 

# Conclusion 

While we were able to achieve our goal of having a turtlebot navigate a maze, we were unable to expand upon this to teach another turtlebot to do the same. 

Part way through the project we felt that the second aspect of our goal would not be able to be met due to time constraints. As such, much of the infrastrucutre such as the message creation of a map of the maze which had already been built went unused. In the future, we would like to expand on this idea. 

One of the reasons we dropped this aspect was because of a particular bug we came across. When publishing to `/cmd_vel_mux/input/teleop`, we would often get an error saying that the velocity command had been zeroed. Which meant that the robot simply would not move desite correctly publishing a twist. We eventually learned that this was due to the time between published messages, time that the robot was spening analyzing the images it recieved from the camera. We worked to optimize the process analyzing the image and by doing so was able to more reliably control the robot. 

Moreover, how we actually go through our maze is a little flawed. As we simply 'follow the wall', this means that no map is ever created. The robot essentially knows no more about the maze at the end than what it knew at the beginning. A lot of the code already exists to properly create this maze and we given more time, we would like to have the robot, when navigating the maze, build up a graph representing the maze. 







