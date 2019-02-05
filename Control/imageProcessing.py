import cv2
import numpy as np
from Camera.camera import Camera
import glob
import os

class ImageProcessing():

    def object_center(image):
        #take the red matrix
        image_bw = image[:,:,2]
        ylen, xlen = image_bw.shape



        ret, image = cv2.threshold(image_bw, 170, 255, cv2.THRESH_BINARY)  # ensure binary
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))
        erosion = cv2.erode(image,kernel)
        clean_im = cv2.dilate(erosion,kernel)

        nb_components, out, stats, centroids = cv2.connectedComponentsWithStats(clean_im, connectivity=8)
        if nb_components == 1:
            #Only background has been found
            #print("Error! There are zero objects found")
            return 3000,3000,1280,720, image_bw
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

