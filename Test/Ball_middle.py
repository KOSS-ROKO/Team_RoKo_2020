# 최종 : 공이 중앙에 위치하면 stop
# go left & go right
# 빨간 공 잘 검출되는지 확인하기 위해, 빨간 공만 띄우는 창 추가함

import cv2
import numpy as np
from ImageProcessor import ImageProcessor 

class Ball:
    def __init__(self):
        pass

    def middle_ball():
        
        origin = ImageProcessor.get_img()
        frame = origin.copy()

        # 화면을 11x11 그리드로 나누는 함수
        def divide_screen(frame):
            height, width = frame.shape[:2]
            cell_height = height // 11
            cell_width = width // 11
            
            # 그리드 라인 그리기
            for i in range(1, 11):
                cv2.line(frame, (0, i * cell_height), (width, i * cell_height), (0, 255, 0), 2)  # 녹색
                cv2.line(frame, (i * cell_width, 0), (i * cell_width, height), (0, 255, 0), 2)
            
            return frame

    
        
        # 빨간색 객체 추출
        red_detected = ImageProcessor.detect_ball(frame)
        
        # 화면을 11x11 그리드로 나누고 그리드 라인 그리기
        divided_frame = divide_screen(frame)
        
        #여기에 새로운 코드 추가
        # 빨간색 객체 검출 및 위치 계산
        non_zero_pixels = np.transpose(np.nonzero(red_detected))
        
        if non_zero_pixels.size > 0:
            x_center = non_zero_pixels[:, 1].mean()
            y_center = non_zero_pixels[:, 0].mean()
            
            cell_width = divided_frame.shape[1] // 11

            # 빨간 공이 중앙 세로줄인 6번째 줄에서 검출되면 "stop" 출력
            if (cell_width * 5 <= x_center <= cell_width * 6):
                print("stop")
                return "stop"
            # 1~5번째 줄에서 검출되면 "go right" 출력
            elif x_center < cell_width * 5:
                print("go right")
                return "go right"
            # 7~11번째 줄에서 검출되면 "go left" 출력
            elif x_center > cell_width * 6:
                print("go left")
                return "go left"
        else:
            print("go far")
            return "go far"
