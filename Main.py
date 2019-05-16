from Handler import Handler
from VideoToFrames import VideoToFrames
from Panorama import Stitcher
import cv2
import time

if __name__ == '__main__':
    fps = 1
    handler = Handler()
    video_converter = VideoToFrames(handler)
    (first_frame, last_frame) = video_converter.video_in_frames_threads(fps)
    #(first_frame, last_frame) = (0, 12000)
    stitcher = Stitcher()
    start = time.time()
    result = stitcher.stitch(first_frame, last_frame, fps)
    print("Time stiching = {0:.5f}s".format(time.time() - start))
    cv2.imwrite("result.jpg", result)

