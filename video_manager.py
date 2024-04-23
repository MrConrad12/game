from const import HEIGHT, WIDTH
from pygame import *

class VideoManager:
    def __init__(self):
        self.video_path = ""
        self.video = Video(self.video_path)
        self.video_info = MediaInfo.parse(self.video_path)
        self.video.set_size((WIDTH, HEIGHT))
        self.video_duration = 0
        self.play = False
        for sequence in self.video_info:
            if sequence.track_type == 'Video':
                self.video_duration = sequence.duration / 1000
    def play_video(self):
        pass