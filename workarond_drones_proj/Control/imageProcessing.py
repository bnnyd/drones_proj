import cv2
import numpy as np
from .control_common import NoObj
from Camera.camera import Camera
import glob
import os

class RedCircle():
    def show(self,frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        cv2.imshow('h',hsv[:,:,0])
        cv2.waitKey(1)
        cv2.destroyAllWindows()

    def object_center(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        hue = hsv[:,:,1]
        ylen, xlen = hue.shape



        ret, clean_im = cv2.threshold(hue, 120, 179, cv2.THRESH_BINARY)  # ensure binary

        nb_components, out, stats, centroids = cv2.connectedComponentsWithStats(clean_im, connectivity=8)
        if nb_components == 1:
            #Only background has been found
            #print("Error! There are zero objects found")
            return NoObj.NO_OBJECT,NoObj.NO_OBJECT,1280,720, hue
        else:
            # 4 is the column of "area" in stats
            areas = stats[:, 4]
            # the background has always max area
            i_backgr = np.argmax(areas)
            # make background area zero
            areas[i_backgr] = 0
            i_max = np.argmax(areas)
            cent = centroids[i_max]
            cX = cent[0]
            cY = cent[1]


        return cX, cY, xlen, ylen, clean_im



