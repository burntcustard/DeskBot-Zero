#! /usr/bin/env python
# coding: utf8
#
# Training data collection program to take training images without
# the robot falling off the edge of the desk or running into things

# Python imports:
import sys
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

moveSpeed = 35   # Movement speed 0-100
delay     = 0.1  # The delay between movements and stuff in seconds
res       = 128  # Camera resolution (# x # pixels)
path      = "trainingImages/"  # Where images are saved
DANGER_DISTANCE =  5  # If closer than this distance (cm), back up.
TARGET_DISTANCE = 10  # If between DANGER and this distance (cm), rotate to move alongside/away.

camera = PiCamera()
camera.resolution = (res,res)

try:
    while True:

        # Take picture
        rawCapture = PiRGBArray(camera)

        # Wait while picture is taken (and stop loop going unreliably fast)
        time.sleep(delay)

        # Convert image to Blue Green Red format (that's what OpenCV likes)
        camera.capture(rawCapture, format="bgr")

        # Look around. "h" refers to a potential hazard (desk edge, wall, etc.)
        hType, distanceToH, rotationToH = head.getHazardDistanceRotation()

        print str(hType.name), distanceToH, rotationToH

        # Save image with suitable filename
        img = rawCapture.array
        imgName = str(hType.name)
        imgName += "-d" + str(distanceToH)
        imgName += "-r" + str(rotationToH) + ".png"
        cv2.imwrite(os.path.join(path, imgName), img)

        # If there's no hazard in view range, or closest hazard is far away:
        if hType is head.Hazard.none or distanceToH > TARGET_DISTANCE:
            body.move(moveSpeed)

        # If the robot is close-ish to the desk edge:
        elif DANGER_DISTANCE <= distanceToH <= TARGET_DISTANCE:
            print "Close-ish to", str(hType)
            body.turnAwayFrom(moveSpeed, rotationToH)
            body.move(moveSpeed)

        # If the robot is TOO CLOSE to the desk edge:
        elif distanceToH < DANGER_DISTANCE:
            print "Dangerously close to", str(hType) + "!"
            body.move(moveSpeed, -1)  # Back up a bit
            body.turnAwayFrom(moveSpeed, rotationToH)


except KeyboardInterrupt:
    print


finally:
    panTilt.cleanup()
    time.sleep(0.5)
    pz.cleanup() # This might actually clean up everything else too?
    time.sleep(0.5)
