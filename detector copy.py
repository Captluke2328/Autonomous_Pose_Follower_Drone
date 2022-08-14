import jetson.inference
import jetson.utils
import cv2
import numpy as np

net = None
camera = None
label = None

def initialize_detector():
    global net, camera
    net = jetson.inference.poseNet("resnet18-body", 0.15)
    camera = jetson.utils.videoSource("csi://0")
    print("Camera Initialized")
    
    
def get_image_size():
    global width, height
    width = camera.GetWidth()
    height = camera.GetHeight()
    return camera.GetWidth(), camera.GetHeight()

def close_camera():
    camera.Close()
    
def get_detections():
    global cx, cy,nose_idx,fps,label
    img = camera.Capture()
    keypoints = []
    poses = net.Process(img, overlay="links,keypoints")
    
    for pose in poses:
        # print(f"Pose : {pose}")
        # print(f"Keypoints : {pose.Keypoints}")
        # print(f"Link : {pose.Links}")
        
        nose_idx = pose.FindKeypoint('nose')
        left_wrist_idx = pose.FindKeypoint('left_wrist')
        left_shoulder_idx = pose.FindKeypoint('left_shoulder')
        right_wrist_idx = pose.FindKeypoint('right_wrist')
        right_shoulder_idx = pose.FindKeypoint('right_shoulder')
        
        if left_wrist_idx < 0 or left_shoulder_idx <0:
            continue
        
        if right_wrist_idx < 0 or right_shoulder_idx <0:
            continue
        
        nose_point= pose.Keypoints[nose_idx]
        left_wrist = pose.Keypoints[left_wrist_idx]
        left_shoulder = pose.Keypoints[left_shoulder_idx]
        right_wrist = pose.Keypoints[right_wrist_idx]
        right_shoulder = pose.Keypoints[right_shoulder_idx]
        
        if (left_wrist.y < left_shoulder.y) and (right_wrist.y > right_shoulder.y):
            label = "Move left"
            
        elif (right_wrist.y < right_shoulder.y) and (left_wrist.y > left_shoulder.y):
            label = "Move Right"
            
        else:
            label = "Searching"
            
        #print(nose_idx, nose_point)
        #keypoints.append([nose_idx, nose_point.x, nose_point.y])
        cx = nose_point.x
        cy = nose_point.y
        
    fps = net.GetNetworkFPS()
    return fps, jetson.utils.cudaToNumpy(img)
        
def visualize(frame):
    try:
        cv2.rectangle(frame, (int(width/2)-1,0), (int(width/2)+1, height), (255,0,0), -1) ## Horizontal
        cv2.rectangle(frame, (0, int(height/2)-1), (width, int(height/2)+1), (255,0,0),-1) ## Vertical

        cv2.circle(frame, (width // 2, height // 2), 5, (0, 255, 0), cv2.FILLED)
        cv2.arrowedLine(frame, (int(width // 2), int(height // 2)), (int(cx), int(cy)), (255, 0, 255), 5, 10)
        #cv2.putText(frame, fps, (100,160),cv2.FONT_HERSHEY_SIMPLEX, 0.55, (150,150,255), 1)

        print(nose_idx,cx,cy,width//2, height//2,fps)   
    except:
        pass
    
def get_pose() -> str:
    return label
    
    