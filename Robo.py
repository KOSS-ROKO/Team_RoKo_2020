# -*- coding: utf-8 -*-

from Motion import Motion
from Def.VideoCall import VideoCall

print('code: Robo.py - ## Debug')


class Robo:
    
    _image_processor = VideoCall(video="")  # Image Processor

    def __init__(self, vpath=''):
        # self._image_processor = ImageProccessor(video=vpath) # Image Processor
        self._motion = Motion()  # Motion
