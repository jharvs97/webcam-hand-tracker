"""
File:           hand.py
Author:         Joshua H
Date:           11/10/19
Purpose:        This module is responsible for calculating the X and Y coordinates of the largest Y point of the contour that 
                bounds the hand mask. The rationale for using the largest Y point versus using the center of the hand was the 
                issue with skin detection picking up the arm as apart of the hand (since your arm is usually the same skin 
                colour as your hand), this led to the center calculation not being accurate if the hand is  also in the frame.
Assumptions:    It is assumed that the inputted hand mask is correct, and that the hand takes up most of the region of interest.
"""
import numpy as np
import cv2
from rect import Rect
class Hand:

    def __init__(self):
       self.calibrated = False

    """
    Method:     get_hand_pos
    Purpose:    Returns the X,Y position of the top point of the contour
    Params:     self: context object
                img: input image
                dest: destination image (for drawing)
                calibrated: ensuring skin detection is calibrated
    
    Return:     Tuple     
    """
    def get_hand_pos(self, img, dest, calibrated=False):
        
        if calibrated is False:
            return

        # img_roi = img[self.roi.minX:self.roi.maxX, self.roi.minY:self.roi.maxY]

        contours, hierarchy  = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
       
        index = -1
        biggest_area = 0

        for i in range(len(contours)):
            area = cv2.contourArea(contours[i], False)
            if area > biggest_area:
                biggest_area = area
                index = i

        if index < 0:
            return np.zeros(dest.shape)
        
        
        c = max(contours[index], key = cv2.contourArea)
        top_hand = tuple(c[0][:])
        #extTop = tuple(c[c[:, :, 1].argmin()][0])

        hull_pts = cv2.convexHull(contours[index], returnPoints=True)


        M = cv2.moments(hull_pts)
        cX = int(M['m10'] / M['m00'])
        cY = int(M["m01"] / M["m00"])
        boundRect = cv2.boundingRect(hull_pts)
        cv2.circle(dest, (cX, cY), 7, (0, 0, 255), -1)
        cv2.circle(dest, top_hand, 7, (255,0,0), -1)

        cv2.drawContours(dest, [hull_pts], -1, (0,255,0))
        # cv2.rectangle(dest, (int(third_hand_w), int(boundRect[1])), \
        #   (int(third_hand_w+self.handSize), int(boundRect[1]+self.handSize)), (0,0,255), 2)
        
        
        return top_hand
        # print(len(hull_pts))
