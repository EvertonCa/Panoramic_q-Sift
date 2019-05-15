import cv2
import datetime
from multiprocessing import Pool
from multiprocessing import cpu_count
import os


class VideoToFrames:
    def __init__(self, handler):
        self.handler = handler

    def video_in_frames_threads(self, fps):
        step = int(1000 / fps)
        first_frame = 0
        process = cpu_count()
        video_name = self.handler.find_video_name()
        vidcap = cv2.VideoCapture(self.handler.input_directory + video_name)
        vidcap.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)
        last_frame = int(vidcap.get(cv2.CAP_PROP_POS_MSEC))


        all_frames = [i for i in range(first_frame, last_frame, step)]

        print("[INFO] converting video into frames...", datetime.datetime.now())
        with Pool(process) as p:
            p.map(self.video_in_frames, all_frames, process)
        return first_frame, last_frame - (last_frame % step)

    def video_in_frames(self, frame):
        video_name = self.handler.find_video_name()
        vidcap = cv2.VideoCapture(self.handler.input_directory + video_name)
        vidcap.set(cv2.CAP_PROP_POS_MSEC, frame)
        success, image = vidcap.read()
        image = cv2.resize(image, (768, 432))
        if success:
            cv2.imwrite(self.handler.temp_directory + "frame%d.jpg" % frame, image)
