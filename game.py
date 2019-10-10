from ball import Ball
from paddle import Paddle
from config import *
from HandDetect import HandDetect

import cv2 as cv
import numpy as np
import time


cap = cv.VideoCapture(0) 
cap.set(cv.CAP_PROP_FRAME_WIDTH, SCREEN_WIDTH)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, SCREEN_HEIGHT)

handDetect = HandDetect()

player1 = Paddle(0,  0,PADDLE_WIDTH,PADDLE_HEIGHT,PADDLE_COLOR, True)
player2 = Paddle(640 - PADDLE_WIDTH,0,PADDLE_WIDTH,PADDLE_HEIGHT,PADDLE_COLOR)
ball    = Ball(SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2, BALL_RADIUS, BALL_COLOR)

ret, begin_frame = cap.read()

game_board = np.zeros(begin_frame.shape)

while(1):

    ret, frame = cap.read()
    frame = cv.flip(frame, 1)
    calibrate_frame = frame.copy()

    center = handDetect.hand_center_XY(frame)

    player1.update()
    player2.update()

    player1.draw(game_board)
    player2.draw(game_board)
    ball.draw(game_board)

    cv.imshow('Pong', game_board)

    key = cv.waitKey(1) & 0xff

    if key == ord('q'):
        break
    elif key == ord('s'):
        handDetect.calibrateSkinDetection(calibrate_frame)
    elif key == ord('o'):
        player2.movement[1] = -8
    elif key == ord('l'):
        player2.movement[1] = 8
    else:
        player2.movement[1] = 0

    # clear the screen
    game_board = np.zeros(begin_frame.shape)

cap.release()
cv.destroyAllWindows()