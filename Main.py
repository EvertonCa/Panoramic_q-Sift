from Handler import Handler
from VideoToFrames import VideoToFrames
from Stitcher import Stitcher

if __name__ == '__main__':
    handler = Handler()
    video_converter = VideoToFrames(handler)
    #video_converter.video_in_frames_threads(10)
    intervalo_menor = 4000
    #intervalo_maior = 7000
    #video_converter.remove_frames_sequentially(intervalo_menor, intervalo_maior)
    video_converter.add_new_frames(intervalo_menor, 2)
    stitcher = Stitcher(handler)
    stitcher.make_panoramic()

