import jetson.inference
import jetson.utils
import cv2
import numpy as np

# net = None
# camera = None
# label = None

class Camera:
    def __init__(self):
        self.ne = jetson.inference.poseNet("resnet18-body", 0.15)
        self.camera = jetson.utils.videoSource("csi://0")  
        #self.camera = jetson.utils.videoSource("/dev/video0")  

    def get_image_size(self):
        self.width = self.camera.GetWidth()
        self.height = self.camera.GetHeight()
        return self.width,self.height

    def close_camera(self):
        self.camera.Close()
    
# def initialize_detector():
#     global net, camera
#     net = jetson.inference.poseNet("resnet18-body", 0.15)
#     camera = jetson.utils.videoSource("csi://0")  
    
#     return net, camera
#     print("Camera Initialized")
    
# def get_image_size():
#     global width, height
#     width = camera.GetWidth()
#     height = camera.GetHeight()
#     return camera.GetWidth(), camera.GetHeight()

# def close_camera():
#     camera.Close()
    
    