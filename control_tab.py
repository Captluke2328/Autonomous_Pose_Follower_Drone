from dronekit import *
from pymavlink import mavutil
from time import sleep
from engine import *
import numpy as np


class controlTab:
    def __init__(self,D):
        self.vehicle = D.vehicle
        self.drone = D
        self.THRESHOLD_ALT = 0.3
        self.engine_imp = Engine(self)

    def armAndTakeoff(self):
        @self.vehicle.on_attribute('mode')
        def mode_callback(self,attr_name,value):
            print(f">> Mode Update: {value} ")

        # We will not let the script to continue unless it changes to GUIDED
        self.vehicle.mode = VehicleMode("GUIDED")
        while not self.vehicle.mode.name == "GUIDED":
            sleep(1)
        
        if (self.vehicle.mode.name == "GUIDED"):
            if not self.vehicle.armed:
                self.vehicle.armed = True
                
                if (self.vehicle.location.global_relative_frame.alt < self.THRESHOLD_ALT):
                    takeoff_alt = 5
                    self.vehicle.simple_takeoff(takeoff_alt)
                    while self.vehicle.location.global_relative_frame.alt < (takeoff_alt - self.THRESHOLD_ALT):
                        sleep(0.3)
                else:
                    if (self.vehicle.location.global_relative_frame.alt > self.THRESHOLD_ALT):
                        self.vehicle.mode = VehicleMode("LAND")     
            else:
                # Disarm if landed
                if (self.vehicle.location.global_relative_frame.alt < self.THRESHOLD_ALT):
                    self.vehicle.armed = False

    def right(self):
        x,y = 0.0, 2.0 
        yaw = self.vehicle.attitude.yaw
        self.engine_imp.send_global_velocity(
            x * np.cos(yaw) - y * np.sin(yaw),
            x * np.sin(yaw) + y * np.cos(yaw),
            0,
            2,      
        )
        self.engine_imp.send_global_velocity(0,0,0,1)

    def left(self):
        x,y = 0.0, -2.0 
        yaw = self.vehicle.attitude.yaw
        self.engine_imp.send_global_velocity(
            x * np.cos(yaw) - y * np.sin(yaw),
            x * np.sin(yaw) + y * np.cos(yaw),
            0,
            2,       
        )
        self.engine_imp.send_global_velocity(0,0,0,1)

    # Go Back
    def backward(self):
        print("Backward...")
        x, y = -10, 0.0  # meters
        yaw = self.vehicle.attitude.yaw
        self.engine_imp.send_global_velocity(
            x * np.cos(yaw) - y * np.sin(yaw),
            x * np.sin(yaw) + y * np.cos(yaw),
            0,
            2, 
        )
        self.engine_imp.send_global_velocity(0, 0, 0, 1)
            
    # Go Front
    def forward(self):
        print("Forward...")
        x, y = 10, 0.0  # meters
        yaw = self.vehicle.attitude.yaw
        self.engine_imp.send_global_velocity(
           x * np.cos(yaw) - y * np.sin(yaw),
           x * np.sin(yaw) + y * np.cos(yaw),
           0,
           2, 
        )
        self.engine_imp.send_global_velocity(0, 0, 0, 1)

    # def stopMovement(self):
    #     self.speed_x = 0
    #     self.speed_y = 0
    #     self.speed_z = 0
    #     self.engine_imp.executeChangesNow()
    
    # # Yaw Left   
    # def rotateLeft(self,angle):
    #     #self.engine.rotate(-1,angle)
    #     print("rotate Left----")
    
    # # Yaw Right
    # def rotateRight(self, angle):
    #     #self.engine.rotate(1, angle)
    #     print("rotate Right----")