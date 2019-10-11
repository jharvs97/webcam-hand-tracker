"""
File:       paddle.py
Author:     Joshua H
Date:       11/10/09
Purpose:    Encapsulates the data/methods for the paddle of the Pong game
"""
import math
import cv2 as cv
from config import *
import random as rand

class Paddle:

    def __init__(self, x, y, w, h, color, ai=False):

        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.movement = [0,0]
        self.color = color
        self.ai = ai
        

    """
    Method:     update
    Purpose:    Update the position of the paddle
    Params:     self: Context object
                ball: The ball of the pong game, used for AI

    Return:     N/A
    """
    def update(self, ball):

        if self.ai:
            if rand.random() > 0.7:
                if self.y + self.h // 2 > ball.y:
                    self.movement[1] = -8
                else:
                    self.movement[1] = 8

            if (self.y + self.movement[1]) < 0 or ((self.y + self.h) + self.movement[1]) > SCREEN_WIDTH:
                return

            self.x += self.movement[0]
            self.y += self.movement[1]


    """
    Method:     set_ypos
    Purpose:    Set the y position of the paddle given a center position
    Params:     self: Context object
                new_y: The new Y pos

    Return:     N/A
    """
    def set_ypos(self, new_y):
        self.y = new_y

    """
    Method:     ball_collision
    Purpose:    Test if the ball is colliding with this paddle
    Params:     self: Context object
                ball: Ball object
    
    Return:     Boolean
    """
    def ball_collision(self, ball):
        x = max(self.x, min(ball.x, self.x+self.w))
        y = max(self.y, min(ball.y, self.y+self.h))

        dist = math.sqrt((x - ball.x) * (x - ball.x) + \
        (y - ball.y) * (y - ball.y))

        return dist < ball.r


    """
    Method:     draw
    Purpose:    Draw the paddle to the frame 
    Params:     self: Context object
                frame: destination of the rendered paddle
    
    Return:     N/A
    """
    def draw(self, frame):
        cv.rectangle(frame, (int(self.x), int(self.y)), (int(self.x + self.w), int(self.y + self.h)), self.color, -1)