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
low_throttle = 1150     # slowest consistent motor launch speed from testing - can be taken down to 1040 after initial spin up

PORT_NAME = "/dev/ttyUSB0" #Lidar initiation - ** pi is tempermental with setting up ttyUSB - best to use USB 2.0 ports
lidar = RPLidar(PORT_NAME)


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

    pi.set_servo_pulsewidth(ESC1,zero_throttle)
    pi.set_servo_pulsewidth(ESC2,zero_throttle)    # sends the throttle puslewidth signal to the esc and thus the motor
    time.sleep(1)
    pi.set_servo_pulsewidth(ESC1, max_throttle)
    pi.set_servo_pulsewidth(ESC2, max_throttle)
    time.sleep(1)
    pi.set_servo_pulsewidth(ESC1, idle_throttle)
    pi.set_servo_pulsewidth(ESC2, idle_throttle)
    time.sleep(2)

    print("Ready for operation")

else:
    print("Ready for operation")
    
    pi.set_servo_pulsewidth(ESC1, idle_throttle)
    pi.set_servo_pulsewidth(ESC2, idle_throttle)
    time.sleep(1)

# FUNCTIONS
def dual_motorstop():
    """
    stops both motors
    """
    pi.set_servo_pulsewidth(ESC1, idle_throttle)
    pi.set_servo_pulsewidth(ESC2, idle_throttle)

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

def collision_avoid():
    """
    predetermined moves to miss obsticle
    """
    dual_motorstop()
    motor.spin_anticlockwise(pi, ESC1, ESC2, relay_left_ch1, relay_left_ch2, relay_right_ch1, relay_right_ch2, low_throttle, idle_throttle)
    time.sleep(2)
    dual_motorstop()

def collision_detection():
    """
    monitors distance to obsticles
    """
    print("*" * 20)
    print("\nhit 'x' to kill operation\n")
    print("*" * 20)
    motor.move_forward(pi, ESC1, ESC2, relay_left_ch1, relay_left_ch2, relay_right_ch1, relay_right_ch2, low_throttle)
    for scan in lidar.iter_scans():
        if len(scan) > 50:
            for (quality, angle, distance) in scan:
                if angle in range (135, 225) and distance < 170:
                        print("collision detected")
                        collision_avoid()
                        break
                        
                   


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
                    motor.move_forward(pi, ESC1, ESC2, relay_left_ch1, relay_left_ch2, relay_right_ch1, relay_right_ch2, low_throttle)
                elif keyboard.is_pressed("down"):
                    motor.move_backwards(pi, ESC1, ESC2, relay_left_ch1, relay_left_ch2, relay_right_ch1, relay_right_ch2, low_throttle)
                    print("moving back")
                elif keyboard.is_pressed("left"):
                    motor.turn_left(pi, ESC1, ESC2, low_throttle, idle_throttle)
                    print("turning left")
                elif keyboard.is_pressed("right"):
                    motor.turn_right(pi, ESC1, ESC2, low_throttle, idle_throttle)
                    print("turning right")
                elif keyboard.is_pressed("a"):
                    motor.spin_clockwise(pi, ESC1, ESC2, relay_left_ch1, relay_left_ch2, relay_right_ch1, relay_right_ch2, low_throttle, idle_throttle)
                    print("spinning clockwise")
                elif keyboard.is_pressed("d"):
                    motor.spin_anticlockwise(pi, ESC1, ESC2, relay_left_ch1, relay_left_ch2, relay_right_ch1, relay_right_ch2, low_throttle, idle_throttle)
                    print("spinning anticlockwise")
                elif keyboard.is_pressed("ctrl + x"):       # will only break one layer
                    break
        
                else:
                    time.sleep(0.5)
                    motor.stop(pi, ESC1, ESC2, idle_throttle)     # if a key is released then the robot stops
                    print("stopped")
        
        elif movement_select == ("preplanned"):     # this set of instructions can be edited in motor.py
            print("\nA pre selected set of moves will now be executed")
            time.sleep(1)
            motor.pre_planned(pi,ESC1, ESC2, relay_left_ch1, relay_left_ch2, relay_right_ch1, relay_right_ch2, low_throttle, idle_throttle)
    
    elif mode_select == ("debug"):
        print("*" * 20)
        debug_select = input("input or stepped?: ")
        print("*" * 20)
        if debug_select == ("input"):
            motor.manual_drive(pi, ESC1, ESC2, idle_throttle)
        elif debug_select == ("stepped"):
            motor.control(pi, ESC1, ESC2, low_throttle, idle_throttle)
    
    elif mode_select == ("x"):
        break
    
    time.sleep(0.3)    # small pause before re-asking for a mode.


#CLEAN UP 
motor.kill(pi, ESC1, ESC2)

pi.stop()
