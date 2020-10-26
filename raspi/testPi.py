from time import sleep #importing sleep from time library to call directly
import os                #importing the os so as to communicate with the system
os.system ("sudo pigiod")  #launching the GPIO library
sleep(1) # Gives time for the system to process
import pigpio

"""
Code for 1 motor and ESC.
"""

ESC = 27 #'GPIO pin number' #Connect the ESC in a GPIO pin eg 4

pi = pigpio.pi()  #Initialise Pi connection
pi.set_servo_pulsewidth(ESC, 0)  #Sets all PWM traffic to 0
sleep(1)
pi.set_servo_pulsewidth(ESC, 1140)
max_value = 2500 #Standard maximum pwm signal for the ESC to motor
                 #change this if ESC's max value is different or leave it be
min_value = 500  #Standard minimum pwm signal for the ESC to motor
                 #change this if ESC's min value is different or leave it be

rpm_in = 22
pi.set_mode(rpm_in, pigpio.INPUT)  # setting the gpio pin of the rpm to be an input

def read_gpio():
    """
    docstring
    """
    gpio_value = pi.read(rpm_in)
    print(gpio_value)

def print_rpm():
    """
    docstring
    """
    print(rpm_in)

#Program

inp = input()

if inp == ("gpio"):
    read_gpio
elif inp == ("read"):
        print_rpm()



