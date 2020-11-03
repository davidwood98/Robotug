import keyboard
import time
import os
import pigpio

pi = pigpio.pi()
ESC_1 = 27
pi.write(22, 1)
pi.write(23, 1)

pi.set_servo_pulsewidth(ESC_1,0)
time.sleep(2)
pi.set_servo_pulsewidth(ESC_1, 1900)
time.sleep(2)
pi.set_servo_pulsewidth(ESC_1, 1100)
time.sleep(1)
pi.set_servo_pulsewidth(ESC_1, 1190)
time.sleep(5)
pi.set_servo_pulsewidth(ESC_1, 0)
time.sleep(2)
pi.write(22, 0)
pi.write(23, 0)
time.sleep(1)
pi.set_servo_pulsewidth(ESC_1, 1190)
time.sleep(5)
pi.set_servo_pulsewidth(ESC_1, 1100)



pi.stop()

