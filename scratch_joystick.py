#!/usr/bin/env python3

import pygame
import cv2
import time
#import pygame.joystick
import sys
class scratch():
     def __init__(self):
        pygame.init()
        pygame.joystick.init()
        print("I am here")
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print(joystick)

        buttons = False

        for i in range(1):
            pygame.event.get()
            if (buttons):
                x = joystick.get_button(3)
                y = joystick.get_button(4)
                z = joystick.get_button(5)
                pr = "printing "
                trigger = "three "
                exit = "four "
                b1 = "five "
                print(pr + trigger + str(x))
                print(pr + b1 + str(y))
                print(pr + exit + str(z))
                print(" ")
            rl = "right-left: "
            bf = "back-forward: "
            rt = "rotation: "
            ud = "up-down: "
            if (1):
                if(joystick.get_axis(0)):
                    print(rl + str(joystick.get_axis(0)))
                if(joystick.get_axis(1)):
                    print(bf + str(joystick.get_axis(1)))
                if(joystick.get_axis(2)):
                    print(rt + str(joystick.get_axis(2)))
                if(joystick.get_axis(3)):
                    print(ud + str(joystick.get_axis(3)))
                print(" ")
            time.sleep(0.1)

