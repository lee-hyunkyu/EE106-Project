#!/usr/bin/env python
from __future__ import print_function
import rospy
import tf
from std_msgs.msg import String
from sensor_msgs.msg import Imu
from sensor_msgs.msg import CompressedImage
import cv2
from cv_bridge import CvBridge, CvBridgeError
import sys
import roslib
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
import numpy as np

class ImageSubscriber:

  def __init__(self, topic):
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber(topic, CompressedImage,self.callback, queue_size=1)

  def callback(self,ros_data):
  	# Convert Image
    np_arr = np.fromstring(ros_data.data, np.uint8)
    image_np = cv2.imdecode(np_arr, cv2.CV_LOAD_IMAGE_COLOR)
    return image_np
