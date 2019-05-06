import cv2
from imutils import paths
import imutils
import datetime
import os


def SIFT(firstFrame, lastFrame, step):

  for i in range(firstFrame, lastFrame - step, step):
    sift = cv2.xfeatures2d.SIFT_create()

    img1 = cv2.imread("Images/frame%dms.jpg" % i)
    img2 = cv2.imread("Images/frame%dms.jpg" % (i + step))

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
    for m, n in matches:
      if m.distance < 0.75 * n.distance:
        good.append([m])
    # cv.drawMatchesKnn expects list of lists as matches.
    img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    # cv2.imshow("Resultado", img3)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # cv2.imwrite("Resultado.png", img3)
    # plt.imshow(img3), plt.show()


def videoInFrames(nome, firstFrame, lastFrame, step):
  vidcap = cv2.VideoCapture(nome)
  for i in range(firstFrame, lastFrame, step):
    vidcap.set(cv2.CAP_PROP_POS_MSEC, i)
    success, image = vidcap.read()
    if success:
      cv2.imwrite("Images/frame%d.jpg" % i, image)


def videoInFramesThreads(nome, fps):
  try:
    os.makedirs("Images")
  except:
    pass
  step = int(1000 / fps)
  firstFrame = 0
#TODO get amount of CPU
  process = 4
  vidcap = cv2.VideoCapture(nome)
  vidcap.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)
  lastFrame = vidcap.get(cv2.CAP_PROP_POS_MSEC)

  Lim = [round(int(i * (int(lastFrame/1000) - firstFrame) / (process))) for i in range(process + 1)]
  Lim = [round(i*1000) for i in Lim]
  print(Lim)
#TODO implement multiprocess
  videoInFrames(nome, Lim[0], Lim[1]-1, step)
  videoInFrames(nome, Lim[1], Lim[2]-1, step)
  videoInFrames(nome, Lim[2], Lim[3]-1, step)
  videoInFrames(nome, Lim[3], Lim[4], step)


def stitching(folderDirectory):
  print("[INFO] loading images...", datetime.datetime.now())
  imagePaths = sorted(list(paths.list_images(folderDirectory)))
  images = []

  # loop over the image paths, load each one, and add them to our
  # images to stich list
  for imagePath in imagePaths:
    image = cv2.imread(imagePath)
    images.append(image)

  # initialize OpenCV's image sticher object and then perform the image
  # stitching
  print("[INFO] stitching images...", datetime.datetime.now())
  stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
  (status, stitched) = stitcher.stitch(images)

  # if the status is '0', then OpenCV successfully performed image
  # stitching
  if status == 0:

    print("data result", datetime.datetime.now())
    # write the output stitched image to disk
    cv2.imwrite("image.jpg", stitched)

    # display the output stitched image to our screen
    cv2.imshow("Stitched", stitched)
    cv2.waitKey(0)
  # otherwise the stitching failed, likely due to not enough keypoints)
  # being detected
  else:
    print("data result", datetime.datetime.now())
    print("[INFO] image stitching failed ({})".format(status))

  return stitched


# img1 = cv2.imread("Img1.jpg", cv2.IMREAD_GRAYSCALE)
# img2 = cv2.imread("Img2.jpg", cv2.IMREAD_GRAYSCALE)
if __name__ == '__main__':
  videoInFramesThreads('Video.MOV', 2)
  #stitching('I')

  """""
  firstFrame = 0
  lastFrame = 921
  step = 1
  process = 4

  Lim = [round(i*(lastFrame-firstFrame)/(process)) for i in range(process+1)]
  Lim[0] = -1

  SIFT(0, 921, 1)

  for i in range(process):
    print(Lim[i]+1, Lim[i+1], step)
    SIFT(Lim[i]+1, Lim[i+1], step)

  """""
