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
lcd = pygame.display.set_mode((720,480))
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
    max_distance = 0  #scaling the pygame window
    print('Recording measurments... Press Crl+C to stop.')
    for scan in lidar.iter_scans():
        if len(scan) > 50:
            lcd.fill((0,0,0))
            pygame.draw.line(lcd,pygame.Color(100,100,100) , (0, 240),(720, 240))
            pygame.draw.line(lcd,pygame.Color(100,100,100) , (360, 0),(360, 480))
            
            for (quality, angle, distance) in scan:
                if distance < 2000:
                    max_distance = max([min([5000, distance]), max_distance])
                    radians = angle * pi / 180.0
                    x = distance * cos(radians)
                    y = distance * sin(radians)
                    point = (360 + int(x / max_distance * 159), 240 + int(y / max_distance * 159))            
                    lcd.set_at(point, pygame.Color(255, 255, 255))
                    if distance < 160 :
                        print("collision detection")
                        print("reversing")
                        once distance > 300: #need a way to make this be the next trigger
                            print("drive")
                   

            pygame.display.update()
        #print(min_distance)
            #print("quality={} angle={:.2f} distance={:.2f}".format(quality, angle, distance))

def min_distance():
    for scan in lidar.iter_scans():
        for (_,_,distance) in scan:
            return distance
            
        
if __name__ == "__main__":
    scan()
    
    #dis = scan()
    #print(dis) # needs to return distance in main
