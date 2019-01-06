import cv2
import numpy as np

image = cv2.imread('red.JPG')

#take the red matrix
image_bw = image[:,:,2]
#cv2.imshow('redscale',image_bw)
#cv2.waitKey(0)
#cv2.destroyAllWindows()


ret, image = cv2.threshold(image_bw, 240, 255, cv2.THRESH_BINARY)  # ensure binary
kernel = np.ones((5,5),np.uint8)
erosion = cv2.erode(image,kernel)
clean_im = cv2.dilate(erosion,kernel)
#cv2.imshow('b&w',image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
ret, labels = cv2.connectedComponents(clean_im)
if np.amax(labels)!=1:
    print("Error! There are zero or more than one objects found")
cv2.imshow('b&w',clean_im)
cv2.waitKey(0)
cv2.destroyAllWindows()

M = cv2.moments(clean_im)

# calculate x,y coordinate of center
cX = int(M["m10"] / M["m00"])
cY = int(M["m01"] / M["m00"])

print(cX,cY)

img = cv2.bitwise_and(clean_im,image)

# # put text and highlight the center
# cv2.circle(img, (cX, cY), 5, (255, 255, 255), -1)
# cv2.putText(img, "centroid", (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
#
# # display the image
cv2.imshow("Image", image)
cv2.waitKey(0)

## The function should return cX and cY