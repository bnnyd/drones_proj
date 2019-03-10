#!/usr/env python3
import cv2
import numpy as np


#class LineProcessing():
# def getOrientation(pts):
#     sz = len(pts)
#     data_pts = np.empty((sz, 2), dtype=np.float64)
#     for i in range(data_pts.shape[0]):
#         data_pts[i, 0] = pts[i, 0, 0]
#         data_pts[i, 1] = pts[i, 0, 1]
#     # Perform PCA analysis
#     mean = np.empty((0))
#     mean, eigenvectors, eigenvalues = cv2.PCACompute2(data_pts, mean)
#     # Store the center of the object
#     #cntr = (int(mean[0, 0]), int(mean[0, 1]))
#
#     #cv.circle(img, cntr, 3, (255, 0, 255), 2)
#     #p1 = (
#     #cntr[0] + 0.02 * eigenvectors[0, 0] * eigenvalues[0, 0], cntr[1] + 0.02 * eigenvectors[0, 1] * eigenvalues[0, 0])
#     #p2 = (
#     #cntr[0] - 0.02 * eigenvectors[1, 0] * eigenvalues[1, 0], cntr[1] - 0.02 * eigenvectors[1, 1] * eigenvalues[1, 0])
#     angle = atan2(eigenvectors[0, 1], eigenvectors[0, 0])  # orientation in radians
#     return angle
#
#  #   def line_angle(self,image):
# image=cv2.imread('/home/benny/Pictures/line.png')
# img_bw = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
# ret, clean_im = cv2.threshold(img_bw, 150, 255, cv2.THRESH_BINARY)
#
# cv2.imshow('lines',clean_im)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
# #cv2.drawContours(src, contours, i, (0, 0, 255), 2);
#
# im, contours = cv2.findContours(clean_im, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
# area_max = 0
# i_max = 0
# i = 0
# cv2.imshow('lines',im)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# for i,cont in enumerate(contours):
#     cv2.drawContours(image, contours, i, (0, 0, 255), 2)
#     #area = cv2.contourArea(cont)
#     #if area > area_max:
#     #    i_max = i
#     #    area_max = area
#     i = i + 1
#     cv2.imshow('lines', image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#
# #i_max = np.argmax(areas)
# angle = getOrientation(contours[i_max])
# print(rad2deg(angle))


        # for i, c in enumerate(contours):
        #     # Calculate the area of each contour
        #     area = cv2.contourArea(c)
        #     # Ignore contours that are too small or too large
        #     if area < 1e2 or 1e5 < area:
        #         continue
        #     # Draw each contour only for visualisation purposes
        #     cv.drawContours(src, contours, i, (0, 0, 255), 2)
        #     # Find the orientation of each shape
        #     getOrientation(c, src)




    #return degree_angle





#############
class LineProcessing():
    def line_angle(self, image): #
           # #Returns the line angle in degrees
        #image=cv2.imread('/home/benny/Pictures/line.png')
        img_bw = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        ret, clean_im = cv2.threshold(img_bw, 200, 255, cv2.THRESH_BINARY)

        nb_components, out, stats, centroids = cv2.connectedComponentsWithStats(clean_im, connectivity=8)

        if nb_components == 1:
            # Only background has been found
            print("Error! There are zero objects found")
            angle = -1
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
                a = "<90"
            else:
                angle = 180 - np.rad2deg(abs_angle)
                a = ">90"
            # cX = int(x_cent)
            # cY = int(y_cent)
            # cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)
            # cv2.putText(image, "centroid", (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            #
            #
            # cv2.circle(image, (midx, int(median_y)), 5, (0, 0, 255), -1)
            # cv2.putText(image, "dir", (midx - 25, int(median_y) - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            #
            # cv2.imshow('lines', image)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            # #
            # print(angle)
        return angle, a


###########


############


##########

#
# image=cv2.imread('/home/benny/Pictures/line.png')
#
# # USE CANNY:
#
# img_bw= cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
# # cv2.imshow('lines',img_bw)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()
# # lowThresh = 100
# # highThresh = 3*lowThresh
# # res = cv2.Canny(img_bw,lowThresh,highThresh, apertureSize=3)
# # cv2.imshow('lines',res)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()
#
# ret, clean_im = cv2.threshold(img_bw, 150, 255, cv2.THRESH_BINARY)
#
# nb_components, out, stats, centroids = cv2.connectedComponentsWithStats(clean_im, connectivity=8)
#
#
# if nb_components == 1:
#     #Only background has been found
#     print("Error! There are zero objects found")
# else:
#     # 2 is width of bounding box, 3 is height of bounding box, 4 is area
#     areas = stats[:, 4]
#     # the background has always max area
#     i_backgr = np.argmax(areas)
#     # make background area zero
#     areas[i_backgr] = 0
#     i_max = np.argmax(areas)
#     # index of the second largest object, the line
#     x_line = stats[i_max,2]
#     y_line = stats[i_max,3]
#     #angle in radians
#     angle = np.arctan(y_line/x_line)
#     print(np.rad2deg(angle))
#
# cv2.imshow('lines',clean_im)
# cv2.waitKey(0)
# cv2.destroyAllWindows()