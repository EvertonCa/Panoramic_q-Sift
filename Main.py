from Handler import Handler
from VideoToFrames import VideoToFrames
from Stitcher import Stitcher

if __name__ == '__main__':
    handler = Handler()
    video_converter = VideoToFrames(handler)
    # video_converter.video_in_frames()
    video_converter.videoInFramesThreads(1)
    stitcher = Stitcher(handler)
    stitcher.make_panoramic()

