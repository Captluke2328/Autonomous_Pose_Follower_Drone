import time, threading, logging
from click import pass_context
from dronekit import VehicleMode, Command
from pymavlink import mavutil
from time import  sleep

class Engine:
    def __init__(self,D):
        self.daemon = True
        self.vehicle = D.vehicle
        self.control = D

        print("Engine has started-------", self.vehicle)

    def send_global_velocity(self,velocity_x, velocity_y, velocity_z, duration):
        #print("Speed Here !! ------->>> ") #, velocity_x, velocity_y, velocity_z
        msg = self.vehicle.message_factory.set_position_target_global_int_encode(
        0,  # time_boot_ms (not used)
        0,
        0,  # target system, target component
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,  # frame
        0b0000111111000111,  # type_mask (only speeds enabled)
        0,  # lat_int - X Position in WGS84 frame in 1e7 * meters
        0,  # lon_int - Y Position in WGS84 frame in 1e7 * meters
        0,  # alt - Altitude in meters in AMSL altitude(not WGS84 if absolute or relative)
        # altitude above terrain if GLOBAL_TERRAIN_ALT_INT
        velocity_x,  # X velocity in NED frame in m/s
        velocity_y,  # Y velocity in NED frame in m/s
        velocity_z,  # Z velocity in NED frame in m/s
        0,
        0,
        0,  # afx, afy, afz acceleration (not supported yet, ignored in GCS_Mavlink)
        0,
        0,
        )  # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

        # send command to vehicle on 1 Hz cycle
        for x in range(0, duration):
            self.vehicle.send_mavlink(msg)
            sleep(1)

    def send_movement_command_XYA(self,velocity_x, velocity_y, altitude):
        #velocity_x positive = forward. negative = backwards
        #velocity_y positive = right. negative = left
        #velocity_z positive = down. negative = up (Yes really!)

        print("Sending XYZ movement command with v_x(forward/backward): %f v_y(right/left): %f " % (velocity_x,velocity_y))

        msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
            0,      
            0, 0,    
            mavutil.mavlink.MAV_FRAME_BODY_NED,  #relative to drone heading pos relative to EKF origin
            0b0000111111100011, #ignore velocity z and other pos arguments
            0, 0, altitude,
            velocity_x, velocity_y, 0, 
            0, 0, 0, 
            0, 0)    

        self.vehicle.send_mavlink(msg)
        #Vehicle.commands.flush()
        
    def send_movement_command_YAW(self,heading):
        speed = 0 
        direction = 1 #direction -1 ccw, 1 cw   
        #heading 0 to 360 degree. if negative then ccw 
        
        print("Sending YAW movement command with heading: %f" % heading)

        if heading < 0:
            heading = heading*-1
            direction = -1
            
        print(direction,heading)
        #point drone into correct heading 
        msg = self.vehicle.message_factory.command_long_encode(
            0, 0,       
            mavutil.mavlink.MAV_CMD_CONDITION_YAW, 
            0,          
            heading,    
            speed,      #speed deg/s
            direction,  
            1,          #relative offset 1
            0, 0, 0)    

        # send command to vehicle
        self.vehicle.send_mavlink(msg)
        #Vehicle.commands.flush()
        