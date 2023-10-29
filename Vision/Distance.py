import cv2
import numpy as np

### 거리 재는 코드 ㅇㅇ
from ImageProcessor import ImageProcessor

class Distance:
    def __init__(self):
        pass

    def holecup_dist(f):
        W = 0.18 # 홀컵 크기
        
        w = ImageProcessor.detect_holecup("call_w") # holecup area 인지 holecup cirle인지 나중에 정해줘야함

        if w is not None:
            d = (W * f) / w
            print("--- holecup_distance :", d)
            return d
        

    def ball_dist(f):
        W = 0.04 # 공 크기
        
        imgThresh = ImageProcessor.detect_ball("call_video")
        
        # 빨간 공의 가로 크기를 측정 (w)
        contours, _ = cv2.findContours(imgThresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            print("this is w :", w)

        # 초점 거리(f) 계산
        if w is not None:
            d = (W * f) / w
            print("--- ball_distance :", d)
            return d

    