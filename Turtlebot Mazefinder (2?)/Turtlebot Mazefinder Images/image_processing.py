import cv2

# Binarize an image
# cv2.threahold(src, thresh, maxval, type) -> retval, dst
    # TYPE: THRESH_BINARY is probably the way to go

# From binary image, look for edges? Hough Lines should do
# #!/usr/bin/python

# '''
# This example illustrates how to use Hough Transform to find lines

# Usage:
#     houghlines.py [<image_name>]
#     image argument defaults to ../data/pic1.png
# '''

# # Python 2/3 compatibility
# from __future__ import print_function

# import cv2
# import numpy as np
# import sys
# import math

# if __name__ == '__main__':
#     print(__doc__)

#     try:
#         fn = sys.argv[1]
#     except IndexError:
#         fn = "../data/pic1.png"

#     src = cv2.imread(fn)
#     dst = cv2.Canny(src, 50, 200)
#     cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)

#     if True: # HoughLinesP
#         lines = cv2.HoughLinesP(dst, 1, math.pi/180.0, 40, np.array([]), 50, 10)
#         a,b,c = lines.shape
#         for i in range(a):
#             x1, y1, x2, y2 = lines[i][0]
#             cv2.line(cdst, (x0, y0), (x_final, y_final), (0, 0, 255), 3, cv2.LINE_AA)

#     else:    # HoughLines
#         lines = cv2.HoughLines(dst, 1, math.pi/180.0, 50, np.array([]), 0, 0)
#         if lines is not None:
#             a,b,c = lines.shape
#             for i in range(a):
#                 rho = lines[i][0][0]
#                 theta = lines[i][0][1]
#                 a = math.cos(theta)
#                 b = math.sin(theta)
#                 x0, y0 = a*rho, b*rho
#                 pt1 = ( int(x0+1000*(-b)), int(y0+1000*(a)) )
#                 pt2 = ( int(x0-1000*(-b)), int(y0-1000*(a)) )
#                 cv2.line(cdst, pt1, pt2, (0, 0, 255), 3, cv2.LINE_AA)

    
#     cv2.imshow("detected lines", cdst)
#     cv2.waitKey(0)

#     cv2.imshow("source", src)
#     cv2.waitKey(0)

import cv2
import numpy as np
import math
import sys

max_img_num = 1110

def line_is_vertical(x1, y1, x2, y2):
    if x1 == x2:
        return True
    m = (y1 - y2)/(x1 - x2)
    return  (m > 1 and m < np.inf) or (m > -np.inf and m < -1)

def distance_to_top(x1, y1, x2, y2):
    # Assume horizontal line
    m           = (y2 - y1)/(x2 - x1)
    mid_point_x = abs((x2 - x1)/2)
    mid_point_y = m * (mid_point_x - x1) + y1
    return mid_point_y

def distance_from_center(x1, x2):
    mid_point_x = abs(x2 - x1)/2
    return mid_point_x 

def should_draw_corner(x1, y1, threshold, corners):
    low_y  = int(y1 - threshold/2)
    high_y = int(low_y + threshold)
    low_x  = int(x1 - threshold/2)
    high_x = int(low_x + threshold)
    # import pdb; pdb.set_trace()
    low_x  = max(0, low_x)
    low_y  = max(0, low_y)
    high_x = min(corners.shape[1], high_x)
    high_y = min(corners.shape[1], high_y)
    return sum(sum(corners[low_y:high_y, low_x:high_x])) != 0

def analyze(img):


for img_num in range(169):
    img = cv2.imread('images3/left{:04d}.jpg'.format(img_num))

    src = img
    # delta = 25
    # low = np.array([125, 0, 0])
    # high = np.array([200, 255, 255])
    # med = np.array([171, 110, 78])
    # low = med - delta
    # high = med + delta
    # src = cv2.inRange(src, low, high)
    # src = cv2.medianBlur(src, 5)
    # src1 = cv2.bitwise_not(src)

    dst = cv2.Canny(src, 50, 200) # Detect the edges
    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)

    blockSize = 2
    apertureSize = 3
    k = 0.1
    import pdb; pdb.set_trace()
    corners = cv2.cornerHarris(dst, blockSize, apertureSize, k, cv2.BORDER_DEFAULT)

    lines = cv2.HoughLinesP(dst, 1, math.pi/200, 40, np.array([]), 70, 20)
    if lines is None:
        continue
    a,b,c = lines.shape
    num_of_vertical_lines = 0
    for i in range(a):
        # import pdb; pdb.set_trace()
        x1, y1, x2, y2 = lines[i][0]
        if not line_is_vertical(x1, y1, x2, y2):
            continue
        
        mid_point_x = abs(x2 - x1)/2

        num_of_vertical_lines += 1



        if should_draw_corner(x1, y1, 10, corners):
            cv2.circle(cdst, (x1, y1), 5, (0, 0, 255))
        if should_draw_corner(x2, y2, 10, corners):
            cv2.circle(cdst, (x2, y2), 5, (0, 0, 255))
        cv2.line(cdst, (x1, y1), (x2,y2), (0, 0, 255), 2, cv2.LINE_AA)
    print(num_of_vertical_lines)
    cv2.imshow('original', img)
    cv2.imshow("src", cdst)
    cv2.waitKey(100)
