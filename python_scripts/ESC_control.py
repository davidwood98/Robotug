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

pi = pigpio.pi()  #Initialise Pi connection
pi.set_servo_pulsewidth(ESC, 0)  #Sets all PWM traffic to 0

max_value = 2000 #Standard maximum pwm signal for the ESC to motor
                 #change this if ESC's max value is different or leave it be
min_value = 700  #Standard minimum pwm signal for the ESC to motor
                 #change this if ESC's min value is different or leave it be
print ("For first time launch, select calibrate. If the ESC is calibrated, select arm.")
print ("Type the exact word for the function you want")
print ("calibrate OR manual OR control OR arm OR kill\n")
print ("Once in a function, type 'home', to select a different mode")

#Defining operating modes

def calibrate():  #This procedure will automatically calibrate the ESC, for a normal ESC that is
    pi.set_servo_pulsewidth(ESC, 0)  #ensures the start point is zero speed
    print ("Disconnect power and then hit Enter to start calibration.")
    inp = input()  #Raw input
    if inp == (""):  #hit enter
        pi.set_servo_pulsewidth(ESC, max_value)
        print("Reconnect power, wait until motor is running at constant speed then press Enter")
        sleep(2)
        inp = input()
        if inp == input(""):
            print("calibrating...")
            pi.set_servo_pulsewidth(ESC, min_value)
            sleep(3)
            print("calibrating...")
            pi.set_servo_pulsewidth(ESC,0)
            sleep(3)
            print("Arming ESC now")
            sleep(0.5)
            armed() #not sure if I want to instantly call another mode??
        elif inp == ("kill"):
            kill()           #safety feature, really
            pass
        pass
    pass
pass

def manual_drive():  #This procedure will allow exact value control
    print("You have selected manual option so input a value between 0 and the max value")
    sleep(1)
    print("Type 'stop' to hault operations")
    while True :     #this while loop should continuously ask for an input
        inp = input()
        if inp == ("stop"):  #exit statement
            stop()
            break
        elif inp == ("kill"): #kill statement
            kill()
            break           #safety feature, really
        elif inp == ("home"):  #takes you back to selecting
            function_selector()
            break
        elif int(inp) > max_value :
            print("value must be smaller than", max_value)
        else:
            pi.set_servo_pulsewidth(ESC,inp)
            pass
        pass
    pass
pass
    
def control():  #this mode allows for stepped PWM control of the motor
    print("The motor is starting now and can be controlled with speed increments. It should be calibrated and armed.")
    sleep(2)
    speed = 1000  #the resting speed of the motor, should be at least 700(min)
    print("Controls - w to decrease speed & s to increase speed OR q to decrease a lot of speed & e to increase a lot of speed")
    while True:   #the while loop will ask for a speed change
        pi.set_servo_pulsewidth(ESC, speed)
        inp = input()
        if inp == ("q"):
            speed -= 300    # decrementing the speed like hell
            print("speed = %s" % speed)
        elif inp == ("e"):
            speed += 300    # incrementing the speed like hell
            print("speed = %s" % speed)
        elif inp == ("w"):
            speed += 50     # incrementing the speed
            print("speed = %s" % speed)
        elif inp == ("s"):
            speed -= 50     # decrementing the speed
            print("speed = %s" % speed)
        elif inp == ("stop"):
            stop()          #going for the stop function
            break
        elif inp == ("kill"):
            kill()
            break           #safety feature, really
        elif inp == ("manual"):
            manual_drive()
            break  #breaks the while
        elif inp == ("arm"):
            armed()
            break
        elif inp == ("home"): #takes you back to selecting
            function_selector()
            break
        else:
            print("WHAT DID I SAY!! Press w,s,q or e")
            pass
        pass
    pass
pass

def armed():  #procedure to arm the ESC
    print("Make sure the battery is connected and press Enter")
    inp = input()
    if inp == (""):  #only requirement is to hit Enter and the arming will commence
        pi.set_servo_pulsewidth(ESC, 0)
        sleep(1)     #little pause between settings to no ruin motor
        pi.set_servo_pulsewidth(ESC, max_value)
        sleep(1)
        pi.set_servo_pulsewidth(ESC, min_value)
        sleep(1)
        print("the system is now armed")
        pass
    elif inp == ("home"):
        function_selector()
    elif inp == ("kill"):
        kill()           #safety feature, really
    pass
pass

def stop():  #stop will cut all signal to the motor
    pi.set_servo_pulsewidth(ESC, 0)
    print("You have stopped the Motor")
    print("press Enter is you want to go home")
    print("if not, kill the program to exit")
    inp = input()
    if inp == (""):
        function_selector()
        pass
    elif inp == ("kill"):
        kill()
    pass
pass

# The kill function is only for emergencies
def kill():  #kill will end all signals from the pi.
    print("You have killed the program and will have to restart.")
    pi.set_servo_pulsewidth(ESC, 0)
    pi.stop()
    pass
pass

def function_selector():    #home button that allows you to resellect a mode, type 'home'
    pi.set_servo_pulsewidth(ESC, 0)
    sleep(1)
    print("welcome home, please select an operating mode")
    print("Reminder! The options are: manual, arm, control or kill")
    inp = input()
    if inp == ("manual"):   #select manual_drive
        manual_drive()
        pass
    elif inp == ("arm"):    #select armed
        armed()
        pass
    elif inp == ("control"):#select control
        control()
        pass
    elif inp == ("kill"):   #select kill
        kill()
        pass
    elif inp == ("calibrate"): #this should already be done
        print("calibration should be done on initial boot up. You will have to restart the program")
        pass
    pass
pass

# The actual program  

inp = input()
if inp == ("manual"):
    manual_drive()
elif inp == ("calibrate"):
    calibrate()
elif inp == ("arm"):
    armed()
elif inp == ("control"):
    control()
elif inp == ("kill"):
    kill()
else:
    print("You have messed up, please try again. The operators are: calibrate , manual , arm , control , kill")
    pass
pass
