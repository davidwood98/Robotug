# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 16:48:09 2020

@author: davis
"""
"""
!!!Need to download pigpio for the pwm control of GPIO prior to code execute!!!

Email code to self for Rpi operation
"""

# Simple code for the Raspberry Pi that should move a Robot Forward and Back then left and right.
# Need to get pigpio for the pwm
# Modules to import are Rpi.gpio for GPIO pin position data and time for timing.

# a lot of code examples use this, import RPi.GPIO as GPIO, instead of pigpio just as a note!!

from time import sleep   #importing sleep from time library to call directly
import os                #importing the os so as to communicate with the system
os.system ("sudo pigiod")  #launching the GPIO library
sleep(1) # Gives time for the system to process
import pigpio

"""
Code for 1 motor and ESC.
"""

ESC = 4 #'GPIO pin number' #Connect the ESC in a GPIO pin eg 4

pi = pigpio.pi();  #Initialise Pi connection
pi.set_servo_pulsewidth(ESC, 0)  #Sets all PWM traffic to 0

max_value = 2000 #Standard maximum pwm signal for the ESC to motor
                 #change this if ESC's max value is different or leave it be
min_value = 700  #Standard minimum pwm signal for the ESC to motor
                 #change this if ESC's min value is different or leave it be
print ("For first time launch, select calibrate")
print ("Type the exact word for the function you want")
print ("calibrate OR manual OR control OR arm OR stop")

#Defining operating modes

def calibrate():  #This procedure will automatically calibrate the ESC, for a normal ESC that is
    pi.set_servo_pulsewidth(ESC, 0)  #ensures the start point is zero speed
    print ("Disconnect power and then hit Enter to start calibration.")
    inp = input()  #Raw input
    if inp == (""):
        pi.set_servo_pulsewidth(ESC, max_value)
        print("Reconnect power, wait until motor is running at constant speed then press Enter")
        sleep(2)
        inp = input()
        if inp == input(""):
            pi.set_servo_pulsewidth(ESC, min_value)
            print("calibrating...")
            sleep(3)
            pi.set_servo_pulsewidth(ESC,0)
            print("calibrating...")
            sleep(2)
            print("Arming ESC now")
            pi.set_servo_pulsewidth(ESC,min_value)
            sleep(1)
            manual_drive() #not sure if I want to instantly call another mode??

def manual_drive():  #This procedure will allow exact value control
    print("You have selected manual option so give a value between 0 and you max value")
