#! /usr/bin/env python
# coding: utf8
#
# Training data collection program to take training images without
# the robot falling off the edge of the desk or running into things

# Python imports:
import sys
import datetime
import time
#import math
#import random
import os      # Maybe needed for creating/selecting folders to save images?
sys.path.insert(0, "../../lib/PiconZero/Python")

# Camera imports:
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2

# DeskBot imports:
import piconzero as pz
import panTilt as panTilt
import infrared as ir
import hcsr04 as hcsr04
import movement as body
import hazardDetect as head


pz.init()
panTilt.init()
ir.init()
hcsr04.init()
body.init()


DEBUG = True      # Whether or not to print debug info to console.
MOVE_SPEED = 35   # Movement speed 0-100%.
DELAY      = 0.1  # The delay between movements and stuff in seconds.
RESOLUTION = 128  # Camera resolution (# x # pixels).

# Distances in centimeters:
DANGER_DIST =  8  # If closer than this, back up.
TARGET_DIST = 14  # Between DANGER & this, rotate to move alongside/away.


# Where images are saved (folders preperation, and filename index number):
now = datetime.datetime.now()
dateStr = now.strftime("%Y-%m-%d")
PATH = os.path.join("trainingImages", dateStr)
if not os.path.exists(PATH):
    os.makedirs(PATH)
PATH = os.path.join(PATH, now.strftime("%H:%M"))
if not os.path.exists(PATH):
    os.makedirs(PATH)
index = 0  # Index for the big while loop (added to filename for easy sorting).

# Initialize camera:
camera = PiCamera()
camera.resolution = (RESOLUTION, RESOLUTION)


try:
    while True:

        if DEBUG:
            print "------------------------"

        index += 1

        # Take picture
        rawCapture = PiRGBArray(camera)

        # Wait while picture is taken (and stop loop going unreliably fast)
        time.sleep(DELAY)

        # Convert image to Blue Green Red format (that's what OpenCV likes)
        camera.capture(rawCapture, format="bgr")

        # Look around. "h" refers to a potential hazard (desk edge, wall, etc.)
        hType, distanceToH, rotationToH = head.getHazardDistanceRotation()

        if DEBUG:
            print "Hazard:", str(hType.name)
            print "Distance:", str(distanceToH) + "cm"
            print "Rotation:", str(rotationToH) + "°"

        # Save image with suitable filename
        img = rawCapture.array
        imgName = str(index) + "-" + str(hType.name)
        imgName += "-d" + str(distanceToH)
        imgName += "-r" + str(rotationToH) + ".png"
        cv2.imwrite(os.path.join(PATH, imgName), img)

        # If there's no hazard in view range, or closest hazard is far away:
        if hType is head.Hazard.none or distanceToH > TARGET_DIST:
            if DEBUG:
                targetDistStr = str(TARGET_DIST) + "cm"
                print "No hazard within target distance of", targetDistStr
            body.move(MOVE_SPEED)

        # If the robot is close-ish to the desk edge:
        elif DANGER_DIST <= distanceToH <= TARGET_DIST:
            if DEBUG:
                distStr = str(DANGER_DIST) + " to " + str(TARGET_DIST) + "cm"
                print "Hazard between target/danger distance (%s)" %(distStr)
            body.turnAwayFrom(MOVE_SPEED, rotationToH)
            body.move(MOVE_SPEED)

        # If the robot is TOO CLOSE to the desk edge:
        elif distanceToH < DANGER_DIST:
            if DEBUG:
                dangerStr = " WITHIN DANGER DISTANCE (%scm)" %str(DANGER_DIST)
                print str(hType.name).upper() + dangerStr
            body.move(MOVE_SPEED, -1)  # Back up a bit
            body.turnAwayFrom(MOVE_SPEED, rotationToH)


except KeyboardInterrupt:
    print


finally:
    panTilt.cleanup()
    time.sleep(0.5)
    pz.cleanup() # This might actually clean up everything else too?
    time.sleep(0.5)
