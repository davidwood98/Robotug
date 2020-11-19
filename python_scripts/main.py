#
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
ESC2 = 19  
ESC_both = [27, 19]   # list to give motors same command

rpm_left = 18       # gpio pins for the rpm signal from esc
rpm_right = 13

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


#PHYSICAL VALUES
wheel_radius = 0.0605       # ***makes sure this is up to date
reduction_ratio = 9


# INITIAL ASK
boot_msg = """Welcome to the Robotug drive program. 

Please ensure you have calibrated the ESCs before running this program!
\n"""
print(boot_msg) 

startup_inp = input("Is this a cold start?: ")
if startup_inp == ("yes"):      # The ESCs need arming when first powered on
    print("Arming the ESCs")

    pi.set_servo_pulsewidth(ESC_both,zero_throttle)    # sends the throttle puslewidth signal to the esc and thus the motor
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

# FUNCTIONS
def motor_rpm(pi, rpm_gpio):
    """
    will return the specified motor rpm
    """
    p = read_PWM.Reader(pi, rpm_gpio)
    
    f = p.frequency()

    rpm = (f * 5.645161)        # 5.645161 was a linear relationship value found from experiment

    return rpm

def vehicle_speed(pi, rpm_gpio, r, gear_ratio):
    """
    will calculate the speed of the tug
    """ 
    wheel_rpm = motor_rpm(pi, rpm_gpio) / gear_ratio

    omega = wheel_rpm / 60

    v = omega * r

    return v


# MAIN CODE
print("""\nSelect a programme you'd like to operate in. The options are:

move OR debug OR 'x' to cancel\n""", "*" * 20, "\n")

while True:
    mode_select = input("Please select a mode: ")
    if mode_select == ("move"):         # enters keyboard control
        print("*" * 20)
        movement_select = input("remote control or preplanned?: ")
        print("*" * 20)
        if movement_select == ("remote control"): 
            print("\nControls are the arrow keys - 'ctrl + right(left)' to spin - 'ctrl + x' to break ")
            while keyboard.KEY_DOWN:
                if keyboard.is_pressed("up"):       # the keyboard press and hold for moving forward 
                    print("moving forward")
                    motor.move_forward(pi, ESC_both, both_relay_left, both_relay_right, all_relays, low_throttle)
                elif keyboard.is_pressed("down"):
                    motor.move_backwards(pi, ESC_both, both_relay_left, both_relay_right, all_relays, low_throttle)
                    print("moving back")
                elif keyboard.is_pressed("left"):
                    motor.turn_left(pi, ESC1, ESC2, low_throttle, idle_throttle)
                    print("turning left")
                elif keyboard.is_pressed("right"):
                    motor.turn_right(pi, ESC1, ESC2, low_throttle, idle_throttle)
                    print("turning right")
                elif keyboard.is_pressed("ctrl + right"):
                    motor.spin_clockwise(pi, ESC_both, both_relay_left, both_relay_right, low_throttle, idle_throttle)
                    print("spinning clockwise")
                elif keyboard.is_pressed("ctrl + left"):
                    motor.spin_anticlockwise(pi, ESC_both, both_relay_left, both_relay_right, low_throttle, idle_throttle)
                    print("spinning anticlockwise")
                elif keyboard.is_pressed("ctrl + x"):       # will only break one layer
                    break
                else:
                    motor.stop(pi, ESC_both, idle_throttle)     # if a key is released then the robot stops
                    print("stopped")
        
        elif movement_select == ("preplanned"):     # this set of instructions can be edited in motor.py
            print("\nA pre selected set of moves will now be executed")
            time.sleep(1)
            motor.pre_planned(pi,ESC_both, ESC1, ESC2, both_relay_left, both_relay_right, all_relays, low_throttle, idle_throttle)
    
    elif mode_select == ("debug"):
        print("*" * 20)
        debug_select = input("input or stepped?: ")
        print("*" * 20)
        if debug_select == ("input"):
            motor.manual_drive(pi, ESC1, idle_throttle)
        elif debug_select == ("stepped"):
            motor.control(pi, ESC1, low_throttle, idle_throttle)
    
    elif mode_select == ("x"):
        break
    
    time.sleep(0.3)    # small pause before re-asking for a mode.


#CLEAN UP 
motor.kill(pi, ESC_both)

pi.stop()
