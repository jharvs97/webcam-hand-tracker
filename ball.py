import cv2 as cv
import numpy

class Ball:

    def __init__(self, x, y, r, color):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.vel = (1,1)

    def move(self):
        self.x += self.vel[0]
        self.y += self.vel[1]
    
    def draw(self, frame):
        cv.circle(frame, (self.x, self.y), self.r, self.color, -1)