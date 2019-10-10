import math
import cv2 as cv

class Paddle:

    def __init__(self, x, y, w, h, color, ai=False):

        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.movement = [0,0]
        self.color = color


    def update(self):
        self.x += self.movement[0]
        self.y += self.movement[1]

    def draw(self, frame):
        cv.rectangle(frame, (int(self.x), int(self.y)), (int(self.x + self.w), int(self.y + self.h)), self.color, -1)