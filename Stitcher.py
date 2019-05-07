import cv2
from imutils import paths
import imutils
import datetime
import re


class Stitcher:
    def __init__(self, handler):
        self.handler = handler

    def atoi(self, text):
        return int(text) if text.isdigit() else text

    def natural_keys(self, text):
        '''
        alist.sort(key=natural_keys) sorts in human order
        http://nedbatchelder.com/blog/200712/human_sorting.html
        (See Toothy's implementation in the comments)
        '''
        return [self.atoi(c) for c in re.split(r'(\d+)', text)]

    def stitch(self):
        print("[INFO] loading images...", datetime.datetime.now())
        image_paths = list(paths.list_images(self.handler.temp_directory))
        image_paths.sort(key=self.natural_keys)
        images = []

        # loop over the image paths, load each one, and add them to our
        # images to stich list
        counter = 0
        index = 0
        temp = []
        for imagePath in image_paths:
            image = cv2.imread(imagePath)
            if counter < 10:
                temp.append(image)
                counter += 1
            else:
                counter = 1
                index += 1
                temp2 = temp.copy()
                images.append(temp2)
                temp.clear()
                temp.append(image)

        if len(temp) is not 0:
            temp2 = temp.copy()
            images.append(temp2)
            temp.clear()

        self.handler.clear_temp()

        # initialize OpenCV's image sticher object and then perform the image
        # stitching
        print("[INFO] stitching images...", datetime.datetime.now())

        quantity = 0

        for index2, i in enumerate(images):
            self.stitch_ten(i, index2)
            quantity = index2

        return quantity

    def stitch_ten(self, images, index):
        stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()

        status, stitched = stitcher.stitch(images)

        # if the status is '0', then OpenCV successfully performed image stitching
        if status == 0:
            print("Stitching Successful at ", datetime.datetime.now())
            # write the output stitched image to disk
            cv2.imwrite(self.handler.temp_directory + "Result_%d.jpg" % index, stitched)

            # display the output stitched image to our screen
            # cv2.imshow("Stitched", stitched)
            # cv2.waitKey(0)

        # otherwise the stitching failed, likely due to not enough keypoints)
        # being detected
        else:
            print("data result", datetime.datetime.now())
            print("[INFO] image stitching failed ({})".format(status))

    def make_panoramic(self):
        size = 11
        while size > 10:
            size = self.stitch()
        self.stitch()
        self.handler.save()

