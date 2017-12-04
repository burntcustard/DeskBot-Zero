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
    # s = min(l, r) <-- Used to use this, but need additional things.

    #  r | l | s
    #  x | x | ?
    #  1 | 1 | ?     Logic table for _r_ight, _l_eft, and output
    #  0 | 0 | ?     _s_hortest distances from robot to desk edge
    #  x | 0 | l
    #  1 | x | r     x = None
    #  0 | 1 | r     1 = arbitrary high-ish value
    #  x | 1 | l     0 = arbitrary low-ish value
    #  1 | 0 | l
    #  0 | x | r

    # Distance to right and left are missing or identical?
    if r is l:
        if r is None:
            if DEBUG:
                print "INFO: Skipping edge calcs because of missing distances."
            return f, 0
        else:
            if DEBUG:
                print "INFO: Skipping edge calcs because of identical distances."
            # This is unlikely-ish because l, f, r are floats...
            #
            #  r < f       r > f
            #    ◆  |  or    ◼
            #  ____➘|      __🠛__
            #
            return min(r, f), 0

    # Figure out if _l_eft or _r_ight is the shorter distance
    else:
        if r is not None and (l < r):  # Python3 fix?... (l is None or l < r)
            s = r
            direction = 1
        else:
            s = l
            direction = -1

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

    if DEBUG:
        print "Distance to edge:", int(d), "cm"
        print "Rotation to edge:", int(a), "degrees"

    return int(d), int(a)
