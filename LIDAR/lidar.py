"""
Author: David Wood
Date: 27/11/2020

The code in this will be used to control the rplidar a1 for positional and distance data.

Will be using the rplidar library made by Artyom Pavlov, Yash Shah and Erik Wang
"""
# This library is for the serial interface of the rplidar a1 and the usb port of the a raspberry pi.

# IMPORTS
import time
import os
import sys
from rplidar import RPLidar 

# SET-UP   
PORT_NAME = "/dev/ttyUSB0" #** or something similar can find in the terminal
lidar = RPLidar(PORT_NAME)

# PROGRAM
try:
    print("Recording measurments... Press Crl+C to stop.")
    for scan in lidar.iter_scans():
        pass

        for (quality, angle, distance) in scan:  # the scan data format is (quality, angle, distance), we dont really mind about the quality

            print("quality={} angle={:.2f} distance={:.2f}".format(quality, angle, dc)
            time.sleep(0.8)

except KeyboardInterrupt:
    print("Stopping...")
lidar.stop()
lidar.disconnect()