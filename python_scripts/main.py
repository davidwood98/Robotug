# author David Wood 
# date 19/11/2020   

# ***This code is for use by Quantuam Leap Technologies Ltd only***
# ***To use this code please get permission from the author***

launch_message = """
FIRSTLY - prior to running this script makes sure to activate the pigpio daemon by running 'sudo pigpiod' in the Rpi terminal.

SECONDLY - make sure to run the script from the terminal as a sudo launch: 'sudo python3 main.py' otherwise there will be errors.
"""
print(launch_message, "\n")
print("*" * 10, "\n")

# IMPORTS
import time 
import pigpio
import keyboard   # this module is the reason you need to run script as a sudo permission
import read_PWM
import motor 

# SET-UP
ESC1 = 27      # pigpio uses BCM gpio numbering
ESC2 = 13  
ESC_both = [27, 13]   # list to give motors same command

relay_left_ch1 = 23 
relay_left_ch2 = 22
both_relay_left = [23, 22]      # list to swap direction of the motor

relay_right_ch1 = 24     # ***might be worth putting the gpio on a breadboard that way these can share pin slots.
relay_right_ch2 = 25
both_relay_right = [24, 25]
all_relays = [23, 22, 24, 25]

pi = pigpio.pi()        #Initialise Pi connection

zero_throttle = 0
max_throttle = 1900     # ***this is a crazy fast speed on these motors and should be altered
half_throttle = max_throttle/2 
idle_throttle = 1100  
low_throttle = 1150     # slowest consistent motor launch speed from testing - can be taken down to 1040 after initial spin up

# INITIAL ASK
boot_msg = """Welcome to the Robotug drive program. 

Please ensure you have calibrated the ESCs before running this program!
\n"""
print(boot_msg) 

startup_inp = input("Is this a cold start?: ")
if startup_inp == ("yes"):      # The ESCs need arming when first powered on
    print("Arming the ESCs")
    pi.set_servo_pulsewidth(ESC_both,zero_throttle)
    time.sleep(2)
    pi.set_servo_pulsewidth(ESC_both, max_throttle)
    time.sleep(2)
    pi.set_servo_pulsewidth(ESC_both, idle_throttle)
    time.sleep(2)
    print("Ready for operation")

else:
    print("Ready for operation")
    pi.set_servo_pulsewidth(ESC_both, idle_throttle)
    time.sleep(1)

