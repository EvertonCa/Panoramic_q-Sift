import cv2
import numpy as np
import matplotlib.pyplot as plt

img1 = cv2.imread("Img1.png", cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread("Img2.png", cv2.IMREAD_GRAYSCALE)

sift = cv2.xfeatures2d.SIFT_create()

kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

# Here kp will be a list of keypoints and des is a numpy array of shape Number_of_Keypoints×128.
# img = cv2.drawKeypoints(img, kp, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
#
# cv2.imshow("Imagem", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


bf = cv2.BFMatcher()
matches = bf.knnMatch(des1, des2, k=2)
# Apply ratio test
good = []
for m,n in matches:
    if m.distance < 0.75*n.distance:
        good.append([m])
# cv.drawMatchesKnn expects list of lists as matches.
img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
cv2.imshow("Resultado", img3)
cv2.waitKey(0)
cv2.destroyAllWindows()
# plt.imshow(img3), plt.show()