#! /usr/bin/env python
#
# Basic test of HC-SR04 ultrasonic sensor on Picon Zero

import sys
import time
sys.path.insert(0, "../../lib/PiconZero/Python")

from math import sqrt

import piconzero as pz
import hcsr04 as ultrasonic
import panTilt as panTilt

pz.init()
ultrasonic.init()
panTilt.init()

moveSpeed =  20 # Movement speed 0-100
lookSpeed =   0.3 # How much delay there is between moving panTilt
robotHeight = 9 # Height of robot's sensors in cm


def getEdgeDistance():
    distances = []
  # Slowly look down while getting distances
    for i in range(70): # Loop should be done number of degrees we're going to loop down times
        panTilt.tilt(int(i))
        time.sleep(0.2) # Take some time to get the distance
        distance = int(ultrasonic.getDistance())
        time.sleep(0.2) # Take some time to get the distance
        if distance > 99:
            distance = 99
        print "getDistance: ", distance
        distances.append(distance)
        # If not on first loop, and the istance is more than 60cm less than the last distance
        # measured (this will need A LOT if tweaking or rewriting to get accurate results!)
        if i > 0 and distance < distances[i-1] - 40:
            hypotenuse = distance
            break
    time.sleep(1)
    panTilt.up() # Look up again
    return int(sqrt(distance * distance - robotHeight * robotHeight))


def nextToEdge():
  
    isNextToEdge = True
  
    for i in range(71): # Loop should be done number of degrees we're going to loop down times (0-70)
    
        panTilt.tilt(int(i))
        
        time.sleep(0.01)
        
        if i > 65: # Only do distance measuring for the last 5 degrees

            # Check distance twice just to be sure, with some delay before
            for i in range(2):
                time.sleep(0.05) # There's a bit of delay in the rest of the loop too.
                distance = int(ultrasonic.getDistance())
                print "Ultrasonic reading:", distance
                if distance < 20: # Robot height * 2ish
                    isNextToEdge = False

    # Slowly tilt back up
    for i in range(70, 0, -1):
        panTilt.tilt(int(i))
        time.sleep(0.01)

    return isNextToEdge
  

try:
    while True:
        
        isNextToEdgeF = False
        isNextToEdgeL = False
        isNextToEdgeR = False

        # Wait, forward, wait, for 0.5 seconds each
        # TODO: "move.forward(speed, time)", or by distance function
        time.sleep(0.5)
        pz.forward(moveSpeed)
        time.sleep(0.5)
        pz.stop()
        time.sleep(0.3)

        # Look around
        time.sleep(lookSpeed)
        if nextToEdge():
            print "Looking down over the edge!"
            isNextToEdgeF = True
        else:
            print "Looking down at desk."
        time.sleep(lookSpeed)

        panTilt.pan(45)
        time.sleep(lookSpeed)
        if nextToEdge():
            print "Looking down over the edge!"
            isNextToEdgeL = True
        else:
            print "Looking down at desk."
        time.sleep(lookSpeed)

        panTilt.pan(-45)
        time.sleep(lookSpeed)
        if nextToEdge():
            print "Looking down over the edge!"
            isNextToEdgeR = True
        else:
            print "Looking down at desk."
        time.sleep(lookSpeed)

        panTilt.center()
        
        if isNextToEdgeF or isNextToEdgeR or isNextToEdgeL:
            
            if isNextToEdgeF:
                # If looking straight over we have to move back further!
                pz.reverse(moveSpeed)
                time.sleep(2)
                pz.stop()
                time.sleep(0.3)
            else:
                pz.reverse(moveSpeed)
                time.sleep(1)
                pz.stop()
                time.sleep(0.3)

            # This is backwards right now because motors are wired the wrong way.
            # TODO: Make easily flip-able with a boolean variable somewhere.
            if isNextToEdgeL:
                pz.spinLeft(moveSpeed)
            else:
                pz.spinRight(moveSpeed)
            # Turn for x seconds (TODO: Rewrite things to work in degrees or radians?)
            time.sleep(1.5)
            pz.stop()
            

    
except KeyboardInterrupt:
    print
  
  
finally:
    time.sleep(1)
    ultrasonic.cleanup()
    panTilt.cleanup()
    time.sleep(1)
    pz.cleanup() # This might actually clean up everything else too?
    time.sleep(1)
