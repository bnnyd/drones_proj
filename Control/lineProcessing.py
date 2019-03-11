#!/usr/env python3
import cv2
import numpy as np

class LineProcessing():
    def line_angle(self, image):
        # #Returns the line angle in degrees
        #image=cv2.imread('/home/benny/Pictures/line.png')
        img_bw = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        ret, clean_im = cv2.threshold(img_bw, 200, 255, cv2.THRESH_BINARY)

        nb_components, out, stats, centroids = cv2.connectedComponentsWithStats(clean_im, connectivity=8)

        if nb_components == 1:
            # Only background has been found
            print("Error! There are zero objects found")
            angle = 0
        else:
            # 0 is the leftmost x coord, 1 is the top y coord, 2 is width of bounding box, 3 is height of bounding box, 4 is area
            areas = stats[:, 4]
            # the background has always max area
            i_backgr = np.argmax(areas)
            # make background area zero
            areas[i_backgr] = 0
            i_max = np.argmax(areas)
            # index of the second largest object, the line

            x_bbox = stats[i_max, 2]
            y_bbox = stats[i_max, 3]
            #angle in radians
            abs_angle = np.arctan(y_bbox / x_bbox)

            cent = centroids[i_max]
            x_cent = cent[0]
            y_cent = cent[1]


            #take the mid point between the centroid and the end of the box, and check if the median y is lower or higher than y_cent
            midx= int(x_cent + 4*x_bbox/5)
            nonzero = np.nonzero(clean_im[:,midx])
            median_y = 0
            if len(nonzero)>0:
                median_y = np.average(nonzero)


            if(median_y < y_cent): # the angle is 0< <90, remember: rows count is from top to bottom
                angle = np.rad2deg(abs_angle)
            else:
                angle = 180 - np.rad2deg(abs_angle)
        return angle

    def line_angle2(self, image): #
        # #Returns the line angle in degrees
        #image=cv2.imread('/home/benny/Pictures/line.png')
        img_bw = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        ret, clean_im = cv2.threshold(img_bw, 200, 255, cv2.THRESH_BINARY)

        nb_components, out, stats, centroids = cv2.connectedComponentsWithStats(clean_im, connectivity=8)

        if nb_components == 1:
            # Only background has been found
            print("Error! There are zero objects found")
            angle = 0
        else:
            # 0 is the leftmost x coord, 1 is the top y coord, 2 is width of bounding box, 3 is height of bounding box, 4 is area
            areas = stats[:, 4]
            # the background has always max area
            i_backgr = np.argmax(areas)
            # make background area zero
            areas[i_backgr] = 0
            # index of the second largest object, the line
            i_max = np.argmax(areas)



            cent = centroids[i_max]
            x_cent = cent[0]
            y_cent = cent[1]

            y_len, x_len = np.shape(clean_im)
            zeros = np.zeros((y_len, x_len))
            zeros[0:int(y_cent), :] = 255
            cut_image = cv2.bitwise_and(clean_im, np.uint8(zeros))
            cut_nb_components, out, cut_stats, cut_centroids = cv2.connectedComponentsWithStats(cut_image, connectivity=8)

            areas = cut_stats[:,4]
            i_backgr = np.argmax(areas)
            areas[i_backgr] = 0
            i_max = np.argmax(areas)

            cent_cut = cut_centroids[i_max]
            x_cent_cut = cent_cut[0]
            y_cent_cut = cent_cut[1]

            x_diff = x_cent_cut - x_cent
            if x_diff==0:
                return 90
            elif x_diff < 0:
                x_diff = -x_diff
                angle = np.pi - np.arctan((y_cent-y_cent_cut)/(x_diff))
            else:
                angle = np.arctan((y_cent-y_cent_cut)/(x_diff))
        return np.rad2deg(angle)