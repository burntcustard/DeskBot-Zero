from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

res = 128

camera = PiCamera()
camera.resolution = (res,res)
rawCapture = PiRGBArray(camera)

time.sleep(0.1)

camera.capture(rawCapture, format="bgr")

image = rawCapture.array
cv2.imwrite("testImage.png", image)
