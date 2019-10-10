import cv2
import numpy as np
from rect import Rect

class DetectSkin:

    def __init__(self):
        self.calibrated = False  
        self.offset_low = 30
        self.offset_high = 30  
    
    def calc_thresh(self, sample1, sample2):
        self.offset_low = 60
        self.offset_high = 60

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

    def display_sampler(self, frame):
        #print(frame.shape)
        frame_h = frame.shape[0]
        frame_w = frame.shape[1]
        rect_size = 5

        self.rect1 = Rect(frame_w/2, frame_h/2, rect_size, rect_size)
        self.rect2 = Rect(frame_w/2, frame_h/3, rect_size, rect_size)
        
        cv2.rectangle(frame, self.rect1.minXY, self.rect1.maxXY, (0,255,0), 2 )
        cv2.rectangle(frame, self.rect2.minXY, self.rect2.maxXY, (255,0,0), 2 )


    def calibrate(self, frame):
        #hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        sample1 = hsv_frame[self.rect1.minY:self.rect1.maxY, self.rect1.minX:self.rect1.maxX]
        sample2 = hsv_frame[self.rect2.minY:self.rect2.maxY, self.rect2.minX:self.rect2.maxX]

        self.calc_thresh(sample1, sample2)

        self.calibrated = True

    def get_mask(self, frame):
        
        if self.calibrated is False:
            return np.zeros(frame.shape)

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv_frame, self.low_thresh, self.high_thresh)

        structElem = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))

        mask = cv2.erode(mask, structElem, iterations = 3)
        mask = cv2.dilate(mask, structElem, iterations = 3)

        # mask = cv2.dilate(mask, structElem, iterations = 3)
        # mask = cv2.erode(mask, structElem, iterations = 3)

        mask = cv2.GaussianBlur(mask, (3,3), 0)

        return mask

