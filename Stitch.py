# import the necessary packages
from Panorama import Stitcher
import imutils
import cv2

# load the two images and resize them to have a width of 400 pixels
# (for faster processing)
imageA = cv2.imread('Result4.jpg')
imageB = cv2.imread('Img4.jpg')
imageA = imutils.resize(imageA, height=600)
imageB = imutils.resize(imageB, height=600)

# stitch the images together to create a panorama
stitcher = Stitcher()
(result, vis) = stitcher.stitch([imageA, imageB], showMatches=True)

# show the images
# cv2.imshow("Image A", imageA)
# cv2.imshow("Image B", imageB)
# cv2.imshow("Keypoint Matches 1", vis)
cv2.imwrite("Result5.jpg", result)
cv2.waitKey(0)