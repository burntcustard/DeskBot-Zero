
import sys
sys.path.insert(0, "../../lib/PiconZero/Python")

import piconzero as pz, time


# Define which pins are the servos
panPin = 1
tiltPin = 0

# Servo default value
panVal = tiltVal = defaultVal = 100

# Tilt servo min/max
tiltRange = 70
minTilt = 100
maxTilt = defaultVal + tiltRange

# Pan servo min/max
panRange = 50
minPan = defaultVal - panRange #  40
maxPan = defaultVal + panRange # 160


def init():
  pz.init()
# Set output mode to Servo
  pz.setOutputConfig(panPin, 2)
  pz.setOutputConfig(tiltPin, 2)
  center()
  print "Initialized panTilt"


# Pan left or right from -60 (left) to 60 (right)
def pan(val):
  # Convert the input value from [-60,60] to [40,160]
  panVal = defaultVal + val
  if minPan <= panVal <= maxPan:
    #print "Trying to set pan (" + str(panPin) + ") to", panVal
    pz.setOutput (panPin, panVal)
  else:
    print("ERROR: Out of range pan value of", val)
    print("Pan must be between", minPan - defaultVal, "and", maxPan - defaultVal)


# Tilt down from 0 to 70
def tilt(val):
  # Convert the input value from [0,70] to [100,70]
  tiltVal = defaultVal + val
  if minTilt <= tiltVal <= maxTilt:
    pz.setOutput(tiltPin, tiltVal)
  else:
    print("ERROR: Out of range tilt value of", val)
    print("Tilt must be between", minTilt - defaultVal, "and", maxTilt - defaultVal)


def left(val = panRange):
  pan(-val)


def right(val = panRange):
  pan(val)


def forward():
  pz.setOutput(panPin, defaultVal)
  

def up():
  pz.setOutput(tiltPin, defaultVal)


def down(val = tiltRange):
  tilt(val)


# Center both pan and tilt so robot looks straight forwards:
def center():
  pz.setOutput(panPin, defaultVal)
  pz.setOutput(tiltPin, defaultVal)


def cleanup():
  center()
  time.sleep(0.2)
  pz.cleanup()
