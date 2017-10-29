#! /usr/bin/env python

#======================================================================
#
# Python Module to control a pan and tilt kit.
# Aimed at use on Picon Zero.
#
# Created by John Evans, Oct 2017
#
# "TLT" is used rather than "TILT" only to match character count.
#
# All input values are in (approximately) in degrees.
#
# This is currently setup to imply that "facing forwards" is when the
# panning servo is centered and the tilt servo is (almost) fully
# "bent backwards" or "facing upwards" - meaning that the servos can
# only be used to look left, right, or downwards.
#
#======================================================================


# Insert path to PiconZero library so modules can be imported
import sys
sys.path.insert(1, "../../lib/PiconZero/Python")

import piconzero as pz, time


# Define which pins are the pan and tilt servos
PAN_PIN = 1
TLT_PIN = 0

# Servo default value
# If a different initial orientation is required this may need to be
# split (and other code changed) to DEFAULT_PAN_VAL and DEFAULT_TLT_VAL.
DEFAULT_VAL = 100

# Tilt servo min/max
TLT_RANGE = 70
TLT_MIN = 100
TLT_MAX = DEFAULT_VAL + TLT_RANGE  # 170

# Pan servo min/max
PAN_RANGE = 60
PAN_MIN = DEFAULT_VAL - PAN_RANGE  #  40
PAN_MAX = DEFAULT_VAL + PAN_RANGE  # 160


def init():
    """Initialize and center the servos."""
    # pz.init()
    # Set output mode to Servo
    pz.setOutputConfig(PAN_PIN, 2)
    pz.setOutputConfig(TLT_PIN, 2)
    center()
    print "Initialized panTilt"


def pan(val = 0):
    """Pan left or right from -PAN_RANGE (left) to PAN_RANGE (right)."""

    # Invert input value so left and right are flipped the correct way around
    val = -val

    # Convert input value from [-60,60] to [40,160]
    panVal = DEFAULT_VAL + val

    if panVal == int(panVal) and PAN_MIN <= panVal <= PAN_MAX:
        pz.setOutput(PAN_PIN, panVal)
    else:
        print "Error: Invalid pan value of", val
        print "Pan must be an integer between", -PAN_RANGE, "-", PAN_RANGE


def tilt(val = 0):
    """Tilt down from 0 to TLT_RANGE."""

    # Convert the input value from [0,70] to [100,170]
    tiltVal = DEFAULT_VAL + val

    if tiltVal == int(tiltVal) and TLT_MIN <= tiltVal <= TLT_MAX:
        pz.setOutput(TLT_PIN, tiltVal)
    else:
        print "Error: Invalid tilt value of", val
        print "Tilt must be an integer between", -TLT_RANGE, "-", TLT_RANGE


def left(val = PAN_RANGE):
    """Pan left to PAN_RANGE or by specified integer."""

    if val == int(val) and 1 <= val <= PAN_RANGE:
        pan(-val)
    else:
        print "Error: Invalid look left value of", val
        print "left() value must be an integer between 1 -", PAN_RANGE


def right(val = PAN_RANGE):
    """Pan right to PAN_RANGE or by specified integer."""

    if val == int(val) and 1 <= val <= PAN_RANGE:
        pan(val)
    else:
        print "Error: Invalid look right value of", val
        print "right() value must be an integer between 1 -", PAN_RANGE


def forward():
    """Pan to face forwards."""
    pz.setOutput(PAN_PIN, DEFAULT_VAL)


def down(val = TLT_RANGE):
    """Tile downwards to TLT_RANGE or by specified integer."""

    if val == int(val) and 1 <= val <= TLT_RANGE:
        tilt(val)
    else:
        print "Error: Invalid look down value of", val
        print "down() value must be an integer between 1 -", TLT_RANGE


def up():
    """Tilt upwards (i.e. face forwards)."""
    pz.setOutput(TLT_PIN, DEFAULT_VAL)


def center():
    """Center both pan and tilt to face straight forward."""
    pz.setOutput(PAN_PIN, DEFAULT_VAL)
    pz.setOutput(TLT_PIN, DEFAULT_VAL)


def cleanup():
    """Return servos to default position and then cleanup."""
    center()
    time.sleep(0.1)
    pz.cleanup()


def get(request):
    if request == "tilt_range":
        return TLT_RANGE
