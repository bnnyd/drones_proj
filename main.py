#!/usr/bin/env python3
import cv2
import os
import time

from General.state_machine import getState
from General.general_common import States
from General.gui import Screen

from Control.joystick import Joystick
from Control.command_center import CommandCenter
import logging
#from run_me import logger
import shutil
from Camera.camera import Camera
#from scratch_joystick import scratch

counter = 0
left_right_clip_val = 0.1
forward_backwards_clip_val = 0.1
rotate_clip_val = 0.2
up_down_clip_val = 0.1

my_joystick = Joystick(left_right_clip_val,forward_backwards_clip_val,rotate_clip_val,up_down_clip_val) # TODO: read these values from the config file

my_camera = Camera()
my_command_center = CommandCenter()
my_screen = Screen()
state=States.IDLE
cnt = 0         #change

# remove the directory where images of previous run are saved
#path = './' + str(my_camera.IMAGE_DIR)
#if os.path.exists(path):
 #   shutil.rmtree(path)



while state != States.EXIT:
    my_joystick.refresh()
    state = getState(state, my_joystick, cnt)    #change
    cX, cY = my_command_center.perform_action(state, my_joystick=my_joystick)

    if state == States.LANDING:      #change
        cnt = cnt + 1
        print(cnt)                 #change
    if state == States.IDLE:
        cnt = 0
    #time.sleep(0.1)
    #scratch()
    image = my_camera.get_RGB_image()
    if state==States.HOVERING:
        if cX == 2000:
            cv2.putText(image, "Empty dir", (640, 360), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        elif cX == 3000:
            cv2.putText(image, "No objects", (640, 360), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        elif cX == 4000:
            cv2.putText(image, "Too many objects", (640, 360), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        else:
            cX = int(cX)
            cY = int(cY)
            cv2.circle(image, (cX, cY), 5, (255, 255, 255), -1)
            cv2.putText(image, "centroid", (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.imshow("video", image)
    cv2.waitKey(1)
    counter = counter + 1
    if counter % 100 == 0:
        my_camera.update_RGB_image()
        counter = 1
    my_screen.update_state(state)
    my_joystick.update_values()

cv2.destroyAllWindows()