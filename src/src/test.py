#!/usr/bin/env python
from __future__ import print_function
from Graph import *
import rospy
import tf
from std_msgs.msg import String
from sensor_msgs.msg import Imu
from sensor_msgs.msg import CompressedImage
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

def talker():
    rospy.init_node('talker', anonymous=True)
    command_topic = '/cmd_vel_mux/input/teleop'
    forward = 0
    clockwise = 1
    vel = Vector3()
    omega = Vector3()
    vel.x = 0
    vel.y = 0
    vel.z = 0
    omega.x = 0
    omega.y = 0
    omega.z = clockwise
    twist = Twist()
    twist.linear = vel
    twist.angular = omega
    pub = rospy.Publisher(command_topic, Twist, queue_size=10)
    r = rospy.Rate(10)  
    while not rospy.is_shutdown():  
        pub.publish(twist)
        r.sleep()

if __name__ == '__main__':
    try: 
        talker()
    except rospy.ROSInterruptException: pass
