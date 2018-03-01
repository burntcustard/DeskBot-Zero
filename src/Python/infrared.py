#! /usr/bin/env python
# coding: utf8

"""
Test code for 4tronix Picon Zero to work with an
analog Infrared Distance Sensor (e.g. GP2Y0A21).

Currently just prints the signal from an analog pin.

#-----------------------------------------------------------------
# GP2Y0A21 info:
# Datasheet: http://www.robot-electronics.co.uk/files/gp2y0a21.pdf
# PiconZero input is 0-5v, 0 - 1023 readings.
# Sensor is 0-3.3v, actually reads ~10 (far) to ~690 at 10cm.
#-----------------------------------------------------------------

"""


import time
import sys
sys.path.insert(1, "../../lib/PiconZero/Python")

import piconzero as pz


# Ratio between 0-100% indicating reflectivity of the observed surface
# TODO: Change from constant to a variable based off camera input.
REFLECTIVE_RATIO = 100

IR_PIN = 3  # The pin number used to connect the infrared sensor


def init():
    """Initializes the infrared sensor on the Picon Zero and and print a reading."""
    # pz.init()
    pz.setInputConfig(IR_PIN, 1)  # Set input pin to analog
    time.sleep(0.5)  # Wait ½ a second to ensure pin is set correctly
    print "Initialized irDigital, initial reading:", analogRead()


def analogRead():
    return pz.readInput(IR_PIN)


def read():
    return analogRead()


def continuousRead():
    """Print infrared reading once a second until exited."""
    try:
        while True:
            ir = pz.readInput(IR_PIN)
            print ir
            time.sleep(1)
    except KeyboardInterrupt:
        print()
    finally:
        pz.cleanup()


def digitalRead():
    """Returns true if the ir output is higher than threshold value."""
    # indicating ~80% reflectivity ~30cm away)
    return pz.readInput(IR_PIN) > 200


def readWithDelay(delayTime = 0.01):
    """Get ir reading with a delay just before and after to ensure accuracy."""
    time.sleep(delayTime)
    value = read()
    time.sleep(delayTime)
    return value


def cleanup():
    """Clears infrared and other Pizon Zero setups."""
    pz.cleanup()
