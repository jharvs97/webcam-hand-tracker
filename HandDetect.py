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
        self.backSub = cv.createBackgroundSubtractorMOG2()

    def hand_center_XY(self, frame):

        height = frame.shape[0]
        width = frame.shape[1]

        frame_copy = frame.copy()
        
        if self.side is 0:
            frame_roi = frame_copy[0:int(height), int(width/2):int(width)]
        else:
            frame_roi = frame_copy[0:int(height), int(0):int(width/2)]
        
        
        fg_mask = self.backSub.apply(frame_roi)
        fg = cv.bitwise_and(frame_roi, frame_roi, mask=fg_mask)
        


        self.detectSkin.display_sampler(frame)
        mask = self.detectSkin.get_mask(fg)
        hand_center = self.findHand.get_hand_pos(mask, fg, self.detectSkin.calibrated)

        cv.imshow('frame', frame)
        cv.imshow('roi', frame_roi)
        cv.imshow('mask', mask)
        cv.imshow('fg', fg)

        #cv.imshow('fg', fg)

        return hand_center

    def calibrateSkinDetection(self, frame):
        self.detectSkin.calibrate(frame)

        
        
    