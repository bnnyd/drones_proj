#!/usr/bin/env python3
import cv2
import time
import numpy as np
from General.state_machine import getState
from General.general_common import States
from General.gui import Screen

from Control.joystick import Joystick
from Control.command_center import CommandCenter
#from Control.control_common import NoObj
#from Control.lineProcessing import LineProcessing
from Control.lines_dir import linesDirection
from Control.line_control import linesControl

from Camera.camera import Camera
my_joystick = Joystick(0.1,0.1,0.2,0.1) # TODO: read these values from the config file
my_camera = Camera()
my_command_center = CommandCenter()
my_screen = Screen()
state = States.IDLE

#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#video = cv2.VideoWriter('flight.avi', fourcc, 20.0, (1280, 720))

init = time.time()
image = my_camera.get_RGB_image()

while state != States.EXIT:
    my_joystick.refresh()
    state = getState(state, my_joystick)
    end = time.time()
    interval = end - init

    #if interval > 1:
    image_big = my_camera.get_RGB_image()
    heigth, width, depth = image_big.shape
    factor = 0.3
    image = cv2.resize(image_big,(int(factor*width), int(factor*heigth)))
    #init = time.time()

    cX, cY, x, y = my_command_center.perform_action(state, my_joystick=my_joystick,img=image)

    # if state == States.HOVERING:


    if state == States.LINE:
    #     ## inserted in my_command_center
    #     x0, y0, line_ang = linesDirection(image)
    #     rows, cols = image.shape[:2]
    #     xc = int(cols / 2)
    #     yc = int(rows / 2)
    #

    #     if x0==0 and y0==0 and line_ang==0:
    #         x_move =0; y_move=0
    #     else:
    #         x_move, y_move = linesControl(x0, y0, line_ang, rows, cols)
    #     #if lefty!=0 and righty!=0:
    #     #cv2.line(image, (cols - 1, righty), (0, lefty), (0, 255, 0), 2)
        text = "x= " + str(np.floor(cX)) + ", y= " + str(np.floor(cY))
        cv2.putText(image, text, (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    #     cv2.arrowedLine(image, (xc, yc), (xc + x_move, yc - y_move), (0, 0, 255), 3)
    cv2.imshow("video", image)
    cv2.waitKey(1)

    #video.write(image)


    my_camera.update_RGB_image()
    my_screen.update_state(state)
    my_joystick.update_values()

#video.release()
cv2.destroyAllWindows()
