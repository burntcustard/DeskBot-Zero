#! /usr/bin/env python
# coding: utf8
#
# Training data collection program to take training images without
# the robot falling off the edge of the desk or running into things

import sys
import time
import math
import random
sys.path.insert(0, "../../lib/PiconZero/Python")

import piconzero as pz
import panTilt as panTilt
import infrared as ir
import movement as robot
import edgeCalc as edge

pz.init()
panTilt.init()
ir.init()
robot.init()

moveSpeed   = 35 # Movement speed 0-100
delay       = 0.1 # The delay between movements and stuff in seconds

try:
    while True:

        time.sleep(delay)

        # Look around
        distanceToEdge, rotationToEdge = edge.getDistanceAndRotation()

        # If the robot is close-ish to the desk edge:
        if 4 <= distanceToEdge <= 8:
            robot.turnAwayFromEdge(moveSpeed, rotationToEdge)
            robot.move(moveSpeed)

        # If the robot is TOO CLOSE to the desk edge:
        elif distanceToEdge < 4:
            print "Dangerously close to desk edge!"
            robot.move(moveSpeed, -1)  # Back up a bit
            robot.turnAwayFromEdge(moveSpeed, rotationToEdge)

        # If the robot is far from the desk edge:
        else:
            robot.move(moveSpeed)


except KeyboardInterrupt:
    print


finally:
    panTilt.cleanup()
    time.sleep(0.5)
    pz.cleanup() # This might actually clean up everything else too?
    time.sleep(0.5)
