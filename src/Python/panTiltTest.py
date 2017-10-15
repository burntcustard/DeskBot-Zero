# Picon Zero Servo Test
# Use arrow keys to move 2 servos on outputs 0 and 1 for Pan and Tilt
# Use G and H to open and close the Gripper arm
# Press Ctrl-C to stop
#

import sys
sys.path.insert(0, "../../lib/PiconZero/Python")

import piconzero as pz, time

import tty
import termios

#======================================================================
# Reading single character by forcing stdin to raw mode

def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    if ch == '0x03':
        raise KeyboardInterrupt
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)  # 16=Up, 17=Down, 18=Right, 19=Left arrows

# End of single character reading
#======================================================================

# speed = 60

print "Tests the servos by using the arrow keys to control"
print "Press <space> key to centre"
print "Press Ctrl-C to end"
print

# Define which pins are the servos
pan = 1
tilt = 0

pz.init()

# Set output mode to Servo
pz.setOutputConfig(pan, 2)
pz.setOutputConfig(tilt, 2)

# Value to increase or decrease serve value by to rotate by 1 degrees (ish)
degrees = 3;

# Centre all servos
defaultVal = tiltVal = panVal = 100
maxTilt = 170
minTilt = 100
maxPan = 160
minPan = 40
pz.setOutput (pan, panVal)
pz.setOutput (tilt, tiltVal)

# main loop
try:
    while True:
        keyp = readkey()
        if keyp == 's' or ord(keyp) == 18:
            panVal = max (minPan, panVal - degrees)
            print 'Right', panVal
        elif keyp == 'a' or ord(keyp) == 19:
            panVal = min (maxPan, panVal + degrees)
            print 'Left', panVal
        elif keyp == 'w' or ord(keyp) == 16:
            tiltVal = max (minTilt, tiltVal - degrees)
            print 'Up', tiltVal
        elif keyp == 'z' or ord(keyp) == 17:
            tiltVal = min (maxTilt, tiltVal + degrees)
            print 'Down', tiltVal
        elif keyp == ' ':
            panVal = tiltVal = defaultVal
            print 'Centre'
        elif ord(keyp) == 3:
            break
        pz.setOutput (pan, panVal)
        pz.setOutput (tilt, tiltVal)

except KeyboardInterrupt:
    print

finally:
    pz.cleanup()
