import keyboard
import time
import os
import pigpio

pi = pigpio.pi()
gpio_list = (22,23)

pi.write(gpio_list, True)

