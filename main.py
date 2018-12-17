#!/usr/bin/env python3
import cv2
import time

from General.state_machine import getState
from General.general_common import States
from General.gui import Screen

from Control.joystick import Joystick
from Control.command_center import CommandCenter
import logging
#from run_me import logger

#from Camera.camera import Camera
#from scratch_joystick import scratch


left_right_clip_val = 0.1
forward_backwards_clip_val = 0.1
rotate_clip_val = 0.2
up_down_clip_val = 0.1

my_joystick = Joystick(left_right_clip_val,forward_backwards_clip_val,rotate_clip_val,up_down_clip_val) # TODO: read these values from the config file

#logger.error('bbbbb')
#logger.critical('aaa')

#my_camera = Camera()
my_command_center = CommandCenter()
my_screen = Screen()
state=States.IDLE
cnt = 0         #change

while state != States.EXIT:
    my_joystick.refresh()
    state = getState(state, my_joystick, cnt)    #change
    my_command_center.perform_action(state, my_joystick=my_joystick)
    if state == States.LANDING:      #change
        cnt = cnt + 1
        print(cnt)                 #change
    if state == States.IDLE:
        cnt = 0
    #time.sleep(0.1)
    #scratch()
    #image = my_camera.get_RGB_image()
   # cv2.imshow("video", image)
    #cv2.waitKey(1)
    #my_camera.update_RGB_image()
    my_screen.update_state(state)
    my_joystick.update_values()

cv2.destroyAllWindows()
