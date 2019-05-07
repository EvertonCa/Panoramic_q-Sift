import cv2


class VideoToFrames:
    def __init__(self, handler):
        self.handler = handler

    def videoInFramesThreads(self, fps):
        step = int(1000 / fps)
        firstFrame = 0
        # TODO get amount of CPU
        process = 4
        video_name = self.handler.find_video_name()
        vidcap = cv2.VideoCapture(self.handler.input_directory + video_name)
        vidcap.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)
        lastFrame = vidcap.get(cv2.CAP_PROP_POS_MSEC)

        Lim = [round(int(i * (int(lastFrame / 1000) - firstFrame) / process)) for i in range(process + 1)]
        Lim = [round(i * 1000) for i in Lim]
        print(Lim)
        # TODO implement multiprocess
        self.videoInFrames(Lim[0], Lim[1] - 1, step)
        self.videoInFrames(Lim[1], Lim[2] - 1, step)
        self.videoInFrames(Lim[2], Lim[3] - 1, step)
        self.videoInFrames(Lim[3], Lim[4], step)

    def videoInFrames(self, firstFrame, lastFrame, step):
        video_name = self.handler.find_video_name()
        vidcap = cv2.VideoCapture(self.handler.input_directory + video_name)
        for i in range(firstFrame, lastFrame, step):
            vidcap.set(cv2.CAP_PROP_POS_MSEC, i)
            success, image = vidcap.read()
            if success:
                cv2.imwrite(self.handler.temp_directory + "frame%d.jpg" % i, image)