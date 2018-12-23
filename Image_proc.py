#!/bin/env python3

import numpy as np
import cv2
import glob

image_list = []
w = 320
h = 180

for filename in glob.glob('Images/*'):
    im_big=cv2.imread(filename)

    im_small=cv2.resize(im_big,(w,h))
    gray_im = cv2.cvtColor(im_small, cv2.COLOR_RGB2GRAY)
    print(gray_im.shape)
    image_list.append(gray_im)



for im in image_list:
    white1 = [0,0]
    white2 = [0,0]
    for i in range(h):
        for j in range(w):
            pixel = im[i][j]
            if (pixel > 240) and (white1 == [0,0]):
                white1 = [i,j]
            elif (pixel > 240) and (white1 != [0,0]):
                white2 = [i,j]
    print(white1, white2)
    black = 0
    im[white1[0]][white1[1]]= black
    im[white2[0]][white2[1]] = black
    cv2.imshow('a', im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
