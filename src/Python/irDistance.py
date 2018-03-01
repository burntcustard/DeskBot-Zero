#! /usr/bin/env python
# coding: utf8

# Test code for 4tronix Picon Zero to work with an
# analog Infrared Distance Sensor (e.g. GP2Y0A21).
#
# Currently just prints the signal from an analog pin.
#
#-----------------------------------------------------------------
# GP2Y0A21 info:
# Datasheet: http://www.robot-electronics.co.uk/files/gp2y0a21.pdf
# PiconZero input is 0-5v, 0 - 1023 readings.
# Sensor is 0-3.3v, actually reads ~10 (far) to ~690 at 10cm.
#-----------------------------------------------------------------


import time
import sys
sys.path.insert(1, "../../lib/PiconZero/Python")

import piconzero as pz
import numpy as np
from scipy.optimize import curve_fit


# Ratio between 0-100% indicating reflectivity of the observed surface
# TODO: Change from constant to a variable based off camera input.
REFLECTIVE_RATIO = 100

IR_PIN = 3  # The pin number used to connect the infrared sensor


pz.init()
pz.setInputConfig(IR_PIN, 1)  # Set input pin to analog


def continuousRead():

    try:
        while True:
            ir = pz.readInput(IR_PIN)
            print ir
            time.sleep(1)
    except KeyboardInterrupt:
        print()
    finally:
        pz.cleanup()


def read():
    ir = pz.readInput(IR_PIN)
    return ir


def calibrate(speed=1):

    print "Infrared sensor calibration started..."
    print "Initial reading:", pz.readInput(IR_PIN)

    # WIP reflectivity
    # reflectivity = input("Input estimate surface reflectivity (0-100): ")
    # if not 0 <= reflectivity <= 100:
    #     print "Error: Invalid reflectivity input. Cancelling calibration."
    #     return False

    maxDistance = input("Input max distance required in cm: ")
    if not 0 <= maxDistance <= 100:
        print "Error: Invalid maxDistance input. Cancelling calibration."
        return False

    calibrations = np.array([1023], dtype='uint16') # 675 should be max (3.3v)
    distances = np.array([9], dtype='uint16')       # ... at 0cm away.
    distance = 10

    while distance <= maxDistance:
        distances = np.append(distances, distance)
        print "Place object", distance, "cm away from sensor"
        time.sleep(speed)
        for _ in range(0, 3):
            print "."
            time.sleep(speed)
        ir = pz.readInput(IR_PIN)
        print "Reading for", distance, "cm:", ir
        time.sleep(speed)
        #
        # First reading (-1) is put into calibrations array for 0cm as well:
        # TODO: Explain why?
        #if calibrations.size == 0:
        #    calibrations = np.append(calibrations, ir + 1)
        calibrations = np.append(calibrations, ir)
        distance += 10

    # Clever WIP maths stuff


    #distancesCount = distances.size
    yData = calibrations
    xData = distances

    # New exponential scipy stuff
    # https://docs.scipy.org/doc/scipy-0.19.1/reference/generated/scipy.optimize.curve_fit.html
    # https://stackoverflow.com/questions/15624070/why-does-scipy-optimize-curve-fit-not-fit-to-the-data

    def func(x, a, b, c):
        return a * np.exp(-b * x) + c

    # Fit an exponential
    popt, pcov = curve_fit(func, xData, yData)

    # Old polyfit stuff
    #z = np.poly1d(np.polyfit(x, y, 2))
    ##xNew = np.linspace(x[0], x[-1], distancesCount)
    #xNew = np.arange(1024)  # Create 0-1023 array for reading lookup table
    #yNew = z(xNew).astype(int)


    # Displaying the data

    print "Calibration finished."

    print "popt:"
    print popt
    print "pcov:"
    print pcov
    trialX = np.arange(1024)
    yExp = func(trialX, *popt)
    print "yExp:"
    print yExp


    '''
    print "xNew:"
    #print xNew
    print "yNew:"
    #print yNew
    print ""
    print "Fancy graph:"

    # print estimated distances for the first half (0-511) of the input readings
    # i = 16 because 1024 / 32 / 2 = 16
    i = 32
    while i > 0:
        outputStr = " "

        # Add a space if row label 2 digits not 3:
        if i * 32 - 1 < 100:
            outputStr += " "

        outputStr += str(i * 32 - 1) + '|'
        calibrationRow = False

        j = 0
        for k in np.nditer(calibrations):
            if i * 32 -1 >= k >= (i - 1) * 32 - 1:
                calibrationRow = True
                rowDistanceIndex = j
            j += 1

        if calibrationRow:
            for j in range(0, min(80, yNew[i * 32 - 1]), 2):
                outputStr += '▯'
                if j >= 78:
                    outputStr += '+'
        else:
            for j in range(0, min(80, yNew[i * 32 - 1]), 2):  # Estimated dist
                outputStr += '▮'
                if j >= 78:
                    outputStr += '+'

        outputStr += " " + str(yNew[i * 32 -1])
        if calibrationRow:
            outputStr += " / " + str(y[rowDistanceIndex])
        print outputStr
        i -= 1

    print "-in-|10cm|20cm|30cm|40cm|50cm|60cm|70cm|80cm|"
 '''
    #
    #print "Original data:"
    #d = np.nditer(x, flags=['f_index'])
    #for i in range(0, distancesCount):
    #    print distances[i], "cm:", y[i]
    #print "Calculated data:"
    #for i in range(0, distancesCount):
    #    print distances[i], "cm:", int(yNew[i])


def cleanup():
    pz.cleanup()
