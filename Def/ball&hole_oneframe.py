import cv2
import numpy as np

class Oneframe:
    def __init__(self):
        pass


    def ball_hole_oneframe(frame):
    
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


        lower_red = np.array([160, 70, 20])
        upper_red = np.array([178, 255, 255])

        red_mask = cv2.inRange(hsv_frame, lower_red, upper_red)
        red_objects = cv2.bitwise_and(frame, frame, mask=red_mask)

        lower_yellow = np.array([0, 80, 50])
        upper_yellow = np.array([36, 250, 250])

        yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
        yellow_objects = cv2.bitwise_and(frame, frame, mask=yellow_mask)

        # 노란색, 빨간색 객체 표시
        #cv2.imshow('Yellow Objects', yellow_objects)
        #cv2.imshow('Red Objects', red_objects)

        y_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        r_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        # 노란색, 빨간색 물체의 크기를 확인할 최소 크기
        min_yellow_size = 10000 #이 수치는 프레임 크기에 따라서 나중에 조정 필요할듯요 
        min_red_size = 1000

        # 노란색 물체를 찾았고 크기가 최소 크기 이상인지 검사
        if y_contours and cv2.contourArea(max(y_contours, key=cv2.contourArea)) >= min_yellow_size \
            and r_contours and cv2.contourArea(max(r_contours, key=cv2.contourArea)) >= min_red_size:
            return True
        else:
            return False


        #cv2.imshow('Result', frame)
        #cv2.imshow('masked', yellow_mask)

