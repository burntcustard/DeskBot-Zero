#! /usr/bin/env python
# coding: utf8
#
# Moves the pan and tilt module and performs calculations to
# determine the distance and rotation to the edge of a desk

import sys
import math
sys.path.insert(0, "../../lib/PiconZero/Python")


DEBUG = False


def getDistanceAndRotationToEdge(l, f, r):
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
    # g = angle between f and e
    # d = distance between robot and edge of desk
    # a = angle between the way the robot is facing and edge of desk
    #     (i.e. if the robot is facing directly towards edge it's 0)
    #     (in radians or degrees?..)
    #
    # e² = f² + s² - 2 * f * s * cos(v)
    # g = sin⁻¹ * (s * sin(v) / e)
    # d = f * sin(g)
    # a = 180 - 90 - g (minus or positive depending on if s is left or right)

    # Figure out if the edge of the desk is more to the right or left
    # s = min(l, r) <-- Used to use this, but need a -/+ as well.
    if r is None and l is None:
        print "ERROR: Tried to do edge calcs without right or left distances."
    else:
        # If there's no _r_ight distance or _l_eft distance is _s_horter:
        if r is None or l < r:
            s = l
            direction = -1
        # If there's no _l_eft distance or _r_ight distance is _s_horter:
        elif l is None or r < l:
            s = r
            direction = 1
        # Else _l_eft and _r_ight distances are equal, just use _l_eft:
        else:
            s = l
            direction = 0

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

    if DEBUG is True:
        print "Distance to edge:", int(d), "cm"
        print "Rotation to edge:", int(a), "degrees"

    return int(d), int(a)
