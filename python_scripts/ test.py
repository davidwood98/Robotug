import keyboard
import time
selected_mode = input()  #asking for an input from keyboard command

if selected_mode == ("control"):
    while keyboard.KEY_DOWN:
        if keyboard.is_pressed("up"):
            print("moving forward")
            #move_forward()
        if keyboard.is_pressed("down"):
            #move_backwards()
            print("moving back")
        if keyboard.is_pressed("left"):
            #turn_left()
            print("turning left")
        if keyboard.is_pressed("right"):
            #turn_right()
            print("turning right")
        if keyboard.is_pressed("ctrl + x"):
            break