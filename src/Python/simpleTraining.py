#! /usr/bin/env python
# coding: utf8
#
# Basic test of HC-SR04 ultrasonic sensor on Picon Zero

import sys
import time
import math
sys.path.insert(0, "../../lib/PiconZero/Python")

import piconzero as pz
import panTilt as panTilt
import infrared as ir

pz.init()
panTilt.init()
ir.init()

moveSpeed   = 20 # Movement speed 0-100
delay       = 0.1 # The delay between movements and stuff in seconds
lookSpeed   = 0.2 # How much delay there is between moving panTilt
robotHeight = 10 # Height of robot's sensors in cm


def getEdgeAngle():
    """
    Slowly look down while checking for edge of desk
    returns angle a
          a
         ⊿
       b   c
    """
    ANGLE_OFFSET = 8  # How far off the angle measurements are in degrees
    angle = 0
    while angle < panTilt.get("tilt_range"):
        angle += 1
        panTilt.tilt(int(angle))
        deskDetected = ir.readWithDelay()
        # print "Angle:", angle + ANGLE_OFFSET, ", ir reading:", deskDetected
        if deskDetected > 200 or angle == panTilt.get("tilt_range"):
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
         ⊿
       b   c

    hypotenuse
              ⊿ adjacent
          opposite

    tan(a) = opposite/adjacent
    adjacent * tan(a) = opposite
    '''

    # A multiplier to take into account the larger ir dot
    # observed when further away from as surface (think torch
    # beam onto a wall getting larger as it gets further away).
    # TODO: Figure out a better to do this.
    PWR = 1.1

    edgeDistance = robotHeight * math.tan(math.radians(getEdgeAngle()))
    if edgeDistance > 2:
        #print "edgeDistance of", edgeDistance
        edgeDistance **= PWR
        #print "multiplied to", edgeDistance
    # print "Distance to edge: ", edgeDistance

    return edgeDistance


def getDistances():
    """ Look around, return left, forward, right distances to edge of desk """

    panTilt.pan(-45)
    time.sleep(delay)
    left = getEdgeDistance()

    panTilt.pan()
    time.sleep(delay)
    forward = getEdgeDistance()

    panTilt.pan(45)
    time.sleep(delay)
    right = getEdgeDistance()

    panTilt.pan()

    return left, forward, right


def getDistanceAndRotation():
    """ Calculate the distance and rotation to the edge of the desk """

    # Maths help from: http://xaktly.com/MathNonRightTrig.html
    # - Specfically the law of cosines, but at least one of their
    #   examples is wrong, but methods are correct... sigh.
    #
    # For triangle with forward length, shortest of
    # left and right length, and desk edge as sides...
    #
    # f = forward distance length
    # l = left distance length
    # r = right distance length
    # e = length of desk edge between left and right views
    # s = shortest of left and right distance length
    # v = "view" angle of how much robot looks left or right
    # g = angle between d and f
    # d = distance between robot and edge of desk
    # a = angle between the way the robot is facing and edge of desk
    #     (i.e. if the robot is facing directly towards edge it's 0)
    #     (in radians or degrees?..)
    #
    # e² = f² + s² - 2 * f * s * cos(v)
    # g = sin⁻¹ * (s * sin(v) / e)
    # d = f * sin(g)
    # a = 180 - 90 - g (minus or positive depending on if s is left or right)

    l, f, r = getDistances()

    # Figure out if the edge of the desk is more to the right or left
    # s = min(l, r) <-- Used to use this, but need a -/+ as well.
    if l < r:
        s = l
        direction = -1
    else:
        s = r
        direction = 1

    cosV = math.cos(math.radians(45))
    sinV = math.sin(math.radians(45))

    e = f**2 + s**2 - 2 * f * s * cosV
    e = math.sqrt(e)
    g = math.degrees(math.asin(s * sinV / e))
    d = f * math.sin(math.radians(g))  # Switching degrees/radians f'debugging
    a = (90 - g) * direction
    '''
    # Debug stuff
    print "f =", f
    print "l =", l
    print "r =", r
    print "e =", e
    print "s =", s
    print "v =", 45
    print "g =", g
    print "d =", d
    print "a =", a
    '''
    return int(d), int(a)


try:
    while True:

        time.sleep(delay)

        # Look around
        distance, rotation = getDistanceAndRotation()

        print "Distance to edge:", distance, "cm"
        print "Rotation to edge:", rotation, "degrees"

        # Wait, forward, wait, for 0.5 seconds
        time.sleep(delay)
        pz.forward(moveSpeed)
        time.sleep(0.5)
        pz.stop()


except KeyboardInterrupt:
    print


finally:
    panTilt.cleanup()
    time.sleep(0.5)
    pz.cleanup() # This might actually clean up everything else too?
    time.sleep(0.5)
