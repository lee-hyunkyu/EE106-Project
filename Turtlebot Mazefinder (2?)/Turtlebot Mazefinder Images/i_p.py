#!/usr/bin/env python
import cv2
# import rospy
# from Robot import *

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
# import sys

max_img_num = 1110

def line_is_vertical(x1, y1, x2, y2):
    if x1 == x2:
        return True
    m = (y1 - y2)/(x1 - x2)
    return  (m > 1 and m < np.inf) or (m > -np.inf and m < -1)

def line_is_horizontal(x1, y1, x2, y2):
    if x1 == x2:
        return True
    x_min = min(x1, x2)

    if x_min == x1:
        m = (y2 - y1)/(x2 - x1)
    else:
        m = (y1 - y2)/(x1 - x2) 
    
    return  -1 < m < 1

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

def get_med_diff(img):
    cv2.imshow('original image', img)
    immediate_front = img[200:300, :]
    immediate_front = cv2.medianBlur(immediate_front, 5)
    cv2.imshow('cropped', immediate_front)
    hsv_l = (90, 60, 0)
    hsv_h = (150, 255, 255)
    immediate_front = cv2.cvtColor(immediate_front, cv2.COLOR_BGR2HSV)
    immediate_front = cv2.inRange(immediate_front, hsv_l, hsv_h)   
    cv2.imshow('filtered', immediate_front)
    # for row in range(len(immediate_front)):
    #     for col in range(len(immediate_front[row])):
    #         if row < immediate_front.shape[0] - 200 or row > immediate_front.shape[0] - 100:
    #             immediate_front[row][col] = 0
    
    median_col = img.shape[1]/2
    median_row = img.shape[0]/2
    # cv2.imshow('med', immediate_front)
    # cv2.waitKey(0)
    locations = np.where(immediate_front)[1]
    median = sum(locations)/len(locations) 

    median_diff = (median - median_row) - 60    

    img[200:300] = cv2.cvtColor(immediate_front, cv2.COLOR_GRAY2RGB)
    cv2.imshow('orienting', img)
    cv2.waitKey(0)
    return median_diff        

def get_med_right_left(img):
    # cv2.imshow('orig', img)
    src     = img[100:350, :]
    left    = src[:, 0:180]
    right   = src[:, 540:]
    src = cv2.medianBlur(src, 5)
    hsv_l = (90, 60, 0)
    hsv_h = (150, 255, 255)
    left = cv2.cvtColor(left, cv2.COLOR_BGR2HSV)
    left = cv2.inRange(left, hsv_l, hsv_h)   
    right = cv2.cvtColor(right, cv2.COLOR_BGR2HSV)
    right = cv2.inRange(right, hsv_l, hsv_h)   
    
    median_left, median_right = None, None

    locations = np.where(left)[0]
    should_turn_left = sum(locations) > 20000
    if len(locations) and should_turn_left:
        median_left = sum(locations)/len(locations) 
        median_left += 100


    locations = np.where(right)[0]
    should_turn_right = sum(locations) > 20000
    if len(locations) and should_turn_right:
        median_right = sum(locations)/len(locations) 
        median_right += 100

    # cv2.imshow('left', left)
    # cv2.imshow('right', right)
    # cv2.waitKey(0)

    img[100:350, 0:180] = cv2.cvtColor(left, cv2.COLOR_GRAY2RGB)
    img[100:350, 540:] = cv2.cvtColor(right, cv2.COLOR_GRAY2RGB)
    cv2.imshow('Correcting', img)  
    cv2.waitKey(0)

    return median_left, median_right, should_turn_left, should_turn_right

def get_forward(img):
    cv2.imshow('img', img)
    src = img[70:150, 250:430]
    src = cv2.medianBlur(src, 5)
    hsv_l = (90, 60, 0)
    hsv_h = (150, 255, 255)
    src = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    src = cv2.inRange(src, hsv_l, hsv_h)   
    cv2.imshow('src', src)
    cv2.waitKey(0)
    print(sum(sum(src)))
    return sum(sum(src)) > 7000

def is_end(img):
    white   = img[0:int(img.shape[0]/2), 100:500]
    # cv2.imshow('white', white)
    # cv2.waitKey(0)
    white   = cv2.medianBlur(white, 5)
    white   = cv2.cvtColor(white, cv2.COLOR_BGR2GRAY)
    white   = cv2.inRange(white, 200, 255)
    white   = cv2.dilate(white, (3, 3))


    locations = np.where(white)[1]
    return len(locations) > 0 and sum(locations) > 50000

def analyze(img):
    immediate_front = img
    immediate_front = cv2.medianBlur(immediate_front, 5)
    immediate_front = cv2.medianBlur(immediate_front, 5)
    immediate_front = cv2.medianBlur(immediate_front, 5)
    left = np.empty_like(immediate_front)
    right = np.empty_like(immediate_front)
    forward = np.empty_like(immediate_front)
    white   = np.empty_like(immediate_front)
    np.copyto(left, immediate_front)
    np.copyto(right, immediate_front)
    np.copyto(forward, immediate_front)
    np.copyto(white, immediate_front)

    hsv_l = (90, 60, 0)
    hsv_h = (150, 255, 255)
    immediate_front = cv2.cvtColor(immediate_front, cv2.COLOR_BGR2HSV)
    immediate_front = cv2.inRange(immediate_front, hsv_l, hsv_h)   

    white = cv2.cvtColor(white, cv2.COLOR_BGR2GRAY)
    white = cv2.inRange(white, 220, 255)
    white = cv2.dilate(white, (3, 3))
    # contours = cv2.findContours(white, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # print(contours)

    cv2.imshow('white', immediate_front)
    cv2.imshow('orig', left)
    cv2.waitKey(0)

    median_col = img.shape[1]/2
    median_row = img.shape[0]/2

    for row in range(len(immediate_front)):
        for col in range(len(immediate_front[row])):
            if row < img.shape[0] - 200 or row > img.shape[0] - 100:
                immediate_front[row][col] = 0
            if col > median_col/2 or row < median_row/2:
                left[row][col] = 0
            if col < 3*median_col/2 or row < median_row/2:
                right[row][col] = 0
            if row > median_row/1.4 or abs(median_col - col) > median_col/3 or row < median_row/4:
                forward[row][col] = 0

    locations = np.where(immediate_front)[1]
    if len(locations) > 3000:
        median = sum(locations)/len(locations)
        median_diff = (median - median_row)
    else:
        median_diff = None

    cv2.imshow('forward', immediate_front)
    cv2.waitKey(1)

    print(median_diff)

    left = sum(sum(left)) > 25000
    right = sum(sum(right)) > 25000
    forward = sum(sum(forward)) > 5000



    # print((median - median_row), left, right, forward)
    # cv2.imshow('analyzed', immediate_front)
    


    return median_diff, left, right, forward


def get_num_vertical_lines(img):
    src = img
    src = cv2.medianBlur(src, 5)
    src = cv2.medianBlur(src, 5)
    src = cv2.medianBlur(src, 5)

    hsv_l = (90, 60, 0)
    hsv_h = (150, 255, 255)

    src = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    src = cv2.inRange(src, hsv_l, hsv_h)   

    dst = cv2.Canny(src, 50, 200) # Detect the edges
    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)

    # blockSize = 2
    # apertureSize = 3
    # k = 0.1

    # method = "FAST"
    # feat_det = cv2.FeatureDetector_create(method)
    # featPoints = feat_det.detect(dst)
    # corners = [(p.pt[0], p.pt[1]) for p in featPoints]
    lines = cv2.HoughLinesP(dst, 1, np.pi/180, 50, np.array([]), 30, 20)

    if lines is None:
        return
    a,b,c = lines.shape
    num_of_vertical_lines = 0
    num_of_horizontal_lines = 0
    for i in range(b):
        x1, y1, x2, y2 = lines[0][i]
        median_x = abs(x1 + x2)/2
        median_y = abs(y1 + y2)/2
        median_of_image = np.array(src.shape)/2
        if abs(median_x - median_of_image[1]) < 30 and median_y > median_of_image[0] and line_is_vertical(x1, y1, x2, y2):
            num_of_vertical_lines += 1
        if line_is_horizontal(x1, y1, x2, y2):
            num_of_horizontal_lines += 1
            cv2.line(cdst, (x1, y1), (x2,y2), (0, 0, 255), 2)#, cv2.LINE_AA)

        # if not line_is_vertical(x1, y1, x2, y2):
        #     continue  
        # mid_point_x = abs(x2 - x1)/2
        # num_of_vertical_lines += 1
        # if should_draw_corner(x1, y1, 10, corners):
        #     cv2.circle(cdst, (x1, y1), 5, (0, 0, 255))
        # if should_draw_corner(x2, y2, 10, corners):
        #     cv2.circle(cdst, (x2, y2), 5, (0, 0, 255))
        # cv2.line(cdst, (x1, y1), (x2,y2), (0, 0, 255), 2)#, cv2.LINE_AA)
    # print(num_of_vertical_lines)
    # cv2.imshow('original', img)
    # cv2.imshow("src", cdst)
    # cv2.waitKey(1)
    # return num_of_vertical_lines, num_of_horizontal_lines

if __name__ == '__main__':
    i = 1
    # i = 53
    img = cv2.imread('images4/frame{:04d}.jpg'.format(i))
    get_med_right_left(img)
    # print(img.shape)
    # cv2.imshow('something', img)
    # cv2.waitKey(0)
    # break
    # get_med_diff(img)
    # analyze(img)
    # src = img
    # img = img[200:300, :]
    # mid_diff, left, right, forward = analyze(img)
    # print(mid_diff, left, right, forward)
    # get_forward(img)
    # print(get_med_right_left(img))
    # l_med, r_med, left, right = get_med_right_left(img)
    # print('l, r', l_med, r_med, left, right)
    # forward = get_forward(img)
    # delta = 25
    # low = np.array([125, 0, 0])
    # high = np.array([200, 255, 255])
    # med = np.array([171, 110, 78])
    # low = med - delta
    # high = med + delta
    # src = cv2.inRange(src, low, high)
    # src = cv2.medianBlur(src, 5)
    # src1 = cv2.bitwise_not(src)

    # dst = cv2.Canny(src, 50, 200) # Detect the edges
    # cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)

    # blockSize = 2
    # apertureSize = 3
    # k = 0.1
    # import pdb; pdb.set_trace()
    # corners = cv2.cornerHarris(dst, blockSize, apertureSize, k, cv2.BORDER_DEFAULT)

    # lines = cv2.HoughLinesP(dst, 1, math.pi/200, 40, np.array([]), 70, 20)
    # if lines is None:
    #     continue
    # a,b,c = lines.shape
    # num_of_vertical_lines = 0
    # for i in range(a):
    #     # import pdb; pdb.set_trace()
    #     x1, y1, x2, y2 = lines[i][0]
    #     if not line_is_vertical(x1, y1, x2, y2):
    #         continue
        
    #     mid_point_x = abs(x2 - x1)/2

    #     num_of_vertical_lines += 1



    #     if should_draw_corner(x1, y1, 10, corners):
    #         cv2.circle(cdst, (x1, y1), 5, (0, 0, 255))
    #     if should_draw_corner(x2, y2, 10, corners):
    #         cv2.circle(cdst, (x2, y2), 5, (0, 0, 255))
    #     cv2.line(cdst, (x1, y1), (x2,y2), (0, 0, 255), 2, cv2.LINE_AA)
    # print(num_of_vertical_lines)
    # cv2.imshow('original', img)
    # cv2.imshow("src", cdst)
    # cv2.waitKey(100)



# if __name__== '__main__':
#     rospy.init_node('robot', anonymous=False)
#     r = Robot()
#     # print(r.heading)
#     while not rospy.is_shutdown():
#         i = r.current_image()

#         # cv2.imshow('image', i)
#         # cv2.waitKey(1)
#         get_center_line_median(i)
#         # print(get_num_vertical_lines(i))
        # r.move(1, 0)

# for img_num in range(169):
#     img = cv2.imread('images3/left{:04d}.jpg'.format(img_num))

#     src = img
#     # delta = 25
#     # low = np.array([125, 0, 0])
#     # high = np.array([200, 255, 255])
#     # med = np.array([171, 110, 78])
#     # low = med - delta
#     # high = med + delta
#     # src = cv2.inRange(src, low, high)
#     # src = cv2.medianBlur(src, 5)
#     # src1 = cv2.bitwise_not(src)

#     dst = cv2.Canny(src, 50, 200) # Detect the edges
#     cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)

#     blockSize = 2
#     apertureSize = 3
#     k = 0.1
#     corners = cv2.cornerHarris(dst, blockSize, apertureSize, k, cv2.BORDER_DEFAULT)

#     lines = cv2.HoughLinesP(dst, 1, math.pi/200, 40, np.array([]), 70, 20)
#     if lines is None:
#         continue
#     a,b,c = lines.shape
#     num_of_vertical_lines = 0
#     for i in range(a):
#         # import pdb; pdb.set_trace()
#         x1, y1, x2, y2 = lines[i][0]
#         if not line_is_vertical(x1, y1, x2, y2):
#             continue
        
#         mid_point_x = abs(x2 - x1)/2

#         num_of_vertical_lines += 1



#         if should_draw_corner(x1, y1, 10, corners):
#             cv2.circle(cdst, (x1, y1), 5, (0, 0, 255))
#         if should_draw_corner(x2, y2, 10, corners):
#             cv2.circle(cdst, (x2, y2), 5, (0, 0, 255))
#         cv2.line(cdst, (x1, y1), (x2,y2), (0, 0, 255), 2, cv2.LINE_AA)
#     print(num_of_vertical_lines)
#     cv2.imshow('original', img)
#     cv2.imshow("src", cdst)
#     cv2.waitKey(100)
