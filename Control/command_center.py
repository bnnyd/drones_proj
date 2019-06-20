#!/usr/bin/env python3
import socket
import time
import numpy as np
from General.general_common import States
from .control_common import AxisIndex, ThresHold, NoObj
from Camera.camera import Camera
from Control.lines_dir import linesDirection
from Control.line_control import linesControl


class CommandCenter():
    def __init__(self):
        self.UDP_IP = "172.16.10.1" # TODO: read these values from config file
        self.UDP_PORT = 8080
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
        self.prev_time = time.time()
        self.prev_command_hash = 0

    def __send_to_drone(self, up_down, rotate, forward_backwards, left_right, byte6, byte7, byte8, byte9):
        current_time = time.time()
        current_command_hash = hash((up_down, rotate, forward_backwards, left_right))
        # we will send a massage if:
        # 1) it has been ThresHold.SENDING_TIME seconds from the last message
        # 2) the new message is not as the one sent before
        if (current_time - self.prev_time) > ThresHold.SENDING_TIME or current_command_hash != self.prev_command_hash:
            command = bytearray([255, 8, up_down, rotate, forward_backwards, left_right, byte6, byte7, byte8, byte9])
            command.extend([255 - sum(command[1:]) % 256])  # check sum
            self.sock.sendto(command, (self.UDP_IP, self.UDP_PORT))
            self.prev_time = current_time
            self.prev_command_hash = current_command_hash

    def perform_action(self, state, my_joystick, img):

        cX = 0
        cY = 0
        x = 0
        y = 0

        if state == States.IDLE:
            self.__send_to_drone(0, 63, 64, 63, 144, 16, 16, 0)  # stand by

        elif state == States.STAND_BY:
            self.__send_to_drone(126, 63, 64, 63, 144, 16, 16, 64)  # start engines

        elif state == States.MANUAL_CONTROL:
            up_down = 126 + int(-1 * my_joystick.get_axis_val(AxisIndex.UP_DOWN) * 126)
            rotate = 63 + int(my_joystick.get_axis_val(AxisIndex.ROTATE) * 63)
            forward_backwards = 64 + int(my_joystick.get_axis_val(AxisIndex.FORWARD_BACKWARDS) * 63)
            left_right = 63 + int(my_joystick.get_axis_val(AxisIndex.LEFT_RIGHT) * 63)
            self.__send_to_drone(up_down, rotate, forward_backwards, left_right, 144, 16, 16, 0)

        elif state == States.HOVERING:
            forward_backwards = 64
            left_right = 63
            self.__send_to_drone(126, 63, forward_backwards, left_right, 144, 16, 16, 0)

        elif state == States.LINE:
            # x0,y0 is the point on the line and on the perpendicular from the center of the image, m is: y = m*x + q, angle is the direction of the line
            x0, y0, angle = linesDirection(img)
            rows, cols = img.shape[:2]
            forward_backwards, left_right = linesControl(x0, y0, angle,rows, cols)
            self.__send_to_drone(160, 63, forward_backwards, left_right, 144, 16, 16, 0)
            cY = - forward_backwards + 64
            cX = left_right - 63
            x = x0
            y = y0

        elif state == States.LEFT:
            self.__send_to_drone(160, 63, 64, 50, 144, 16, 16, 0)

        elif state == States.RIGHT:
            self.__send_to_drone(160, 63, 64, 75, 144, 16, 16, 0)

        elif state == States.FRW:
            self.__send_to_drone(160, 63, 50, 63, 144, 16, 16, 0)

        elif state == States.BCK:
            self.__send_to_drone(160, 63, 75, 63, 144, 16, 16, 0)

        elif state == States.UP:
            self.__send_to_drone(200, 63, 64, 63, 144, 16, 16, 0)

        elif state == States.DOWN:
            self.__send_to_drone(50, 63, 70, 63, 144, 16, 16, 0)

        if state == States.STOP or state == States.STOP_BEFORE_EXIT:
            self.__send_to_drone(126, 63, 64, 63, 144, 16, 16, 160)
            self.__send_to_drone(126, 63, 64, 63, 144, 16, 16, 160)
            self.__send_to_drone(126, 63, 64, 63, 144, 16, 16, 160)# stop

        return cX, cY, x, y

    @staticmethod
    def __byte9(mSpeedValue, m360RollValue, mNoHeadValue, mStopValue, mToflyValue, mToLandValue):
        return mSpeedValue | m360RollValue << 2 | mNoHeadValue << 4 | mStopValue << 5 | mToflyValue << 6 | mToLandValue << 7