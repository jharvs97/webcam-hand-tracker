"""
File:       game.py
Author:     Joshua H
Date:       11/10/19
Purpose:    This file contains the main game loop for the Toy Pong Example 
            to test my implementation of the handtracking algorithm/s.
"""

from ball import Ball
from paddle import Paddle
from config import *
from HandDetect import HandDetect
from utils import remap

import cv2 as cv
import numpy as np
import time
import sys
import time

# Keep track of the score
# 0th index is the left paddle
# 1st index is the right paddle
score = [0,0]

# Initialise video capture
cap = cv.VideoCapture(0) 
cap.set(cv.CAP_PROP_FRAME_WIDTH, SCREEN_WIDTH)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, SCREEN_HEIGHT)

# Initialise variables for game objects / hand detection objects
ai_paddle = None
human_paddle = None
handDetect = None

# If there is only one command line arg
# print the invalid usage and exit
if len(sys.argv) is 1:
    print("Invalid usage, please provide one command line argument stating your handedness")
    print("E.g: python3 game.py [--l | --left | --r | --right]\n")
    sys.exit(1)
# Ensure only two command line args
elif len(sys.argv) == 2:
    # If the user is right handed, initialise game for right-handedness
    if sys.argv[1] == '--right' or sys.argv[1] == '--r':
        handDetect = HandDetect(0)
        ai_paddle = Paddle(0,  0,PADDLE_WIDTH,PADDLE_HEIGHT,PADDLE_COLOR, True)
        human_paddle = Paddle(640 - PADDLE_WIDTH,0,PADDLE_WIDTH,PADDLE_HEIGHT,PADDLE_COLOR)
    # Else if the user is left handed, initialise game for left-handedness
    elif sys.argv[1] == '--left' or sys.argv[1] == '--l':
        handDetect = HandDetect(1)
        ai_paddle = Paddle(640 - PADDLE_WIDTH,0,PADDLE_WIDTH,PADDLE_HEIGHT,PADDLE_COLOR, True)
        human_paddle = Paddle(0,  0,PADDLE_WIDTH,PADDLE_HEIGHT,PADDLE_COLOR)
# If more than two command line args, display same usage error message and exit
else:
    print("Invalid usage, please provide one command line argument stating your handedness")
    print("E.g: python3 game.py [--l | --left | --r | --right]\n")
    sys.exit(1)

# Create the ball game object 
ball = Ball(SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2, BALL_RADIUS, BALL_COLOR)

# Dont run the game loop unit specified by the user
game_start = False

# Main game loop
while(1):

    # Read frame from the capture
    ret, frame = cap.read()
    # Flip the frame as to be displayed correctly
    frame = cv.flip(frame, 1)
    # Create a pure copy of the input for detection/calibration
    calibrate_frame = frame.copy()

    # Call my hand detection API to get the hand position
    # start = time.time()
    hand_pos = handDetect.hand_center_XY(calibrate_frame)
    # end = time.time()
    # print("Time elapsed for hand detection = %f" % (end - start))

    # If the user has started the game
    if game_start:

        # Check ball collision on each paddle
        if ai_paddle.ball_collision(ball):
            ball.vel[0] *= -1
        
        if human_paddle.ball_collision(ball):
            ball.vel[0] *= -1

        # If the ball exceeds the left of the screen
        # Increment right paddle score and reset the ball
        if ball.x < 0:
            score[1] += 1
            ball.reset(SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2)
            pass
        
        # If the ball exceeds the right of the screen
        # Increment left paddle score and reset the ball
        if ball.x > SCREEN_HEIGHT:
            score[0] += 1
            ball.reset(SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2)
            pass
        
        # If the hand detection is calibrated
        if handDetect.calibrated is True:
            # use a try-block incase there are no bounding-boxes in the frame
            try:
                if hand_pos[1]:
                    if hand_pos[1] >= 0 and hand_pos[1] <= SCREEN_WIDTH:
                        #print("Center Y: %d" % hand_pos[1])
                        human_paddle.set_ypos(hand_pos[1])
            except:
                print("Error, no hand in the frame!")

        # Update each game object
        ai_paddle.update(ball)
        human_paddle.update(ball)
        ball.move()

    # Draw each game object
    ai_paddle.draw(frame)
    human_paddle.draw(frame)
    ball.draw(frame)

    # Show the pong game
    cv.imshow('Pong', frame)

    key = cv.waitKey(1) & 0xff

    if key == ord('q'):
        break
    # Calibrate the skin detection module
    elif key == ord('s'):
        handDetect.calibrateSkinDetection(calibrate_frame)
    # Start the game 
    elif key == ord('p'):
        if handDetect.calibrated:
            game_start = True
    elif key == ord('o'):
    # Allow UP movement with keys
        human_paddle.movement[1] = -16
    elif key == ord('l'):
    # Allow DOWN movement with keys
        human_paddle.movement[1] = 16
    # Reset the game
    elif key == ord('r'):
        ball.reset(SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2)
        game_start = False
        ai_paddle_score = 0
        human_paddle_score = 0
    else:
        human_paddle.movement[1] = 0


# Free memory and destroy windows if the main game loop has been exited
cap.release()
cv.destroyAllWindows()