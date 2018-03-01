#! /usr/bin/env python
# coding: utf8
#
# Simplifies moving the robot forwards, backwards, turning
# in a set direction, or turning randomly left or right


import sys
import time
import random
sys.path.insert(0, "../../lib/PiconZero/Python")

import piconzero as pz


DEBUG = False


def init():
    """Initialize the motors."""
    # pz.init()
    print "Initialized motors"


def turn(speed = 40, direction = 0, duration = 0.5):
    """ Turn the robot at x speed in y direction for z duration in seconds """

    # If no direction specified, pick left (-1) or right (1) randomly:
    if not direction:
        direction = random.choice([-1, 1])

    print direction

    if DEBUG is True:
        directionStr = "right" if direction == 1 else "left"
        print "Turning", directionStr, "for", duration, "seconds"

    pz.setMotor(0,  speed * direction)
    pz.setMotor(1, -speed * direction)
    time.sleep(duration)
    pz.stop()


def move(speed = 40, direction = 1, duration = 0.5):
    """ Move the robot at x speed in y direction for z duration in seconds """

    if DEBUG is True:
        directionStr = "forward" if direction == 1 else "backwards"
        print "Moving", directionStr, "for", duration, "seconds"

    pz.setMotor(0, speed * direction)
    pz.setMotor(1, speed * direction)
    time.sleep(duration)
    pz.stop()


def turnAwayFrom(speed = 40, rotation = 0):
    """ Turn robot away from a hazard """

    if rotation   < -15: # If hazard is to the left:
        turn(speed,  1)  # Turn right
    elif rotation > 15:  # If hazard is to the right:
        turn(speed, -1)  # Turn left
    else:                # If hazard is in front (ish):
        print "Trying to turn randomly, picked..."
        turn(speed)      # Turn randomly either left or right


def cleanup():
    """ Set both motors to 0 """
    pz.cleanup()
