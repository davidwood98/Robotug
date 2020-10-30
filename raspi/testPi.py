import pigpio
import time

esc = 27
pi = pigpio.pi()
pi.set_PWM_dutycycle(esc, 0)
pi.set_PWM_frequency(esc, 60)
pi.set_mode(esc, pigpio.OUTPUT)
pi.set_PWM_range(esc, 100)
pi.set_PWM_dutycycle(esc, 90)
time.sleep(2)
pi.set_PWM_dutycycle(esc, 50)
time.sleep(2)

while True:
    inp = input()
    pi.set_PWM_dutycycle(esc,inp)
    if inp == ("end"):
        pi.set_PWM_dutycycle(esc,40)
        break
    

