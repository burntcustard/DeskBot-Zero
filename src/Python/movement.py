#! /usr/bin/env python
# coding: utf8
#
# Basic test of HC-SR04 ultrasonic sensor on Picon Zero

import sys
import time
import random
sys.path.insert(0, "../../lib/PiconZero/Python")

import piconzero as pz

DEBUG = True


def init():
    """Initialize the motors."""
    # pz.init()
    print "Initialized motors"


def turn(speed = 40, direction = random.choice([-1, 1]), duration = 0.5):
    """ Turn the robot at x speed in y direction for z duration in seconds """

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


def turnAwayFromEdge(speed = 40, rotation = 0):
    """ Turn robot away from the desk edge """

    if rotation   < -30: # If desk edge is to the left:
        turn(speed,  1)  # Turn right
    elif rotation > 30:  # If desk edge is to the right:
        turn(speed, -1)  # Turn left
    else:                # If desk edge is in front (ish):
        turn(speed)      # Turn randomly either left or right


def cleanup():
    """ Set both motors to 0 """
    pz.cleanup()
