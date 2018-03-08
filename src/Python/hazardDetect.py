#! /usr/bin/env python
# coding: utf8
#
# Moves the pan and tilt module and performs calculations to
# determine the distance and rotation to the edge of a desk

import sys
import time
import math
sys.path.insert(0, "../../lib/PiconZero/Python")

# For hazard types e.g. "wall" or "edge".
# If causes error 'coz of old Python: $ sudo pip install --upgrade pip enum34
from enum import Enum

import panTilt as panTilt
import infrared as ir
import hcsr04
import edgeCalc as edgeCalc

DEBUG = True
DELAY = 0.3      # The delay between movements and stuff in seconds.
BOT_HEIGHT = 10  # Height of robot's sensor module in cm.
VIEW_RANGE = 40  # Maximum range that the robot cares about hazards to, in cm.
SENS_OFFSET = 4  # How far back from front of robot are the sensors, in cm.


class Hazard(Enum):
    """ A type of hazard that the robot may want to avoid (or no hazard) """
    edge = 1
    wall = 2
    crnr = 3  # CoRNeR wall (i.e. wall to the left AND right)
    none = 0


def getEdgeAngle():
    """
    Slowly look down while checking for edge of desk
    returns angle a
          a
         ◿
       b   c
    """
    ANGLE_OFFSET = 8  # How far off the angle measurements are in degrees
    angle = 0
    while angle < panTilt.TLT_RANGE:
        angle += 1
        panTilt.tilt(int(angle))
        deskDetected = ir.readWithDelay()
        # print "Angle:", angle + ANGLE_OFFSET, ", ir reading:", deskDetected
        if deskDetected > 200 or angle == panTilt.TLT_RANGE:
            # print "-----------------------"
            break  # Break out of looking downwards loop
    panTilt.up() # Look up again
    return 90 - angle - ANGLE_OFFSET


def getEdgeDistance():
    """
    Returns the distance to a detected edge in cm
    """
    '''

          a
         ◿
       b   c

    hypotenuse
              ◿ adjacent
          opposite

    tan(a) = opposite/adjacent
    adjacent * tan(a) = opposite
    '''

    # A multiplier to take into account the larger ir dot
    # observed when further away from as surface (think torch
    # beam onto a wall getting larger as it gets further away).
    # TODO: Figure out a better way to do this.
    PWR = 1.1

    edgeDistance = BOT_HEIGHT * math.tan(math.radians(getEdgeAngle()))
    if edgeDistance > 2:
        #print "edgeDistance of", edgeDistance
        edgeDistance **= PWR
        #print "multiplied to", edgeDistance
    # print "Distance to edge: ", edgeDistance

    return edgeDistance


def getWallDistance():
    """ Use ultrasonic sensor to get a distance to a wall and return it if it's <30cm """

    # 30cm is used because any further than that might be erroneous,
    # and is unlikely to affect the robot's movement anyway.

    distance = int(hcsr04.getDistance() - SENS_OFFSET)

    print "ultrasonic distance:", distance

    if distance <= 30:
        return max(0, distance)  # If < 0 return 0
    else:
        return None


def getDistance(angle):
    """ Look (angle), wait for servos to respond, then get & return wall or edge distance """

    panTilt.pan(angle)
    time.sleep(DELAY)
    wallDistance = getWallDistance()
    edgeDistance = getEdgeDistance() if wallDistance is None else None

    return wallDistance, edgeDistance


def getDistances():
    """ Look around, return left, forward, right distances to stuff """

    # If there's a wall in the way then there's no edge that way (probably)

    wallL, edgeL = getDistance(-45)  # Left
    wallF, edgeF = getDistance(  0)  # Forward
    wallR, edgeR = getDistance( 45)  # Right

    panTilt.pan()  # Recenter

    return wallL, edgeL, wallF, edgeF, wallR, edgeR


def getHazardDistanceRotation():

    hzrdType = Hazard.none
    distance = None
    rotation = 0

    # Move the sensor module or "robot head" around and measure distances:
    wl, el, wf, ef, wr, er = getDistances()

    # WALL DETECTION if wall detected in any direction
    if wl is not None or wf is not None or wr is not None:
        hzrdType = Hazard.wall
        # Distance and rotation to wall (ish). Order is important.
        if wl is not None and wr is not None:  # If wall on left and right
            hzrdType = Hazard.crnr
            distance = min(wl, wr)  # Use the closer wall as hazard distance
            rotation = 0
        elif wf is not None:
            distance, rotation = wf, 0
        elif wl is not None:
            distance, rotation = wl, -45
        elif wr is not None:
            distance, rotation = wr, 45

    # EDGE DETECTION if edge is deteced looking front, and left and/or right
    if ef is not None and (el is not None or er is not None):
        edgeDistance, edgeRotation = edgeCalc.getDistanceAndRotationToEdge(el, ef, er)
        if hzrdType is Hazard.none or edgeDistance < distance:
            hzrdType = Hazard.edge
            distance = edgeDistance
            rotation = edgeRotation

    # If the closest hazard is too far away, pretend it does't exist.
    if (distance is None) or (not 0 <= distance <= VIEW_RANGE):
        hzrdType = Hazard.none
        distance = 0
        rotation = 0

    return hzrdType, distance, rotation
