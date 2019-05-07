import cv2


class VideoToFrames:
    def __init__(self, handler):
        self.handler = handler

    def video_in_frames(self):
        video_name = self.handler.find_video_name()
        vidcap = cv2.VideoCapture(self.handler.input_directory + video_name)
        success, image = vidcap.read()
        count = 1
        while success:
            image = cv2.resize(image, (768, 432))
            cv2.imwrite(self.handler.temp_directory + "frame%d.jpg" % count, image)  # save frame as JPEG file
            success, image = vidcap.read()
            print('Read a new frame: ', success)
            count += 1
