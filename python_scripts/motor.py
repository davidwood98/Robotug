"""
Created on Wed Oct 21 14:58:09 2020

@author: davis
"""
import pigpio
import time
import keyboard

# MOVEMENT FUNCTIONS

def move_forward(pi, ESC_both, relays_left, relays_right, all_relays, speed):  #forward movement function
    """
    funciton will rotate both motors at equal speed
    """
    if pi.read(relays_left) or pi.read(relays_right) == 1:
        pi.set_servo_pulsewidth(ESC_both,0)
        time.sleep(0.5)
        pi.write(all_relays, 0)
        pi.set_servo_pulsewidth(ESC_both, speed)
    else:
        pi.set_servo_pulsewidth(ESC_both, speed)


def move_backwards(pi, ESC_both, relays_left, relays_right, all_relays, speed):
    """
    funciton will rotate both motors at equal speed in reverse

    """
    if pi.read(relays_left) or pi.read(relays_right) == 0:
        pi.set_servo_pulsewidth(ESC_both,0)
        time.sleep(0.5)
        pi.write(all_relays, 1)
        pi.set_servo_pulsewidth(ESC_both, speed)
    else:
        pi.set_servo_pulsewidth(ESC_both, speed)


def turn_left(pi, ESC1, ESC2, speed, idle):
    """
    In order to turn left we must engage the right motor ESC_2 and not move the left motor ESC_both
    """
    pi.set_servo_pulsewidth(ESC1, idle)
    pi.set_servo_pulsewidth(ESC2, speed)


def turn_right(pi, ESC1, ESC2, speed, idle):
    """
    In order to turn right we must engage the left motor ESC_both and not move the right motor ESC_2
    """
    pi.set_servo_pulsewidth(ESC1,speed)
    pi.set_servo_pulsewidth(ESC2,idle)


def spin_clockwise(pi, ESC_both, relays_left, relays_right, speed, idle):
    """
    funciton will rotate both motors at equal speed in opposite directions creating
    a clockwise rotation
    """
    pi.set_servo_pulsewidth(ESC_both,idle)
    time.sleep(0.5)
    pi.write(relays_left, 0)
    pi.write(relays_right, 1)
    pi.set_servo_pulsewidth(ESC_both, speed)


def spin_anticlockwise(pi, ESC_both, relays_left, relays_right, speed, idle):
    """
    will spin the robot in an anticlockwise direction
    """
    pi.set_servo_pulsewidth(ESC_both,idle)
    time.sleep(0.5)
    pi.write(relays_left, 1)
    pi.write(relays_right, 0)
    pi.set_servo_pulsewidth(ESC_both, speed)

    
def pre_planned(pi, ESC_both, ESC1, ESC2, relays_left, relays_right, all_relays, speed, idle):
    """
    executes the movement functions for a set movement output
    as an example:
    """
    move_forward(pi, ESC_both, relays_left, relays_right, all_relays, speed)
    time.sleep(2)
    turn_left(pi, ESC1, ESC2, speed, idle)
    time.sleep(2)
    turn_right(pi, ESC1, ESC2, speed, idle)
    time.sleep(2)
    move_backwards(pi, ESC_both, relays_left, relays_right, all_relays, speed)
    time.sleep(2)
    move_forward(pi, ESC_both, relays_left, relays_right, all_relays, speed)
    time.sleep(2)
    stop(pi, ESC_both, idle)


# DEBUGGING FUNCTONS
# these only operate ESC1

def manual_drive(pi, ESC1, idle): 
    """
    This allows for manual input of the motor speed
    """
    print("You have selected manual option so input a value of 0 or between min and the max value")
    time.sleep(1)
    max_value = 1900
    print("Type 'stop' to hault operations")
    while True :     #this while loop should continuously ask for an input
        inp = input()
        if inp == ("stop"):  #exit statement
            stop(pi, ESC1, idle)
            break
        elif inp == ("kill"): #kill statement
            kill(pi, ESC1)
            break           #safety feature, really
        elif int(inp) > max_value :
            print("value must be smaller than", max_value)
        else:
            pi.set_servo_pulsewidth(ESC1,inp)
    
def control(pi, ESC1, speed, idle):
    """
    This mode allows for incrimental stepping PWM control of the motor
    """
    print("The motor is starting now and can be controlled with speed increments. It should be calibrated and armed.")
    time.sleep(2)
    print("Controls - w to decrease speed & s to increase speed OR q to decrease a lot of speed & e to increase a lot of speed, or x to kill")
    while True:   #the while loop will ask for a speed change
        pi.set_servo_pulsewidth(ESC1, speed)
        inp = input()
        if inp == ("q"):
            speed -= 200    # decrementing the speed like hell
            print("speed = %s" % speed)
        elif inp == ("e"):
            speed += 200    # incrementing the speed like hell
            print("speed = %s" % speed)
        elif inp == ("w"):
            speed += 50     # incrementing the speed
            print("speed = %s" % speed)
        elif inp == ("s"):
            speed -= 50     # decrementing the speed
            print("speed = %s" % speed)
        elif inp == ("stop"):
            pi.set_servo_pulsewidth(ESC1,idle)         #going for the stop function
            break
        elif inp == ("x"):
            kill(pi, ESC1)
            break           #safety feature, really
        else:
            print("WHAT DID I SAY!! Press w,s,q or e")


# STOP FUNCITONS

def kill(pi, ESC_both):
    """
    kill will end all signals from the pi.
    """
    print("You have killed the program and will have to restart.")
    pi.set_servo_pulsewidth(ESC_both, 0)
    pi.stop()


def stop(pi, ESC_both, idle):
    """
    function will hault both the motors, bringing Robotug to a stop.
    """
    pi.set_servo_pulsewidth(ESC_both,idle)
