"""
Created on Wed Oct 21 14:58:09 2020

@author: davis
"""
"""
This code is to give 2 drive motors movement commands in the forward, backwards, left and right direction.
It will also enable a spin option.

AGAIN WILL NEED pigpio INSTALLED!!!
"""
#IMPORTS
from time import sleep   #this is an invaluable function for pausing the script
import ESC_control
import os                #should import functions from os, you never know when you might need it
#import RPi.GPIO as GPIO  #this may not be necessary  #I dont think I will use this yet...
os.system ("sudo pigiod")#launching the GPIO library
sleep(1)                 #gives time for the system to process
import pigpio            #GPIO is identified on broadcom numbers

#If I want the GPIO pin work this is an example:

"""
GPIO.setmode(GPIO.BOARD)
GPIO.setup(5,GPIO.OUT)   #Left motor input A
GPIO.setup(7,GPIO.OUT)   #Left motor input B
GPIO.setup(11,GPIO.OUT)  #Right motor input A
GPIO.setup(13,GPIO.OUT)  #Right motor input B
GPIO.setwarnings(False)
"""     
#INITIAL SET-UP

ESC_1 = 8  # Motor 1 control. this will need to be changed for the actual pin when plugged im
ESC_2 = 4  # Motor 2 control. 'GPIO pin number' #Connect the ESC in a GPIO pin eg 4

pi = pigpio.pi()  #Initialise Pi connection

pi.set_PWM_dutycycle(ESC_1,   0) # initial PWM off so as not to ruin anything
pi.set_PWM_dutycycle(ESC_2,   0) # initial PWM off ""

pi.set_mode(ESC_1, pigpio.OUTPUT) # ESC_1 gpio as output
pi.set_mode(ESC_2, pigpio.OUTPUT) # ESC_2 gpio as output

pi.set_PWM_range(ESC_1, 100)  #Sets the duty cycle range of the PWM to 0-100%  *wonder if possible to set both in one operation?
pi.set_PWM_range(ESC_2, 100)  #Sets the duty cycle range of the PWM to 0-100%

""" Frequency of the PWM is defualt 8000 - 10 Hz 
The frequency can be set by using:  pi.set_PWM_frequency(gpio, frequency_value)
"""

max_duty = 100 #Duty cycle input
half_duty = 50 #half duty cycle input
min_duty = 0   #Min duty cycle input

boot_msg = """Welcome to Robotug drive operation program. 

Please ensure you have calibrated the ESCs before running this program!

Press Enter confirm you have calibrated the ESC."""
print(boot_msg) 


# MOVEMENT FUNCTIONS
