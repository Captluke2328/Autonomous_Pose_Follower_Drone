import numpy as np
import time, threading, logging

class pid(threading.Thread):
    def __init__(self,D):
        threading.Thread.__init__(self)
        self.daemon = True
        self.cx = 0
        self.cy = 0
        self.w = 0
        self.h = 0
        self.pError = 0
        self.pid = [0.2,0.2,0]
        self.control = D.control_tab
        
    def findPID(self,cx,cy,w,h):
        self.cx = cx
        self.cy = cy
        self.width = w
        self.height = h

        self.posX_error = self.cx - self.width//2
        self.posY_error = self.cy - self.height//2       
        
        self.speedX = self.pid[0] * self.posX_error + self.pid[1] * (self.posX_error - self.pError)
        self.speedY = self.pid[0] * self.posY_error + self.pid[1] * (self.posY_error - self.pError)
        
        self.speedX = int(np.clip(self.speedX,-15,15))
        self.speedY = int(np.clip(self.speedY,-15,15))

        #print("PID Data",self.speedX, self.speedY)

        self.control.yaw( self.speedX,self.speedY)


    def run(self):
        pass
       
        #Command that control z axis based on motor altitude
        #pass