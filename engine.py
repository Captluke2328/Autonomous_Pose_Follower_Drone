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
        print("Speed Here !! ------->>> ") #, velocity_x, velocity_y, velocity_z
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
        
        