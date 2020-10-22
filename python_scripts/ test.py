import keyboard
import time
while keyboard.KEY_DOWN:
    if keyboard.is_pressed("up"):
        print("moving forward")
    if keyboard.is_pressed("down"):
        print("moving back")
    if keyboard.is_pressed("left"):
        print("turning left")
    if keyboard.is_pressed("right"):
        print("turning right")
    if keyboard.is_pressed("space + x"):
        break
"""else:
    print("haulted")"""
