import cv2
import numpy as np

frame = cv2.imread('../../../Pictures/b.png')
hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
for i in range(3):
    cv2.imshow('h',hsv[:,:,i])
    cv2.waitKey()
cv2.destroyAllWindows()