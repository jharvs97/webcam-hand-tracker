import cv2 as cv
import numpy
import random as rand
from config import *

class Ball:

    def __init__(self, x, y, r, color):
        self.x = x
        self.y = y
        self.r = r
        self.color = color

        rand_x = 0

        if rand.random() > 0.5:
            rand_x = 1
        else:
            rand_x = -1

        self.vel = [rand_x,rand.random()]

    def move(self):

        if (self.y + self.r) + self.vel[1] < 0 or (self.y + self.r) + self.vel[1] > SCREEN_WIDTH:
            self.vel[1] *= -1

        self.x += self.vel[0] * 10
        self.y += self.vel[1] * 10

        
    def draw(self, frame):
        cv.circle(frame, (int(self.x), int(self.y)), int(self.r), self.color, -1)

    def reset(self,x,y):
        self.x = x
        self.y = y

        rand_x = 0

        if rand.random() > 0.5:
            rand_x = 1
        else:
            rand_x = -1
        self.vel = [rand_x,rand.random()]

