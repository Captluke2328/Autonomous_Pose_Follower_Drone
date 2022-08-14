import keyboard
import jetson.inference
import jetson.utils
import sys, time

import cv2
import collections
import argparse
import sys

#import detector as d
from camera import *
from detector import *

#def setup():
print("Setting up detector")
cam = Camera()
#net,cam = c.initialize_detector()
#d.initialize_detector()

#setup()

while True:
    #fps, image = d.get_detections(net,cam)
    #data = det.get_detections()

    det = detector(cam)
    data = det.get_detections()
    #fps,image = det.get_detections()

    # Convert image into RGB Format
    frame = cv2.cvtColor(data[0][1], cv2.COLOR_BGR2RGB)
    #frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # d.visualize(frame)
    # z = (d.get_pose())

    det.visualize(frame,data)
    z = (det.get_pose())
    print(z)
        
    cv2.imshow("Capture",frame)
    if cv2.waitKey(1) & 0XFF == ord('q'):
        cam.close_camera()
        break
    
cv2.destroyAllWindows()

try:
    while True:
        pass
    
except:
    pass