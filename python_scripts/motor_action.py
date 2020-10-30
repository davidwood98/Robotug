"""
Created on Wed Oct 21 14:58:09 2020

@author: davis
"""
"""
This code is to give 2 drive motors movement commands in the forward, backwards, left and right direction.
It will also enable a spin option.

AGAIN WILL NEED pigpio INSTALLED!!!
"""
#If I want the GPIO pin work this is an example:

"""
GPIO.setmode(GPIO.BOARD)
GPIO.setup(5,GPIO.OUT)   #Left motor input A
GPIO.setup(7,GPIO.OUT)   #Left motor input B
GPIO.setup(11,GPIO.OUT)  #Right motor input A
GPIO.setup(13,GPIO.OUT)  #Right motor input B
GPIO.setwarnings(False)
"""     

#IMPORTS
from time import sleep   #this is an invaluable function for pausing the script
import keyboard          #gives time for the system to process
import pigpio            #GPIO is identified on broadcom numbers
print("*" * 10, "\n")
print("""This script will not run unless the pigpio daemon has been activated by: 'sudo pigpiod'
This script will also not run if it was not sudo called from the terminal: 'sudo python3 motor_control.py'""", "\n")
print("*" * 10, "\n")

#INITIAL SET-UP
ESC_1 = 27  # Motor 1 control. this will need to be changed for the actual pin when plugged im
ESC_2 = 13  # Motor 2 control. 'GPIO pin number' #Connect the ESC in a GPIO pin eg. 4

pi = pigpio.pi()  #Initialise Pi connection

max_throttle = 1900 #Max throttle input
half_throttle = max_throttle/2 #half throttle input
min_throttle = 1100  #Min throttle input, essentially a neutral
low_throttle = 1140


#ESC arming
pi.set_servo_pulsewidth(ESC_1,0)
pi.set_servo_pulsewidth(ESC_2,0)
sleep(2)
pi.set_servo_pulsewidth(ESC_1, max_throttle)
pi.set_servo_pulsewidth(ESC_2, max_throttle)
sleep(2)
pi.set_servo_pulsewidth(ESC_1, min_throttle)
pi.set_servo_pulsewidth(ESC_2, min_throttle)
sleep(1)

#PROGRAM START
boot_msg = """Welcome to Robotug drive operation program. 

Please ensure you have calibrated the ESCs before running this program!

Please type 'confirm' to confirm you have calibrated the ESC.\n"""
print(boot_msg) 

cnfrm = input()  #asking for a confirmation input
if cnfrm == ("confirm"):  #conditional statements
    print("Excellent\n")
    
else:
    print("Please go and calibrate the ESCs")
      #should call the kill function from ESC_control.py
    

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
    pi.set_servo_pulsewidth(ESC_1, low_throttle)
    pi.set_servo_pulsewidth(ESC_2, low_throttle)


def move_backwards():
    """
    funciton will rotate both motors at equal speed in reverse

    """
    #currently this an unknown if possible with the ESC
    


def turn_left():
    """
    In order to turn left we must engage the right motor ESC_2 and not move the left motor ESC_1
    """
    pi.set_servo_pulsewidth(ESC_1,min_throttle)
    pi.set_servo_pulsewidth(ESC_2,low_throttle)


def turn_right():
    """
    In order to turn right we must engage the left motor ESC_1 and not move the right motor ESC_2
    """
    pi.set_servo_pulsewidth(ESC_1,low_throttle)
    pi.set_servo_pulsewidth(ESC_2,min_throttle)


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
    move_forward()
    sleep(2)
    turn_left()
    sleep(2)
    turn_right()
    sleep(2)
    move_forward()
    sleep(2)
    stop()


def stop():
    """
    function will hault both the motors, bringing Robotug to a stop.
    """
    pi.set_servo_pulsewidth(ESC_1,min_throttle)
    pi.set_servo_pulsewidth(ESC_2,min_throttle)


# ACUTUAL PROGRAMME

selected_mode = input()  #asking for an input from keyboard command

if selected_mode == ("control"):
    while keyboard.KEY_DOWN:
        if keyboard.is_pressed("up"):
            print("moving forward")
            move_forward()
        elif keyboard.is_pressed("down"):
            move_backwards()
            print("moving back")
        elif keyboard.is_pressed("left"):
            turn_left()
            print("turning left")
        elif keyboard.is_pressed("right"):
            turn_right()
            print("turning right")
        elif keyboard.is_pressed("ctrl + x"):
            break
        else:
            stop()
            print("stopped")

if selected_mode == ("pre-planned"):
    pre_planned()

else:
    print("control or pre-planned.")