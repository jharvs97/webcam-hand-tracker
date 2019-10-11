"""
File:       ball.py
Author:     Joshua H
Date:       11/10/19
Purpose:    Encapsulate data/methods for a ball in the Pong game
"""
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

        # 50/50 Chance that the ball goes left or right
        if rand.random() > 0.5:
            rand_x = 1
        else:
            rand_x = -1

        self.vel = [rand_x,rand.random()]

    """
    Method:     move
    Purpose:    Update the position of the ball with respect to its current velocity
    Params      self: context object
    Return:     N/A
    """
    def move(self):

        if (self.y + self.r) + self.vel[1] < 0 or (self.y + self.r) + self.vel[1] > SCREEN_WIDTH:
            self.vel[1] *= -1

        self.x += self.vel[0] * 15
        self.y += self.vel[1] * 10

    """
    Method:     draw
    Purpose:    Draw the ball onto the output frane
    Params:     self: context object
                frame: destination frame
    Return:     N/A
    """    
    def draw(self, frame):
        cv.circle(frame, (int(self.x), int(self.y)), int(self.r), self.color, -1)

    """
    Method:     reset
    Purpose:    Reset the ball to the center of the screen, and re-initialise its velocity
    Params:     self: context object
                x: Center X of the screen
                y: Cetner Y of the screen
    Return:     N/A
    """
    def reset(self,x,y):
        self.x = x
        self.y = y

        rand_x = 0

        if rand.random() > 0.5:
            rand_x = 1
        else:
            rand_x = -1
        self.vel = [rand_x,rand.random()]

