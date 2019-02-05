#!/usr/env python3
import cv2
import numpy as np
import os
for i in range(6):
	name = "no_obj_"+str(i)+".jpg"
	if os.path.isfile("./"+name)==False:
		continue
	im = cv2.imread(name)
	x, y, z = im.shape
	p = 0.6
	im = cv2.resize(im, (int(y*p), int(x*p)))
	cv2.imshow('im',im)
	cv2.waitKey(0)

cv2.destroyAllWindows()


