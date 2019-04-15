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
    #     if cX == NoObj.NO_OBJECT:
    #         cv2.putText(image, "No objects", (640, 360), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    #     else:
    #         cX = int(cX)
    #         cY = int(cY)
    #         cv2.circle(image, (cX, cY), 5, (255, 255, 255), -1)
    #  #       cv2.arrowedLine(image, (640,360), (640 + int(x), 360 + int(y)),(255,255,255),5)
    #         cv2.putText(image, "centroid", (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    if state == States.LINE:
        ## inserted in my_command_center
        dist, angle = linesDirection(image)
        rows, cols = image.shape[:2]
        #if lefty!=0 and righty!=0:
        #    cv2.line(image, (cols - 1, righty), (0, lefty), (0, 255, 0), 2)
        text = "dist " + str(np.floor(dist)) + ", angle " + str(np.floor(np.rad2deg(angle)))
        cv2.putText(image, text, (int(cols/2), int(rows/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.imshow("video", image)
    cv2.waitKey(1)

    #video.write(image)


    my_camera.update_RGB_image()
    my_screen.update_state(state)
    my_joystick.update_values()

#video.release()
cv2.destroyAllWindows()
