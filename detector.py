import jetson.inference
import jetson.utils
import cv2
import numpy as np
from camera import *
import threading
from config import Drone
from pid import *


class detector:
    def __init__(self,C,D):
        self.ca = C
        self.net = C.ne
        self.cam = C.camera
        self.label = ""
        self.control = D.control_tab

        self.pid = pid(D)
        self.pid.start()

    def get_detections(self):
        cx = None
        cy = None

        data = []
        keypoints = []
        img = self.cam.Capture()
        poses = self.net.Process(img, overlay="links,keypoints")
        
        for pose in poses:
            
            #print(f"Pose : {pose}")
            #print(f"Keypoints : {pose.Keypoints}")
            # print(f"Link : {pose.Links}")
            
            nose_idx = pose.FindKeypoint('nose')
            neck_idx = pose.FindKeypoint('neck')
            left_wrist_idx = pose.FindKeypoint('left_wrist')
            left_shoulder_idx = pose.FindKeypoint('left_shoulder')
            right_wrist_idx = pose.FindKeypoint('right_wrist')
            right_shoulder_idx = pose.FindKeypoint('right_shoulder')
            left_elbow_idx = pose.FindKeypoint('left_elbow')
            right_elbow_idx = pose.FindKeypoint('right_elbow')
            
            if left_wrist_idx < 0 or left_shoulder_idx <0:
                continue
            
            if right_wrist_idx < 0 or right_shoulder_idx <0:
                continue
            
            nose_point = pose.Keypoints[nose_idx]
            neck_point = pose.Keypoints[neck_idx]
            left_wrist = pose.Keypoints[left_wrist_idx]
            left_shoulder = pose.Keypoints[left_shoulder_idx]
            right_wrist = pose.Keypoints[right_wrist_idx]
            right_shoulder = pose.Keypoints[right_shoulder_idx]
            left_elbow = pose.Keypoints[left_elbow_idx]
            right_elbow = pose.Keypoints[right_elbow_idx]

            cx = neck_point.x
            cy = neck_point.y
            w, h = self.ca.get_image_size()
            
            try:           
                if (neck_point.x != 0) or (neck_point.y != 0):
                
                    if (left_wrist.y < left_shoulder.y) and (right_wrist.y < right_shoulder.y) and (left_wrist.y < nose_point.y) and (right_wrist.y < nose_point.y) and (left_elbow.y < left_shoulder.y) and (right_elbow.y < right_shoulder.y):
                        self.label = "Takeoff"
                        #self.control.armAndTakeoff()

                    elif (left_wrist.y < left_shoulder.y) and (right_wrist.y > right_shoulder.y) and (left_wrist.y > nose_point.y) and (left_elbow.y > left_shoulder.y) and (right_elbow.y > right_shoulder.y):
                        self.label = "Left"
                        #self.control.forward()
                        
                    elif (right_wrist.y < right_shoulder.y) and (left_wrist.y > left_shoulder.y) and (right_wrist.y > nose_point.y) and (left_elbow.y > left_shoulder.y) and (right_elbow.y > right_shoulder.y):
                        self.label = "Right"
                        #self.control.backward()
                        
                    elif(left_wrist.y < left_shoulder.y) and (right_wrist.y > right_shoulder.y) and (left_wrist.y < nose_point.y) and (right_wrist.y > nose_point.y) and (left_elbow.y < left_shoulder.y) and (right_elbow.y > right_shoulder.y):
                        self.label = "Forward"
                        
                    elif(right_wrist.y < right_shoulder.y) and (left_wrist.y > left_shoulder.y) and (right_wrist.y < nose_point.y) and (left_wrist.y > nose_point.y) and (left_elbow.y > left_shoulder.y) and (right_elbow.y < right_shoulder.y):
                        self.label = "Backward"

                    elif(left_wrist.y < left_shoulder.y) and (right_wrist.y < right_shoulder.y) and (left_elbow.y < left_shoulder.y) and (right_elbow.y < right_shoulder.y) and (left_wrist.y > nose_point.y) and (right_wrist.y > nose_point.y):
                        self.label = "Land" 
                    
                    #else:
                    #    self.label = "Searching"
                    
                    if (self.control.takeoff):
                        self.pid.findPID(cx,cy,w,h)
      
            except:
                pass
                
            #print(nose_idx, nose_point)
            #keypoints.append([nose_idx, nose_point.x, nose_point.y])
            
            #keypoints.append([neck_idx, neck_point.x, neck_point.y])
        
            # cx = nose_point.x
            # cy = nose_point.y
            
        fps = self.net.GetNetworkFPS()
        data.append([fps, jetson.utils.cudaToNumpy(img),cx,cy])
    
        return data

        #return fps, jetson.utils.cudaToNumpy(img)
            
    def visualize(self,frame,data):
        try:
            width, height = self.ca.get_image_size()
            cv2.rectangle(frame, (int(width/2)-1,0), (int(width/2)+1, height), (255,0,0), -1) ## Horizontal
            cv2.rectangle(frame, (0, int(height/2)-1), (width, int(height/2)+1), (255,0,0),-1) ## Vertical

            cv2.circle(frame, (width // 2, height // 2), 5, (0, 255, 0), cv2.FILLED)
            cv2.arrowedLine(frame, (int(width // 2), int(height // 2)), (int(data[0][2]), int(data[0][3])), (255, 0, 255), 5, 10)
            #cv2.putText(frame, fps, (100,160),cv2.FONT_HERSHEY_SIMPLEX, 0.55, (150,150,255), 1)

        #print(nose_idx,cx,cy,width//2, height//2,fps)   
        except:
            pass
        
    def get_pose(self) -> str:
        return self.label
        
        