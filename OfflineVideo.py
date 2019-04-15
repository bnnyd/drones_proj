#!/usr/bin/env python3
import cv2
import os
import numpy as np
import time

#from Control.imageProcessing import ImageProcessing
#from Control.lineProcessing import LineProcessing
from Control.lines_dir import linesDirection
from Control.line_control import linesControl
#videos = ['offline.mp4', 'offline1.mp4', 'offline2.mp4']
videos = ['line1.mp4']

for video in videos:
    #print(video)
    vidcap = cv2.VideoCapture(video)
    success,image = vidcap.read()
    print(success)
    rate = 5
    cnt = 5
    num = 0
    while success:

        time.sleep(0.05)
        success,image2 = vidcap.read()

        if False: ## Try to find on a offline video the red point centroids
            if cnt==rate:
                image = image2
                cX, cY, xlen, ylen, pr_img = ImageProcessing.object_center(image)
                cnt = 0



            if cX == 2000:
                cv2.putText(image, "Empty dir", (640, 360), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            elif cX == 3000:
                cv2.putText(image, "No objects", (640, 360), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                if cnt == 0:
                    cv2.imwrite(video + "_no_obj_" + str(num) + ".jpg", pr_img)
                    num = num + 1
            elif cX == 4000:
                cv2.putText(image, "Too many objects", (640, 360), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                if cnt == 0:
                    cv2.imwrite(video + "_too_many_" + str(num) + ".jpg", pr_img)
                    num = num + 1
            else:
                cX = int(cX)
                cY = int(cY)
                cv2.circle(image, (cX, cY), 5, (255, 255, 255), -1)
                cv2.putText(image, "centroid", (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.imshow(video, image)
            cv2.waitKey(1)
            cnt = cnt + 1
        if True: ## Try to find on an offline video the line angle
            if cnt==rate:
                image = image2
                x0, y0, m = linesDirection(image)
                x_p, y_p = linesControl(0,0,m)
                #q, angle = linesDirection(image)
                #dist = 0
                rows, cols = image.shape[:2]
                cnt = 0
                ## take a perpendicular to the line
                #if dist < 0: ## below the center
                #    angle = angle + np.pi/2
                #elif dist >= 0:
                #    angle = angle - np.pi/2

                #if angle > 2*np.pi:
                #    angle = angle - 2 * np.pi

                #sin = np.sin(angle)
                #cos = np.cos(angle)
                # #
                #arrow_end_x = int(abs(dist)*cos)
                #arrow_end_y = int(abs(dist)*sin)

                #text = "dist " + str(dist) + ", angle " + str(np.rad2deg(angle))
                #cv2.putText(image, str(int(m)), (640, 360 + 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                #cv2.line(image, (cols - 1, righty), (0, lefty), (0, 255, 0), 2)
                #cv2.putText(image, "m: " + str(dist) + ", q: " + str(angle), (640, 360), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                #a = np.deg2rad(angle)
                cv2.arrowedLine(image, (640,360), (x_p, y_p), (0,0,255) ,3)
                #cv2.arrowedLine(image, (640,360), (640 + arrow_end_x, 360 - arrow_end_y), (0,0,255) ,3)
            cv2.imshow(video, image)
            cv2.waitKey(1)
            cnt = cnt + 1


cv2.destroyAllWindows()
