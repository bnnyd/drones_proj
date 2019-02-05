#!/usr/bin/env python3
import socket
from General.general_common import States
from .control_common import AxisIndex
from Camera.camera import Camera
#from auto_hover import find_direction
from .auto_hover import AutoHover
from .imageProcessing import ImageProcessing





class CommandCenter():
    def __init__(self):
        self.UDP_IP = "172.16.10.1" # TODO: read these values from config file
        self.UDP_PORT = 8080
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP

    def __send_to_drone(self, up_down, rotate, forward_backwards, left_right, byte6, byte7, byte8, byte9):
        command = bytearray([255, 8, up_down, rotate, forward_backwards, left_right, byte6, byte7, byte8, byte9])
        command.extend([255 - sum(command[1:]) % 256])  # check sum
        self.sock.sendto(command, (self.UDP_IP, self.UDP_PORT))

    def perform_action(self, state, my_joystick):
        my_camera = Camera()
        cX = 0
        cY = 0
        if state == States.IDLE:
            self.__send_to_drone(0, 63, 64, 63, 144, 16, 16, 0)  # stand by

        elif state == States.STAND_BY:
            self.__send_to_drone(126, 63, 64, 63, 144, 16, 16, 64)  # start engines

        elif state == States.HOVERING:
        #    self.__send_to_drone(126, 63, 64, 63, 144, 16, 16, 0)  #
            img = my_camera.get_RGB_image()
            cX, cY, xlen, ylen, clean_im = ImageProcessing.object_center(img)

            #my_hover = AutoHover()
            x, y = AutoHover.find_direction([cX, cY], [xlen, ylen])
            forward_backwards, left_right = AutoHover.engine_power(x,y,[xlen, ylen])
            #print(forward_backwards, left_right)
            self.__send_to_drone(126, 63, forward_backwards, left_right, 144, 16, 16, 0)



        #move = find_direction([200, 200], [320, 320])

        elif state == States.LANDING:
            self.__send_to_drone(40, 63, 64, 63, 144, 16, 16, 0)  #
            print("landing")
        elif state == States.STOP or state == States.STOP_BEFORE_EXIT:
            self.__send_to_drone(126, 63, 64, 63, 144, 16, 16, 160)  # stop
        elif state == States.MANUAL_CONTROL:
            up_down = 126 + int(-1 * my_joystick.get_axis_val(AxisIndex.UP_DOWN) * 126)
            left_right = 63 + int(my_joystick.get_axis_val(AxisIndex.LEFT_RIGHT) * 63)
            rotate = 63 + int(my_joystick.get_axis_val(AxisIndex.ROTATE) * 63)
            forward_backwards = 64 + int(my_joystick.get_axis_val(AxisIndex.FORWARD_BACKWARDS) * 63)      #check
            self.__send_to_drone(up_down, rotate, forward_backwards, left_right, 144, 16, 16, 0)
        return cX, cY

    @staticmethod
    def __byte9(mSpeedValue, m360RollValue, mNoHeadValue, mStopValue, mToflyValue, mToLandValue):
        return mSpeedValue | m360RollValue << 2 | mNoHeadValue << 4 | mStopValue << 5 | mToflyValue << 6 | mToLandValue << 7