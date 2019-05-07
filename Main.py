from Handler import Handler
from VideoToFrames import VideoToFrames
from Stitcher import Stitcher

if __name__ == '__main__':
    handler = Handler()
    video_converter = VideoToFrames(handler)
    video_converter.videoInFramesThreads(10)
    stitcher = Stitcher(handler)
    stitcher.make_panoramic()

