"""
File:           skin_detect.py
Author:         Joshua H
Date:           11/10/19
Purpose:        This module is responsible for taking a region of interest and binarizing based on the threshold values of 
                the players skin. Before the skin mask can be calculated, the thresholds need to be calibrated by 
                taking samples of the users skin.

Assumptions:    It is assumed that the camera is stationary, there is uniform lighting within the room where the player 
                is within, and that the background is static (no frequent moving objects).
"""
import cv2
import numpy as np
from rect import Rect

class DetectSkin:

    def __init__(self):
        self.calibrated = False  
        self.offset_low = 30
        self.offset_high = 30  
    
    """
    Method:     calc_thresh
    Purpose:    calculate the HSV skin thresholds based on the samples provided from the user
    Params:     sample1: the first sample
                sample2: the second sample
    Return      N/A
    """
    def calc_thresh(self, sample1, sample2):

        mean_sample1 = cv2.mean(sample1)
        mean_sample2 = cv2.mean(sample2)

        h_low_thresh    = min(mean_sample1[0], mean_sample2[0]) - self.offset_low
        h_high_thresh   = max(mean_sample1[0], mean_sample2[0]) + self.offset_high

        s_low_thresh    = min(mean_sample1[1], mean_sample2[1]) - self.offset_low
        s_high_thresh   = max(mean_sample1[1], mean_sample2[1]) + self.offset_high
        
        #v_low_thresh    = min(mean_sample1[2], mean_sample2[2]) - offset_low
        #v_high_thresh   = max(mean_sample1[2], mean_sample2[2]) + offset_high

        self.low_thresh = np.array([h_low_thresh,s_low_thresh,0])
        self.high_thresh = np.array([h_high_thresh, s_high_thresh, 255])

    """
    Method:     display_sample
    Purpose:    display the sample regions to the ROI frame
    Params:     frame: the destination frame
    Return:     N/A
    """
    def display_sampler(self, frame):
        #print(frame.shape)
        frame_h = frame.shape[0]
        frame_w = frame.shape[1]
        rect_size = 10

        self.rect1 = Rect(frame_w/2, frame_h/2, rect_size, rect_size)
        self.rect2 = Rect(frame_w/2, frame_h/3, rect_size, rect_size)
        
        cv2.rectangle(frame, self.rect1.minXY, self.rect1.maxXY, (0,255,0), 2 )
        cv2.rectangle(frame, self.rect2.minXY, self.rect2.maxXY, (255,0,0), 2 )


    """
    Method:     calibrate
    Purpose:    Take the samples from the ROI and calculate the skin thresholds 
    Params:     frame: ROI
    Return:     N/A
    """
    def calibrate(self, frame):
        #hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        sample1 = hsv_frame[self.rect1.minY:self.rect1.maxY, self.rect1.minX:self.rect1.maxX]
        sample2 = hsv_frame[self.rect2.minY:self.rect2.maxY, self.rect2.minX:self.rect2.maxX]

        self.calc_thresh(sample1, sample2)

        self.calibrated = True

    """
    Method:     get_mask
    Purpose:    Return the binarized mask based on the skin thresholds
    Params:     frame: ROI
    Return:     mask: np.ndarray
    """
    def get_mask(self, frame):
        
        if self.calibrated is False:
            return np.zeros(frame.shape)

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv_frame, self.low_thresh, self.high_thresh)

        structElem = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
        #cv2.morphologyEx(mask, cv2.MORPH_OPEN, structElem )
        #cv2.morphologyEx(mask, cv2.MORPH_CLOSE, structElem )
        mask = cv2.erode(mask, structElem, iterations = 2)
        mask = cv2.dilate(mask, structElem, iterations = 2)
        mask = cv2.dilate(mask, structElem, iterations = 2)
        mask = cv2.erode(mask, structElem, iterations = 2)

        mask = cv2.GaussianBlur(mask, (3,3), 0)

        return mask

