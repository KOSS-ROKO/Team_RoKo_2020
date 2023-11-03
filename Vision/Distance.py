import cv2
import numpy as np

### 거리 재는 코드 ㅇㅇ
from ImageProcessor import ImageProcessor



class Distance:
    def __init__(self):
        pass

    def distance():
        _Head_UD_Middle_Value = 113
        _Head_ServoAngle_list = [i*3+11 for i in range(17)]
        _Head_Length_list = [0.8, 1.9, 3.5, 4.4, 6.4, 7.9, 9.5, 11.2, 12.9, 14.8, 16.5, 18.1, 21.5, 24.1, 26.5, 29.8, 32.6]
        

        Head_UD_Middle_Value_Measures = 100
        Head_ud_angle = Head_UD_Middle_Value_Measures


        Length_Weight = _Head_UD_Middle_Value - Head_UD_Middle_Value_Measures
        Head_ServoAngle_Measures_list = [i*3+11-Length_Weight for i in range(17)]


        Length_ServoAngle = list(zip(Head_ServoAngle_Measures_list,_Head_Length_list))
        Length_ServoAngle_dict = dict(Length_ServoAngle)


    '''def holecup_dist(f):
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
            return d'''
    

    