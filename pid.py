import numpy as np

class pid:
    def __init__(self):
        self.cx = 0
        self.cy = 0
        self.pError = 0
        self.pid = [0.2,0.2,0]
        
    def findPID(self):
        self.posX_error = self.cx - self.width//2
        self.posY_error = self.cy - self.height//2       
        
        self.speedX = self.pid[0] * self.posX_error + self.pid[1] * (self.posX_error - self.pError)
        self.speedY = self.pid[0] * self.posY_error + self.pid[1] * (self.posY_error - self.pError)
        
        self.speedX = int(np.clip(self.speedX,-5,5))
        self.speedY = int(np.clip(self.speedY,-5,5))
        
        # Command that control z axis based on motor altitude