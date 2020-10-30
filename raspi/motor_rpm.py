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
sleep(2)

max_value = 1950 #Standard maximum pwm signal for the ESC to motor
                 #change this if ESC's max value is different or leave it be
min_value = 700  #Standard minimum pwm signal for the ESC to motor
                 #change this if ESC's min value is different or leave it be
rpm_in = 22
pi.set_mode(rpm_in, pigpio.INPUT)  # setting the gpio pin of the rpm to be an input
pi.set_pull_up_down(rpm_in,pigpio.PUD_DOWN) #setting the gpio pin to 0 - it reads 1 24/7 otherwise
rpm = pi.read(rpm_in)
print(rpm)

pi.set_servo_pulsewidth(ESC, 0)
sleep(2)     #little pause between settings to no ruin motor
pi.set_servo_pulsewidth(ESC, max_value)
sleep(2)
pi.set_servo_pulsewidth(ESC, min_value)
sleep(2)
print("the system is now armed")
sleep(2)
pi.set_servo_pulsewidth(ESC, 1140)


while True:
    print(rpm)
    pass




