"""
Created on Wed Oct 21 14:58:09 2020

@author: davis
"""
import pigpio
import time
import keyboard

# MOVEMENT FUNCTIONS

def move_forward(pi, ESC1, ESC2, relay_left1, relay_left2, relay_right1, relay_right2, speed):  #forward movement function
    """
    funciton will rotate both motors at equal speed
    """
    if pi.read(relay_left1) or pi.read(relay_left2) or pi.read(relay_right1) or pi.read(relay_right2)== 1:
        pi.set_servo_pulsewidth(ESC1,1100)
        pi.set_servo_pulsewidth(ESC2,1100)
        time.sleep(0.5)
        pi.write(relay_left1, 0)
        pi.write(relay_left2, 0)
        pi.write(relay_right1, 0)
        pi.write(relay_right2, 0)
        pi.set_servo_pulsewidth(ESC1, speed)
        pi.set_servo_pulsewidth(ESC2, speed)
    else:
        pi.set_servo_pulsewidth(ESC1, speed)
        pi.set_servo_pulsewidth(ESC2, speed)


def move_backwards(pi, ESC1, ESC2, relay_left1, relay_left2, relay_right1, relay_right2, speed):
    """
    funciton will rotate both motors at equal speed in reverse

    """
    if pi.read(relay_left1) or pi.read(relay_left2) or pi.read(relay_right1) or pi.read(relay_right2)== 0:
        pi.set_servo_pulsewidth(ESC1,1100)
        pi.set_servo_pulsewidth(ESC2,1100)
        time.sleep(0.5)
        pi.write(relay_left1, 1)
        pi.write(relay_left2, 1)
        pi.write(relay_right1, 1)
        pi.write(relay_right2, 1)
        pi.set_servo_pulsewidth(ESC1, speed)
        pi.set_servo_pulsewidth(ESC2, speed)
    else:
        pi.set_servo_pulsewidth(ESC1, speed)
        pi.set_servo_pulsewidth(ESC2, speed)


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


def spin_clockwise(pi, ESC1, ESC2, relay_left1, relay_left2, relay_right1, relay_right2, speed, idle):
    """
    funciton will rotate both motors at equal speed in opposite directions creating
    a clockwise rotation
    """
    pi.set_servo_pulsewidth(ESC1,idle)
    pi.set_servo_pulsewidth(ESC2,idle)
    time.sleep(0.5)
    pi.write(relay_left1, 0)
    pi.write(relay_left2, 0)
    pi.write(relay_right1, 1)
    pi.write(relay_right2, 1)
    pi.set_servo_pulsewidth(ESC1, speed)
    pi.set_servo_pulsewidth(ESC2, speed)


def spin_anticlockwise(pi, ESC1, ESC2, relay_left1, relay_left2, relay_right1, relay_right2, speed, idle):
    """
    will spin the robot in an anticlockwise direction
    """
    pi.set_servo_pulsewidth(ESC1,idle)
    pi.set_servo_pulsewidth(ESC2,idle)
    time.sleep(0.5)
    pi.write(relay_left1, 1)
    pi.write(relay_left2, 1)
    pi.write(relay_right1, 0)
    pi.write(relay_right2, 0)
    pi.set_servo_pulsewidth(ESC1, speed)
    pi.set_servo_pulsewidth(ESC2, speed)

    
def pre_planned(pi, ESC1, ESC2, relay_left1, relay_left2, relay_right1, relay_right2, speed, idle):
    """
    executes the movement functions for a set movement output
    as an example:
    """
    move_forward(pi, ESC1, ESC2, relay_left1, relay_left2, relay_right1, relay_right2, speed)
    time.sleep(4)
    #turn_left(pi, ESC1, ESC2, speed, idle)
    #time.sleep(2)
    #turn_right(pi, ESC1, ESC2, speed, idle)
    #time.sleep(2)
    spin_clockwise(pi, ESC1, ESC2, relay_left1, relay_left2, relay_right1, relay_right2, speed, idle)
    time.sleep(2)
    #spin_anticlockwise(pi, ESC1, ESC2, relay_left1, relay_left2, relay_right1, relay_right2, speed, idle)
    #time.sleep(4)
    #move_backwards(pi, ESC1, ESC2, relay_left1, relay_left2, relay_right1, relay_right2, speed)
    #time.sleep(3)
    #move_forward(pi, ESC1, ESC2, relay_left1, relay_left2, relay_right1, relay_right2, speed)
    #time.sleep(2)
    stop(pi, ESC1, ESC2, idle)


# DEBUGGING FUNCTONS
# these only operate the ESC at the same time

def manual_drive(pi, ESC1, ESC2, idle): 
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
            stop(pi, ESC1, ESC2, idle)
            break
        elif inp == ("kill"): #kill statement
            kill(pi, ESC1, ESC2)
            break           #safety feature, really
        elif int(inp) > max_value :
            print("value must be smaller than", max_value)
        else:
            pi.set_servo_pulsewidth(ESC1,inp)
            pi.set_servo_pulsewidth(ESC2,inp)
    
def control(pi, ESC1, ESC2, speed, idle):
    """
    This mode allows for incrimental stepping PWM control of the motor
    """
    time.sleep(1)
    print("Controls - w to decrease speed & s to increase speed OR q to decrease a lot of speed & e to increase a lot of speed, or x to kill")
    speed = 1150
    while True:   #the while loop will ask for a speed change
        pi.set_servo_pulsewidth(ESC1, speed)
        pi.set_servo_pulsewidth(ESC2, speed)
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
            pi.set_servo_pulsewidth(ESC2,idle)
            break
        elif inp == ("x"):
            kill(pi, ESC1, ESC2)
            break           #safety feature, really
        else:
            print("WHAT DID I SAY!! Press w,s,q,e or x")


# STOP FUNCITONS

def kill(pi, ESC1, ESC2):
    """
    kill will end all signals from the pi.
    """
    print("You have killed the program and will have to restart.")
    pi.set_servo_pulsewidth(ESC1, 0)
    pi.set_servo_pulsewidth(ESC2, 0)
    pi.stop()


def stop(pi, ESC1, ESC2, idle):
    """
    function will hault both the motors, bringing Robotug to a stop.
    """
    pi.set_servo_pulsewidth(ESC1,idle)
    pi.set_servo_pulsewidth(ESC2,idle)


if __name__ == "__main__":
    import pigpio
    import time
    import keyboard

    ESC1 = 17      # pigpio uses BCM gpio numbering
    ESC2 = 16  

    rpm_left = 18       # gpio pins for the rpm signal from esc
    rpm_right = 13

    relay_left_ch1 = 27 
    relay_left_ch2 = 22

    relay_right_ch1 = 23     # ***might be worth putting the gpio on a breadboard that way these can share pin slots.
    relay_right_ch2 = 24

    pi = pigpio.pi()        #Initialise Pi connection

    pi.write(relay_right_ch1, 0)  #set pins to low, default forward
    pi.write(relay_right_ch2, 0)

    pi.write(relay_left_ch1, 0)  #set pins to low, default forward
    pi.write(relay_left_ch2, 0)

    zero_throttle = 0
    max_throttle = 1900     # ***this is a crazy fast speed on these motors and should be altered
    half_throttle = max_throttle/2 
    idle_throttle = 1100  
    low_throttle = 1150 
    
    inp = input("arm, yes or no: ")
    if inp == ("yes"):
        pi.set_servo_pulsewidth(ESC1,zero_throttle)
        pi.set_servo_pulsewidth(ESC2,zero_throttle)    # sends the throttle puslewidth signal to the esc and thus the motor
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC1, max_throttle)
        pi.set_servo_pulsewidth(ESC2, max_throttle)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC1, idle_throttle)
        pi.set_servo_pulsewidth(ESC2, idle_throttle)
        time.sleep(2)
    elif inp == ("no"):
        pass

    inp2 = input()
    if inp2 == (""):
        pre_planned(pi, ESC1, ESC2, relay_left_ch1, relay_left_ch2, relay_right_ch1, relay_right_ch2, low_throttle, idle_throttle)