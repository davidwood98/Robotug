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
os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()
lcd = pygame.display.set_mode((480,320))
pygame.mouse.set_visible(False)
lcd.fill((0,0,0))
pygame.display.update()  

PORT_NAME = "/dev/ttyUSB0" #** or something similar can find in the terminal
lidar = RPLidar(PORT_NAME)


#FUNCTIONS
def scan():
    """
    processes the lidar data
    """
    max_distance = 0
    print('Recording measurments... Press Crl+C to stop.')
    for scan in lidar.iter_scans():
        if len(scan) > 100:
            lcd.fill((0,0,0))
            for (quality, angle, distance) in scan:
                max_distance = max([min([5000, distance]), max_distance])
                radians = angle * pi / 180.0
                x = distance * cos(radians)
                y = distance * sin(radians)
                point = (240 + int(x / max_distance * 159), 160 + int(y / max_distance * 159))
                lcd.set_at(point, pygame.Color(255, 255, 255))
            pygame.display.update()
            print("quality={} angle={:.2f} distance={:.2f}".format(quality, angle, distance))


if __name__ == "__main__":
    scan()
