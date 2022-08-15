import keyboard
import jetson.inference
import jetson.utils
import sys, time
import threading
import time

import cv2
import collections
import argparse
import sys

#import detector as d
from camera import *
from detector import *

from dronekit import *
from config import *

#def setup():
    #net,cam = c.initialize_detector()
    #d.initialize_detector()
#setup()

def thread_function(z):
    
    if (z=="Takeoff"):
        drone.control_tab.armAndTakeoff()

    if (z=="Left"):
        drone.control_tab.left()
    
    if (z=="Right"):
        drone.control_tab.right()
        
    if (z=="Forward"):
        drone.control_tab.forward()
    
    if (z=="Backward"):
        drone.control_tab.backward()
        
    if (z=="Searching"):
        drone.control_tab.stop()
    
if __name__ == "__main__":

    print("Setting up detector")
    cam = Camera()

    while True:
        #fps, image = d.get_detections(net,cam)
        #data = det.get_detections()

        try:
            drone = Drone()
            break

        except Exception as e:
            print(str(e))
            sleep(2)
        
    while drone.is_active:
        try:
            #fps,image = det.get_detections()
            det = detector(cam,drone)
            data = det.get_detections()

            # Convert image into RGB Format
            #frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            frame = cv2.cvtColor(data[0][1], cv2.COLOR_BGR2RGB)
            
            # d.visualize(frame)
            # z = (d.get_pose())
            det.visualize(frame,data)
            z = (det.get_pose())
            print(z)

            x = threading.Thread(target=thread_function, args=(z,))
            x.start()

            cv2.imshow("Capture",frame)
            if cv2.waitKey(1) & 0XFF == ord('q'):
                cam.close_camera()
                break
                
        except Exception as e:
            print(str(e))

    cv2.destroyAllWindows()
