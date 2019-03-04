#!/usr/bin/env python3
import cv2
import time

from General.state_machine import getState
from General.general_common import States
from General.gui import Screen

from Control.joystick import Joystick
from Control.command_center import CommandCenter

from Camera.camera import Camera
counter = 0
my_joystick = Joystick(0.1,0.1,0.2,0.1) # TODO: read these values from the config file
my_camera = Camera()
my_command_center = CommandCenter()
my_screen = Screen()
state=States.IDLE

#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#video = cv2.VideoWriter('flight.avi', fourcc, 20.0, (1280, 720))

while state != States.EXIT:
    my_joystick.refresh()
    state = getState(state, my_joystick)
    image = my_camera.get_RGB_image()
    cX , cY = my_command_center.perform_action(state, my_joystick=my_joystick,img=image)



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
    #counter = counter + 1
    #if counter % 100 == 0:
    my_camera.update_RGB_image()
     #   counter = 1
    #video.write(image)

    my_camera.update_RGB_image()
    my_screen.update_state(state)
    my_joystick.update_values()

#video.release()
cv2.destroyAllWindows()
