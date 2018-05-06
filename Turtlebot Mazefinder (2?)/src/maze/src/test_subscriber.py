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
# roslib.load_manifest('my_package')
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
from nav_msgs.msg import Odometry


class image_converter:

  def __init__(self):
    # self.image_pub = rospy.Publisher("image_topic_2",Image)

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/odom",,self.callback, queue_size=1)

  def callback(self,ros_data):
    # np_arr = np.fromstring(ros_data.data, np.uint8)
    # image_np = cv2.imdecode(np_arr, cv2.CV_LOAD_IMAGE_COLOR)


    # # try:
    # #   cv_image = self.bridge.imgmsg_to_cv2(msg.data, "bgr8")
    # # except CvBridgeError as e:
    # #   print(e)

    # # (rows,cols,channels) = cv_image.shape
    # # if cols > 60 and rows > 60 :
    # #   cv2.circle(cv_image, (50,50), 10, 255)


    # method = "HARRIS"
    # feat_det = cv2.FeatureDetector_create(method)
    
    # featPoints = feat_det.detect(cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY))
    # for p in featPoints:
    # 	x, y = p.pt
    # 	cv2.circle(image_np, (int(x), int(y)), 3, (0, 0, 255), -1)

    # cv2.imshow("Image window", image_np)
    # cv2.waitKey(1)

    # try:
    #   self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    # except CvBridgeError as e:
    #   print(e)
    # print(ros_data.pose.pose.position)

def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)

# def callback(message):
# 	#import pdb; pdb.set_trace()
# 	# qx = message.orientation.x
# 	# qy = message.orientation.y
# 	# qz = message.orientation.z
# 	# qw = message.orientation.w
# 	# euler = tf.transformations.euler_from_quaternion((qx, qy, qz, qw))
# 	# roll, pitch, yaw = euler
# 	# print('roll\t {}'.format(roll))
# 	# print('pitch\t {}'.format(pitch))
# 	# print('yaw\t {}'.format(yaw))
# 	# print(message)
# 	image = message
# 	import pdb; pdb.set_trace()

# 	cv2.namedWindow("Camera")
# 	cv2.imshow("Camera", image)



# def listener():
# 	rospy.init_node('listener', anonymous=True)
# 	rospy.Subscriber('/camera/rgb/image_raw/compressed', CompressedImage, callback)
# 	rospy.spin()

# if __name__ == '__main__':
# 	listener()