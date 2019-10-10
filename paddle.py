import math
import cv2 as cv
from config import *

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
    Used for AI or Keyboard movement
    """
    def update(self, ball):

        if self.ai:
            if ball.y > (self.y + self.h // 2):
                self.movement[1] = 16
            
            if ball.y < (self.y + self.h // 2):
                self.movement[1] = -16

        if self.y + self.movement[1] < 0 or (self.y + self.h) + self.movement[1] > SCREEN_WIDTH:
            return

        self.x += self.movement[0]
        self.y += self.movement[1]


    """
    Used for Hand controller 
    """
    def set_ypos(self, center):

        if (center - (self.h // 2)) < 0 or (center + (self.h // 2)) > SCREEN_WIDTH:
            return
        

        self.y = center + (self.h // 2)

    def ball_collision(self, ball):
        x = max(self.x, min(ball.x, self.x+self.w))
        y = max(self.y, min(ball.y, self.y+self.h))

        dist = math.sqrt((x - ball.x) * (x - ball.x) + \
        (y - ball.y) * (y - ball.y))

        return dist < ball.r

    def draw(self, frame):
        cv.rectangle(frame, (int(self.x), int(self.y)), (int(self.x + self.w), int(self.y + self.h)), self.color, -1)