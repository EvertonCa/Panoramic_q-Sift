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
        start_images = []
        stitched = None

        print("[INFO] stitching images...", datetime.datetime.now())
        for imagePath in image_paths:
            image = cv2.imread(imagePath)
            if len(start_images) is 20:
                stitched = self.stitch_two(start_images)
                cv2.imwrite(self.handler.temp_directory + "Result.jpg", stitched)
                start_images.clear()
            if counter < 20:
                start_images.append(image)
                counter += 1
            else:
                temp.append(stitched)
                temp.append(image)
                new_stitched = self.stitch_two(temp)
                temp.clear()
                cv2.imwrite(self.handler.temp_directory + "Result_%d.jpg" % index, new_stitched)
                stitched = new_stitched.copy()
            index += 1

        self.handler.clear_temp()

        cv2.imwrite(self.handler.temp_directory + "Result.jpg", stitched)

    def stitch_two(self, images):
        stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()

        status, stitched = stitcher.stitch(images)

        # if the status is '0', then OpenCV successfully performed image stitching
        if status == 0:
            print("Stitching Successful at ", datetime.datetime.now())
            # write the output stitched image to disk
            # cv2.imwrite(self.handler.temp_directory + "Result_%d.jpg" % index, stitched)

            # display the output stitched image to our screen
            # cv2.imshow("Stitched", stitched)
            # cv2.waitKey(0)

        # otherwise the stitching failed, likely due to not enough keypoints)
        # being detected
        else:
            print("ERROR Stitching at", datetime.datetime.now())
            print("[INFO] image stitching failed ({})".format(status))

        return stitched

    def make_panoramic(self):
        size = 11
        while size > 10:
            size = self.stitch()
        self.stitch()
        self.handler.save()

