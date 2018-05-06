#!/usr/bin/env python
from __future__ import print_function
from Graph import *
import rospy
import tf
from std_msgs.msg import String
from sensor_msgs.msg import Imu
from sensor_msgs.msg import PointCloud2
from sensor_msgs.msg import CompressedImage
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError
import sys

import roslib
# roslib.load_manifest('my_package')
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
from ros_numpy import *
import time
from image_processing import *
from nav_msgs.msg import Odometry
from kobuki_msgs.msg import MotorPower
class Robot:

    def __init__(self):
        self._current_node      = None
        self._current_image     = None
        self._current_depth_image = None
        self._is_near_node      = None
        self._is_at_node        = True
        self._possible_directions_at_next_node = []

        self._should_save_image = False

        image_topic = '/camera/rgb/image_color'
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber(image_topic, Image,self.callback, queue_size=1)

        command_topic = '/mobile_base/commands/velocity'
        # rospy.init_node('robot')
        self.movement_pub = rospy.Publisher(command_topic, Twist , queue_size=1)
        self.r = rospy.Rate(10)

        # imu data
        imu_topic = '/mobile_base/sensors/imu_data'
        self.imu_sub = rospy.Subscriber(imu_topic, Imu, self.imu_callback, queue_size=1)
        self._should_save_imu_data = False
        self._imu_data = None

        # encoder data
        encoder_topic = '/odom'
        self.encoder_sub = rospy.Subscriber(encoder_topic, Odometry, self.encoders_callback, queue_size=1)
        self._should_save_encoder_data = False
        self._encoder_data = None

        # self._heading           = Direction.NORTH() # TODO? 
        self._north_heading     = self.get_imu_heading()

        self._headings          = [self._north_heading, self._north_heading + np.pi/2, self._north_heading + np.pi, self._north_heading - np.pi/2]
        self._headings          = np.array(self._headings) % (2*np.pi)
        self._heading           = self._north_heading
        # camself._constant_middle   = analyze(self.current_image())
        self._constant_middle   = analyze(self.current_image())[0]

    @property
    def heading(self):
        return self._heading

    def encoders_callback(self, ros_data):
        if self._should_save_encoder_data:
            self._should_save_encoder_data = False
            p = ros_data.pose.pose.position
            x, y, z = p.x, p.y, p.z
            self._encoder_data = x, y

    def encoder_data(self):
        self._encoder_data = None 
        self._should_save_encoder_data = True
        while self._encoder_data is None:
            rospy.sleep(.01)
        return self._encoder_data

    def imu_callback(self, ros_data):
        if self._should_save_imu_data:
            self._should_save_imu_data = False
            self._imu_data = ros_data
            # qx = ros_data.orientation.x
            # qy = ros_data.orientation.y
            # qz = ros_data.orientation.z
            # qw = ros_data.orientation.w
            # euler = tf.transformations.euler_from_quaternion((qx, qy, qz, qw))
            # print(euler)

    def imu_data(self):
        self._imu_data = None
        self._should_save_imu_data = True
        while self._imu_data is None:
            rospy.sleep(.01)
        return self._imu_data

    def get_imu_heading(self):
        imu = self.imu_data()
        qx = imu.orientation.x
        qy = imu.orientation.y
        qz = imu.orientation.z
        qw = imu.orientation.w
        euler = tf.transformations.euler_from_quaternion((qx, qy, qz, qw))

        heading = euler[2]
        if heading < 0:
            heading = heading + 2*np.pi
            heading = heading % (2*np.pi)
        return heading

    def callback(self, ros_data):
        if self._should_save_image:
            self._should_save_image = False
            data = image.image_to_numpy(ros_data)
            self._current_image = data

    def show_image(self, image=None):
        if self.current_image is None:
            return
        if image is not None:
            img = image
        else:
            img = self.current_image

    # def turn(self, heading):
    #     if heading == Direction.EAST():
    #         wanted_imu_heading = self._north_heading - np.pi/2
    #     if heading == Direction.WEST():
    #         wanted_imu_heading = self._north_heading + np.pi/2
    #     if heading == Direction.NORTH():
    #         wanted_imu_heading = self._north_heading
    #     if heading == Direction.SOUTH():
    #         wanted_imu_heading = self._north_heading + np.pi

    #     wanted_imu_heading = (wanted_imu_heading + 2*np.pi) % (2*np.pi)
    #     current_heading    = self.get_imu_heading()
    #     slack = 0.05
    #     speed = 0.5
    #     while abs(current_heading - wanted_imu_heading) > slack:
    #         # speed = 1
    #         # if abs(current_heading - wanted_imu_heading) < slack * 5:
    #         #     speed = 0.5
    #         self.move(0, -speed)
    #         current_heading    = self.get_imu_heading()
    #         print(current_heading, wanted_imu_heading)

        
    #     self.curr_heading = heading
    #     return self.curr_heading

    def turn_around(self):
        print(self._headings)
        self._heading      = self.get_imu_heading()
        wanted_imu_heading = self._heading + np.pi/2
        wanted_imu_heading = (wanted_imu_heading + np.pi*2) % (2*np.pi)
        print('a', wanted_imu_heading)
        minimum = np.inf 
        possible_heading = None
        for h in self._headings:
            print(abs(h-wanted_imu_heading), h)
            if abs(h - wanted_imu_heading) < minimum:
                minimum = abs(h - wanted_imu_heading)
                possible_heading = h
        wanted_imu_heading = possible_heading
        current_heading = self._heading
        slack = 0.1
        speed = 0.1
        while True:
            # speed = 1
            if abs(current_heading - wanted_imu_heading) > slack:
                self.move(0, speed)
            else:
                break
            # new_middle = analyze(self.current_image())
            # self.move(0, -.2)
            # if abs(self._constant_middle - new_middle) < 20:
            #     break
            current_heading    = self.get_imu_heading()
            print(current_heading, wanted_imu_heading)

        self.move(0, 0)
        self._heading = current_heading
        return self._heading

    def turn_left(self):
        print(self._headings)
        self._heading      = self.get_imu_heading()
        wanted_imu_heading = self._heading + np.pi/2
        wanted_imu_heading = (wanted_imu_heading + np.pi*2) % (2*np.pi)
        print('a', wanted_imu_heading)
        minimum = np.inf 
        possible_heading = None
        for h in self._headings:
            print(abs(h-wanted_imu_heading), h)
            if abs(h - wanted_imu_heading) < minimum:
                minimum = abs(h - wanted_imu_heading)
                possible_heading = h
        wanted_imu_heading = possible_heading
        print('b', wanted_imu_heading)
        # wanted_imu_heading = minimum
        current_heading = self._heading
        slack = 0.1
        speed = 0.1
        while True:
            # speed = 1
            if abs(current_heading - wanted_imu_heading) > slack:
                self.move(0, speed)
            else:
                break
            # new_middle = analyze(self.current_image())
            # self.move(0, -.2)
            # if abs(self._constant_middle - new_middle) < 20:
            #     break
            current_heading    = self.get_imu_heading()
            print(current_heading, wanted_imu_heading)

        self.move(0, 0)
        self._heading = current_heading
        return self._heading

    def turn_right(self):
        # self._constant_middle   = analyze(self.current_image())
        print(self._headings)
        self._heading      = self.get_imu_heading()
        wanted_imu_heading = self._heading - np.pi/2
        wanted_imu_heading = (wanted_imu_heading + np.pi*2) % (2*np.pi)
        print('a', wanted_imu_heading)
        minimum = np.inf 
        possible_heading = None
        for h in self._headings:
            print(abs(h-wanted_imu_heading), h)
            if abs(h - wanted_imu_heading) < minimum:
                minimum = abs(h - wanted_imu_heading)
                possible_heading = h
        wanted_imu_heading = possible_heading
        print('b', wanted_imu_heading)
        # wanted_imu_heading = minimum
        current_heading = self._heading
        slack = 0.1
        speed = 0.1
        while True:
            # speed = 1
            if abs(current_heading - wanted_imu_heading) > slack:
                self.move(0, -speed)
            else:
                break
            # new_middle = analyze(self.current_image())
            # self.move(0, -.2)
            # if abs(self._constant_middle - new_middle) < 20:
            #     break
            current_heading    = self.get_imu_heading()
            # print(current_heading, wanted_imu_heading)

        self.move(0, 0)
        self._heading = current_heading
        return self._heading

    def turn(self, angle):
        self._heading      = self.get_imu_heading()
        wanted_imu_heading = self._heading + angle
        wanted_imu_heading = (wanted_imu_heading + np.pi*2) % (2*np.pi)
        # wanted_imu_heading = minimum
        current_heading = self._heading
        slack = 0.05
        speed = 0.2
        while True:
            # speed = 1
            if abs(current_heading - wanted_imu_heading) > slack * 5:
                speed = 0.3
            else:
                speed = 0.2
            if abs(current_heading - wanted_imu_heading) > slack:
                self.move(0, -speed)
            else:
                break
            current_heading    = self.get_imu_heading()
            # print(current_heading, wanted_imu_heading)

        self.move(0, 0)
        self._heading = current_heading
        return self._heading

    def move(self, forward, counter):
        vel = Vector3()
        omega = Vector3()
        vel.x = forward
        vel.y = 0
        vel.z = 0
        omega.x = 0
        omega.y = 0
        omega.z = counter
        twist = Twist()
        twist.linear = vel
        twist.angular = omega
        start_time = rospy.get_time()
        while rospy.get_time() - start_time < 1:
            self.movement_pub.publish(twist)
        return 

    # TODO: 
    # This function is to determine if I am near a node i.e.
    # The camera can see corners or a wall that's in front
    def set_is_near_node(self, image):
        print('set_is_near_node')

    @property
    def is_near_node(self):
        return self._is_near_node

    # TODO
    def move_to_next(self):
        while True:
            self.move_one_unit()
            self.orient()
            img = self.current_image()
            _, left, right, forward = analyze(img)
            if left:
                self.move(0, 0)
                self.move_one_unit()
                self.turn_left()
                self.orient()
                return 
            if not left and not forward and right:
                self.move(0, 0)
                self.move_one_unit()
                self.turn_right()
                self.orient()
                return
            if not left and not forward and not right:
                self.move(0, 0)
                self.move_one_unit()
                self.turn_right()
                self.orient()
                self.move_one_unit()
                return 

    def move_one_unit(self):
        start = rospy.get_time()
        x0, y0 = self.encoder_data()
        curr = 0

        img = self.current_image()
        l_med, r_med, l, r = get_med_left_right(img)
        if l and not r:
            median = 183 - l_med
        elif r and not l:
            median = 183 - r_med
        elif l and r:
            median = 183 - (l_med + r_med)/2
        else:
            median = False
        if median < 0:
            final = 0.38 + 0.21*median/90
        elif median > 0:
            final = 0.38 + 0.21*median/115
        else:
            final = 0.38
        print(median, final)
        while curr < final:
            x, y = self.encoder_data()
            x = abs(x - x0)
            y = abs(y - y0)
            curr = np.sqrt(x**2 + y**2)
            self.move(0.2, 0)
        
        # if self._is_near_node:
        #     self._is_near_node = False
        #     self._is_at_node    = True
        # self.orient()
        
    # Makes sure the line on the ground matches up
    def orient(self):
        start = rospy.get_time()
        slack = 15
        start_image = rospy.get_time()
        img = r.current_image()
        # cv2.imshow('img', img)
        # cv2.waitKey(0)
        start_anal = rospy.get_time()
        median_difference = get_med_diff(img)
        if not median_difference:
            return 
        speed = 0.1
        while True and median_difference is not None:
            # start = rospy.get_time()
            difference = median_difference - self._constant_middle
            if abs(difference) > slack:
                if difference > 0:
                    self.move(0, -speed)
                else:
                    self.move(0, speed)
            else:
                break
            # if abs(median_difference - self._constant_middle) > 100:
            #     speed *= 3
            img = r.current_image()
            median_difference = get_med_diff(img)
        
        self.move(0, 0)
        # median_difference, left, right, forward = analysis
        # median_difference = analysis
        # speed = 0.1
        # cv2.imshow('img', img)
        # cv2.waitKey(1)
        # print(median_difference)
        # while median_difference > slack and median_difference is not None:
        #     self.move(0, -speed)
        #     img = r.current_image()
        #     median_difference = analyze(img)[0]
        #     print('>', median_difference)
        # while median_difference < -slack and median_difference is not None:
        #     self.move(0, speed)
        #     img = r.current_image()
        #     median_difference = analyze(img)[0]
        #     print('<', median_difference)
        # self._is_near_node = left or right
        # if self._is_near_node: 
        #     self._possible_directions_at_next_node = []
        #     if left:
        #         self._possible_directions_at_next_node += [self._heading.counter_clockwise_turn_direction()]
        #     if right:
        #         self._possible_directions_at_next_node += [Direction.clockwise_turn_direction()]
        #     if forward:
        #         self._possible_directions_at_next_node += self._heading

    # TODO
    def move_forward_until_next_node(self):
        while not self.is_near_node():
            # TODO: send command to actually move forward
            pass
        # Do some checks to make sure you're positioned correctly
        # i.e. make sure you're not at a dead end
        # if not positino yourself s.t the paths are all able to be seen if turned
        return True

    def create_graph_dfs(self, v=None): 
        pass
        # # Initialization
        # # TODO reset encoder value

        # # Initialize graph if necessary
        # if not v:
        #     g = Graph()
        #     v = g.add_node()


        # entering_direction = self.heading # Heading when robot entered the node
        # opposite_of_entering_heading = entering_direction.opposite_direction()

        # # Assume that the robot is at node v
        # self._current_node = v
        # directions = self.determine_possible_directions()
        # # Deadend has been reached
        # if len(direction) == 1: # Backwards only 
        #     self.turn(opposite_of_entering_heading)
        #     node = v.get_neighbor(opposite_of_entering_heading)
        #     self.move_to_node(node)
        #     return None
        # # TODO
        # # if end has been reached: 
        #     # return 'Complete'

        # # The robot should be at v
        # for dir in directions:
        #     if dir is current_heading.opposite_direction(): # Makes sure it doesn't go backward
        #         continue                                    # The connection should already be made!!!
        #     self.turn(dir)

        #     # Robot still at start node
        #     self.move_forward_until_next_node()
            
        #     # Robot now at a neighbor of v. Create correct connections
        #     u = g.add_node()
        #     v.add_neighbor(u, dir) # The neighbor of u is also update automatically

        #     # Recursive call
        #     done = create_graph_dfs(robot, u)
        #     if done == 'Complete': # End has been reached
        #         return g

        #     # Robot should still be at the neighbor of v (u)
        #     # Now I have to return to v
        #     self.move_to_node(v)
        # return g

    def solve_maze(self):
        while True:
            print('self.orient')
            self.orient()
            img = self.current_image()
            l_med, r_med, left, right = get_med_left_right(img)
            print('l, r', l_med, r_med, left, right)
            forward = get_forward(img)
            print('forward', forward)
            if left:
                self.move(0, 0)
                self.move_one_unit()
                self.turn_left()
                self.orient()
                continue
            white   = is_end(img)
            print('white', white)
            if white:
                self.move_one_unit()
                self.move_one_unit()
                return
            if forward: 
                self.move(0, 0)
                self.move_one_unit()
                self.orient()
                continue
            if right:
                self.move(0, 0)
                self.move_one_unit()
                self.turn_right()
                self.orient()
                continue
            self.move(0, 0)
            self.turn_right()

    # Use opencv?
    def wall_in_front(self):
        pass

    def current_image(self):
        self._current_image = None
        # self._current_depth_image = None
        self._should_save_image = True
        while self._current_image is None: # Ensure that the image I'm seeing is the image I want to see
            rospy.sleep(.01)
        # self._should_save_depth = True
        # while self._current_depth_image is None: # Ensure that the image I'm seeing is the image I want to see
        #     pass
        return self._current_image#, self._current_depth_image


if __name__ == '__main__':
    rospy.init_node('robot', anonymous=False)
    r = Robot()
    r.solve_maze()
    # while not rospy.is_shutdown():
    # r.move_one_unit()
    # r.move_one_unit()
    # r.move_one_unit()
    # r.solve_maze()
    # r.turn_left()
    # r.orient()
    # print('done')
    # rospy.sleep(1)
    # r.turn_left()
    # r.orient()
    # print('done')
    # rospy.sleep(1)
    # r.turn_left()
    # r.orient()
    # print('done')
    # rospy.sleep(1)
    # r.turn_left()
    # r.orient()
    # print('done')
    # r.solve_maze()
# print('move')
# r.move_one_unit()
# print('done')
# r.orient()
# print("move")
# r.move_one_unit()
# print('done')
        # r.orient()
        # rospy.sleep(2)
    # import time
    # time.sleep(100)
    # r.move_one_unit()
    # r.orient()
    # r.move_one_unit()
    # r.orient()
    # r.move_one_unit()
    # r.orient()
    # r.turn_left()
    # r.orient()
    # r.turn_right()
    # r.orient()
    # import time; time.sleep(2)
    # r.turn_right()
    # r.orient()
    # r.move_one_unit()
    # r.orient()
    # r.move_one_unit()
    # r.orient()
    # r.turn_right()
    # r.move_one_unit()
    # r.orient()
    # r.move_one_unit()
    # r.orient()


        