#!/usr/bin/env python3
import cv2
import os

from imageProcessing import ImageProcessing


vidcap = cv2.VideoCapture('offline1.mp4')
success,image = vidcap.read()
rate = 25
cnt = 25
num = 0
while success:


    success,image2 = vidcap.read()

    if cnt==rate:
        image = image2
        cX, cY, xlen, ylen, pr_img = ImageProcessing.object_center(image)
        cnt = 0



    if cX == 2000:
        cv2.putText(image, "Empty dir", (640, 360), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    elif cX == 3000:
        cv2.putText(image, "No objects", (640, 360), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        if cnt == 0:
            cv2.imwrite("no_obj_" + str(num) + ".jpg", pr_img)
            num = num + 1
    elif cX == 4000:
        cv2.putText(image, "Too many objects", (640, 360), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        if cnt == 0:
            cv2.imwrite("too_many_" + str(num) + ".jpg", pr_img)
            num = num + 1
    else:
        cX = int(cX)
        cY = int(cY)
        cv2.circle(image, (cX, cY), 5, (255, 255, 255), -1)
        cv2.putText(image, "centroid", (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.imshow("video", image)
    cv2.waitKey(1)
    cnt = cnt + 1

cv2.destroyAllWindows()

