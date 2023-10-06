import cv2
import numpy as np
import os
import time
import platform
from imutils.video import WebcamVideoStream
from imutils.video import FileVideoStream
from imutils.video import FPS

import warnings
warnings.simplefilter(
    action='ignore', category=FutureWarning)  # FutureWarning 제거

print('code: ImageProcessor.py - ## Debug')

if __name__ == "__main__":
    from Ball_hole_oneframe import Oneframe
    from Ball_middle import Ball  # 파일명 / class이름
    from Detection import Detection
    from Holein import Holein



class ImageProcessor:
    def __init__(self, video: str = ""):
        print("init_imgprocessor")

        if video and os.path.exists(video):
            self._cam = FileVideoStream(path=video).start()
        else:
            print('# image processor #', platform.system())
            if platform.system() == "Linux":
                print('eee')
                self._cam = WebcamVideoStream(src=-1).start()
            else:
                self._cam = WebcamVideoStream(src=0).start()
            print('Acquire Camera ')

        self.fps = FPS()  # FPS
        print(self.fps)  # debuging: fps
        shape = (self.height, self.width, _) = self.get_img().shape
        print("Shape :: ", shape)  # debuging: image shape => height, width
        time.sleep(2)


    ########### 이미지 불러오기 ###########
    def get_img(self, show=False):
        img = self._cam.read()
        # 이미지를 받아오지 못하면 종료
        if img is None:
            exit()

        # 이미지를 받아오면 화면에 띄움
        if show:
            cv2.imshow("imageProcessor-get_img", img)
            cv2.waitKey(1)
        return img
