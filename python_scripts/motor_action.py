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
import keyboard 
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
ESC_2 = 4  # Motor 2 control. 'GPIO pin number' #Connect the ESC in a GPIO pin eg. 4

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

Please type 'confirm' to condirm you have calibrated the ESC.\n"""
print(boot_msg) 

confirm = input()  #asking for a confirmation input
if confirm == ("confirm"):  #conditional statements
    print("Excellent\n")
    
else:
    print("Please go and calibrate the ESCs")
    ESC_control.kill()  #should call the kill function from ESC_control.py
    

print("*" * 15, "\n")
sleep(1)
movement_msg = """To move Robotug select an operation.
Please type the command exactly.
Select:

control , pre-planned\n"""
print(movement_msg)


# MOVEMENT FUNCTIONS

def move_forward():  #forward movement function
    """
    funciton will rotate both motors at equal speed
    """
    pi.set_PWM_dutycycle(ESC_1, 100)
    pi.set_PWM_dutycycle(ESC_2, 100)


def move_backwards():
    """
    funciton will rotate both motors at equal speed in reverse

    """
    #currently this an unknown if possible with the ESC
    


def turn_left():
    """
    In order to turn left we must engage the right motor ESC_2 and not move the left motor ESC_1
    """
    pi.set_PWM_dutycycle(ESC_1,0)
    pi.set_PWM_dutycycle(ESC_2,100)


def turn_right():
    """
    In order to turn right we must engage the left motor ESC_1 and not move the right motor ESC_2
    """
    pi.set_PWM_dutycycle(ESC_1,100)
    pi.set_PWM_dutycycle(ESC_2,0)


def spin():
    """
    funciton will rotate both motors at equal speed in opposite directions
    """
    #currently this an unknown if even possible with the ESC
    


def pre_planned():
    """
    executes the movement functions for a set movement output
    as an example:
    """
    move_forward()
    sleep(1)
    turn_left()
    sleep(1)
    turn_right()
    sleep(1)
    move_backwards()
    


def stop():
    """
    function will hault both the motors, bringing Robotug to a stop.
    """
    pi.set_PWM_dutycycle(ESC_1,0)
    pi.set_PWM_dutycycle(ESC_2,0)


# ACUTUAL PROGRAMME

selected_mode = input()  #asking for an input from keyboard command

if selected_mode == ("control"):
    while keyboard.KEY_DOWN:
        if keyboard.is_pressed("up"):
            print("moving forward")
            move_forward()
        if keyboard.is_pressed("down"):
            move_backwards()
            print("moving back")
        if keyboard.is_pressed("left"):
            turn_left()
            print("turning left")
        if keyboard.is_pressed("right"):
            turn_right()
            print("turning right")
        if keyboard.is_pressed("ctrl + x"):
            break
    
elif selected_mode == ("pre-planned"):
    pre_planned()

else:
    print("control or pre-planned.")