import cv2 as cv
import numpy as np
from rect import Rect
from skin_detect import DetectSkin
from hand import Hand

title_window = "Mask"
trackbar_name1 = "Offset low"
trackbar_name2 = "Offset high"

def nothing(x):
    pass


class HandDetect:

    def __init__(self, side=0):
        self.detectSkin = DetectSkin()
        self.findHand = Hand()
        self.side = side
        self.calibrated = False

    def hand_center_XY(self, frame):


        height = frame.shape[0]
        width = frame.shape[1]

        frame_copy = frame.copy()
        
        if self.side is 0:
            frame_roi = frame_copy[0:int(height), int(width/2):int(width)]
        else:
            frame_roi = frame_copy[0:int(height), int(0):int(width/2)]
        
        
        self.detectSkin.display_sampler(frame_roi)
        mask = self.detectSkin.get_mask(frame_roi)
        hand_center = self.findHand.get_hand_pos(mask, frame_roi, self.detectSkin.calibrated)

        cv.namedWindow(title_window)
        cv.createTrackbar(trackbar_name1, title_window, 0, 80, nothing)
        cv.createTrackbar(trackbar_name2, title_window, 0, 80, nothing)

        self.detectSkin.offset_low = cv.getTrackbarPos(trackbar_name1, title_window)
        self.detectSkin.offset_high = cv.getTrackbarPos(trackbar_name2, title_window)

        #cv.imshow('frame', frame)
        cv.imshow('roi', frame_roi)
        cv.imshow(title_window, mask)
        #cv.imshow(title_window, )

        #print(hand_center)

        return hand_center

    def calibrateSkinDetection(self, frame):
        self.detectSkin.calibrate(frame)
        self.calibrated = True

        
    