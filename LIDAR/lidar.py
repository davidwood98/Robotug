"""
Author: David Wood
Date: 27/11/2020

The code in this will be used to control the rplidar a1 for positional and distance data.

Will be using the rplidar library made by Artyom Pavlov, Yash Shah and Erik Wang
"""
# This library is for the serial interface of the rplidar a1 and the usb port of the a raspberry pi.

# Should create a screen showing the position of each data point and print the raw data. 

# IMPORTS
import time
import os
import sys
from math import cos, sin, pi
import pygame
from rplidar import RPLidar 

# SET-UP   
PORT_NAME = "/dev/ttyUSB0" #** or something similar can find in the terminal
lidar = RPLidar(PORT_NAME)
lcd = pygame.display.set_mode((320,240))

#FUNCTIONS
def process_data(data):
    """
    processes the lidar data from scan[]
    """
    print("quality={} angle={:.2f} distance={:.2f}".format(quality, angle, distance))
    time.sleep(0,8)
    max_distance = max([distance])
    radians = angle * pi / 180.0
    x = distance * cos(radians)
    y = distance * sin(radians)
    point = (240 + int(x / max_distance * 159), 160 + int(y / max_distance * 159))
    lcd.set_at(point, pygame.Color(255, 255, 255))
    pygame.display.update()

# PROGRAM
try:
    print("Recording measurments... Press Crl+C to stop.")
    for scan in lidar.iter_scans():
        pass
        lcd.fill((0,0,0))

        for (quality, angle, distance) in scan:  # the scan data format is (quality, angle, distance), we dont really mind about the quality
            scan_data = []

        process_data(scan_data)
        
except KeyboardInterrupt:
    print("Stopping...")
lidar.stop()
lidar.disconnect()