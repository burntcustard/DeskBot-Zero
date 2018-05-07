#! /usr/bin/env python
# coding: utf8
#
# Functions for moving the robot forwards, backwards, turning
# in a specific direction, or turning randomly left or right.


import sys
import time
import random
sys.path.insert(0, "../../lib/PiconZero/Python")

import piconzero as pz


DEBUG = True
SPEED = 40
TURN_DURATION = 0.5


def init():
    """Initialize the motors."""
    # pz.init()
    print "Initialized motors"


def turn(speed = SPEED, direction = 0, duration = TURN_DURATION):
    """ Turn the robot at x speed in y direction for z duration in seconds """

    debugStr = "Turning"

    # If no direction specified, pick left (-1) or right (1) randomly:
    if direction == 0:
        debugStr += " (randomly)"
        direction = random.choice([-1, 1])

    debugDirectionStr = "right" if direction == 1 else "left"

    if DEBUG is True:
        print debugStr, debugDirectionStr, "for", str(duration) + "s"

    pz.setMotor(0,  speed * direction)
    pz.setMotor(1, -speed * direction)
    time.sleep(duration)
    pz.stop()


def move(speed = SPEED, direction = 1, duration = TURN_DURATION):
    """ Move the robot at x speed in y direction for z duration in seconds """

    if DEBUG is True:
        directionStr = "forward" if direction == 1 else "backwards"
        print "Moving", directionStr, "for", str(duration) + "s"

    pz.setMotor(0, speed * direction)
    pz.setMotor(1, speed * direction)
    time.sleep(duration)
    pz.stop()


def turnAwayFrom(speed = SPEED, rotation = 0):
    """ Turn robot away from a hazard """
    if rotation   >  20:  # If hazard is >20° to the right:
        turn(speed,  -1)  #  - turn right.
    elif rotation < -20:  # If hazard is >20° to the left:
        turn(speed,   1)  #  - turn left.
    else:                # If hazard is in front (ish):
        turn(speed)      #  - turn randomly either left or right.


def cleanup():
    """ Set both motors to 0 """
    pz.cleanup()
