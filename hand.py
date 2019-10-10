import numpy as np
import cv2
from rect import Rect
class Hand:

    def __init__(self):
       # self.roi = Rect(x,y,w,h)
       self.calibrated = False
       self.handSize = 60

    def display_hand_area(self, frame):
        
        cv2.rectangle(frame, self.roi.minXY, self.roi.maxXY, (0,255,0), 2)

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
        
        
        # c = max(contours[index], key = cv2.contourArea)
        # print(c)
        #extTop = tuple(c[c[:, :, 1].argmin()][0])

        hull_pts = cv2.convexHull(contours[index], returnPoints=True)


        M = cv2.moments(hull_pts)
        cX = int(M['m10'] / M['m00'])
        cY = int(M["m01"] / M["m00"])
        boundRect = cv2.boundingRect(hull_pts)
        cv2.circle(dest, (cX, cY), 7, (0, 0, 255), -1)

        cv2.drawContours(dest, [hull_pts], -1, (0,255,0))
        # cv2.rectangle(dest, (int(third_hand_w), int(boundRect[1])), \
        #   (int(third_hand_w+self.handSize), int(boundRect[1]+self.handSize)), (0,0,255), 2)
        
        
        return (cX, cY)
        # print(len(hull_pts))
