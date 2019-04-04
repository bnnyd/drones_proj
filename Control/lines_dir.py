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
    lefty = int((-x * vy / vx) + y)
    righty = int(((cols - x) * vy / vx) + y)
    #if righty < -30000 or lefty > 30000:
    #    print("large numbers")
    #    return 0,0


    m = -vy/vx
    q = y - m*x

    ## angle in radians
    line_ang = np.arctan(m)
    if line_ang < 0 :
        line_ang = line_ang + np.pi

    ## distance from the center of the pic
    a = np.shape(bw)
    x_cent = a[1]/2
    y_cent = a[0]/2
    dist = abs(y_cent - (m*x_cent + q))/np.sqrt(1 + m**2)

    return dist,line_ang
