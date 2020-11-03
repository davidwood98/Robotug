import keyboard
import time
import os
import pigpio

pi = pigpio.pi()

pi.write(22, 1)
pi.write(23, 1)

