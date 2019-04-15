#!/usr/env python3
import cv2
import numpy as np


def linesDirection(image):
    # Salt and Pepper noise removal
    img = cv2.medianBlur(image,5)

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,bw = cv2.threshold(gray, 200, 225, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(bw,2,1)

    try:
        cnt = contours[0]
    except IndexError:
        return 0,0

    rows, cols = img.shape[:2]
    [vx, vy, x, y] = cv2.fitLine(cnt, cv2.DIST_L2, 0, 0.01, 0.01)

    # a general line equation: y = m*x + q
    # x and y are the coordinates of a point on the line.
    # vx and vy are the x and y components of a vector parallel to the line

    m = vy/vx
    #lefty = int((-x * vy / vx) + y)
    # the point in which the line crosses the y axes (x=0), = q
    lefty = int((-x * m) + y)
    #righty = int(((cols - x) * vy / vx) + y)
    # the point in which the line crosses the line (x=x_max)
    righty = int(((cols - x) * m) + y)

    # the perpendicular line passing from the center of the pic will be: y - rows/2 = -(1/m)*(x - cols/2)
    # TODO: m = 0
    m_p = -1/m
    y_p = int(rows/2)
    x_p = int(cols/2)
    lefty_p = int((-x_p * m_p) + y_p)
    righty_p = int(((cols - x_p) * m_p) + y_p)


    # find the crossing point of the two lines
    x0 = int(-(lefty - lefty_p) / (m - m_p))
    y0 = int(m_p * x0 + lefty_p)



    if righty_p < -30000 or lefty_p > 30000:
        #print("large numbers")
        return 0,0

    # the minus is to make the y axis upwards, angle is calculated counterclockwise
    line_ang = -np.rad2deg(np.arctan(m))
    if line_ang < 0:
        line_ang = line_ang + 180

    return x0, y0, m
