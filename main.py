#!/usr/bin/env python3

import cv2
import time
import numpy as np
from General.state_machine import getState
from General.general_common import States
from General.gui import Screen

from Control.joystick import Joystick
from Control.command_center import CommandCenter
from Control.lines_dir import linesDirection
from Control.line_control import linesControl

from Camera.camera import Camera
my_joystick = Joystick(0.1,0.1,0.2,0.1) # TODO: read these values from the config file
my_camera = Camera()
my_command_center = CommandCenter()
my_screen = Screen()
state = States.IDLE

#==== Possibilty to save video
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#video = cv2.VideoWriter('flight.avi', fourcc, 20.0, (1280, 720))
#==============================


image = my_camera.get_RGB_image()

cX = 0
cY = 0

init = 0
while state != States.EXIT:
    my_joystick.refresh()
    state = getState(state, my_joystick)
    image_big = my_camera.get_RGB_image()

    if state == States.EXIT or state == States.STOP_BEFORE_EXIT:
        print("exit")
        init = 0

    if state == States.AUTO:
        state = States.IDLE
        init = time.time()

    end = time.time()
    interval = end - init

    if init > 0:
        if 1 < interval and interval < 2:
            state = States.STAND_BY
            print("stand by")
        elif 2 < interval and interval < 4:
            state = States.UP
            print("Up")
        elif 4 < interval and interval <6:
            state = States.LINE
            print("line")
        elif 6 < interval and interval <8.5:
            state = States.DOWN
            print("down")
        elif 8.5 < interval:
            state = States.STOP_BEFORE_EXIT
            print("stop before exit")


    heigth, width, depth = image_big.shape
    factor = 0.3
    image = cv2.resize(image_big, (int(factor * width), int(factor * heigth)))

    cX, cY, x, y = my_command_center.perform_action(state, my_joystick=my_joystick, img=image)







    #if state is line, print on the screen power and direction
    if state == States.LINE:
        text = "x= " + str(cX) + ", y= " + str(cY)
        cv2.circle(image, (int(x), int(y)), 5, (0,0,255))
        cv2.putText(image, text, (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow("video", image)
    cv2.waitKey(1)

    #===saving video
    #video.write(image)
    #=================

    my_camera.update_RGB_image()
    my_camera.update_RGB_image()
    my_camera.update_RGB_image()
    my_screen.update_state(state)
    my_joystick.update_values()

#=====Release video
#video.release()
#=================
cv2.destroyAllWindows()
