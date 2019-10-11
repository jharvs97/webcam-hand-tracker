"""
File:           HandDetect.py
Author:         Joshua H   
Date:           11/10/19
Purpose:        The high-level API which encapsulates the methods/data/objects required to determine the position
                of a players hand.
"""
import cv2 as cv
import numpy as np
from rect import Rect
from skin_detect import DetectSkin
from hand import Hand

class HandDetect:

    def __init__(self, side=0):
        self.detectSkin = DetectSkin()
        self.findHand = Hand()
        self.side = side
        self.calibrated = False

    """
    Method:     hand_center_XY
    Purpose:    Main method to return the hand position tuple, calls subroutines to determine the position of the hand
    Params:     frame: Webcam frame
    Return:     Tuple: X,Y position of the hand
    """
    def hand_center_XY(self, frame):

        height = frame.shape[0]
        width = frame.shape[1]
        
        # Create deep copy of frame to ensure no modification to inputted frame
        # As python passes by reference
        frame_copy = frame.copy()
        
        # Set the ROI to the side of the handedness of the player
        if self.side is 0:
            frame_roi = frame_copy[0:int(height), int(width/2):int(width)]
        else:
            frame_roi = frame_copy[0:int(height), int(0):int(width/2)]
        
        # Create deep copy of ROI as the sample displayer modifies the original ROI
        # Ensuring the sampler doesnt take the pixels which have been coloured 
        # to display the sample areas
        roi_copy = frame_roi.copy()
        
        self.detectSkin.display_sampler(roi_copy)
        mask = self.detectSkin.get_mask(frame_roi)
        hand_center = self.findHand.get_hand_pos(mask, frame_roi, self.detectSkin.calibrated)

        cv.imshow('ROI Sampler', roi_copy)
        cv.imshow('Hand position', frame_roi)
        cv.imshow('Mask', mask)

        return hand_center

    """
    Method:
    """
    def calibrateSkinDetection(self, frame):
        self.detectSkin.calibrate(frame)
        self.calibrated = True

        
    