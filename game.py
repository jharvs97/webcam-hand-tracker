from ball import Ball
from paddle import Paddle
from config import *
from HandDetect import HandDetect
from utils import remap

import cv2 as cv
import numpy as np
import time
import sys

ai_paddle_score = 0
human_paddle_score = 0

cap = cv.VideoCapture(0) 
cap.set(cv.CAP_PROP_FRAME_WIDTH, SCREEN_WIDTH)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, SCREEN_HEIGHT)

right_or_left = -1

ai_paddle = None
human_paddle = None


if len(sys.argv) is 1:
    print("Invalid usage, please provide one command line argument stating your handedness")
    print("E.g: python3 game.py [--l | --left | --r | --right]\n")
    sys.exit(1)
elif sys.argv[1] == '--right' or sys.argv[1] == '--r':
    right_or_left = 0
    ai_paddle = Paddle(0,  0,PADDLE_WIDTH,PADDLE_HEIGHT,PADDLE_COLOR, True)
    human_paddle = Paddle(640 - PADDLE_WIDTH,0,PADDLE_WIDTH,PADDLE_HEIGHT,PADDLE_COLOR)
elif sys.argv[1] == '--left' or sys.argv[1] == '--l':
    right_or_left = 1
    ai_paddle = Paddle(640 - PADDLE_WIDTH,0,PADDLE_WIDTH,PADDLE_HEIGHT,PADDLE_COLOR, True)
    human_paddle = Paddle(0,  0,PADDLE_WIDTH,PADDLE_HEIGHT,PADDLE_COLOR)
else:
    print("Invalid usage, please provide one command line argument stating your handedness")
    print("E.g: python3 game.py [--l | --left | --r | --right]\n")
    sys.exit(1)

ball = Ball(SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2, BALL_RADIUS, BALL_COLOR)
handDetect = HandDetect(right_or_left)

game_start = False

while(1):

    ret, frame = cap.read()
    frame = cv.flip(frame, 1)
    calibrate_frame = frame.copy()

    center = handDetect.hand_center_XY(calibrate_frame)

    if game_start:

        if ai_paddle.ball_collision(ball):
            ball.vel[0] *= -1
        
        if human_paddle.ball_collision(ball):
            ball.vel[0] *= -1

        if ball.x < 0:
            human_paddle_score += 1
            ball.reset(SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2)
            pass
        
        if ball.x > SCREEN_HEIGHT:
            ai_paddle_score += 1
            ball.reset(SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2)
            pass
        
        if handDetect.calibrated is True:
            if len(center) is 1:
                if center[1] >= 0 and center[1] <= SCREEN_HEIGHT:
                    print("Center Y: %d" % center[1]    )
                    human_paddle.set_ypos(center[1])

        ai_paddle.update(ball)
        human_paddle.update(ball)
        ball.move()

        if handDetect.calibrated is True:
            if center is not None:
                if center[1] >= 0 and center[1] <= SCREEN_HEIGHT:
                    human_paddle.set_ypos(center[1])

    ai_paddle.draw(frame)
    human_paddle.draw(frame)
    ball.draw(frame)

    cv.imshow('Pong', frame)

    key = cv.waitKey(1) & 0xff

    if key == ord('q'):
        break
    elif key == ord('s'):
        handDetect.calibrateSkinDetection(calibrate_frame)
    elif key == ord('p'):
        game_start = True
    elif key == ord('o'):
        human_paddle.movement[1] = -16
    elif key == ord('l'):
        human_paddle.movement[1] = 16
    elif key == ord('r'):
        ball.reset(SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2)
        game_start = False
        ai_paddle_score = 0
        human_paddle_score = 0
    else:
        human_paddle.movement[1] = 0

    # clear the screen
    #frame = np.zeros((SCREEN_WIDTH, SCREEN_HEIGHT, 3))

cap.release()
cv.destroyAllWindows()