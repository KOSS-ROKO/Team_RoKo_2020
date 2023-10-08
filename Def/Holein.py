import cv2
import numpy as np

from Def.ImageProcessor import ImageProcessor
from Detection import Detection

class Holein:
    def __init__(self):
        pass


    def detect_hole_in():
        
        origin = ImageProcessor.get_img()
        frame = origin.copy()
        
        try:
        
            # 노란색 홀컵 검출
            yellow_lower = np.array([20, 20, 100])
            yellow_upper = np.array([36, 250, 250])
            
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            yellow_mask = cv2.inRange(hsv_frame, yellow_lower, yellow_upper)
            yellow_objects = cv2.bitwise_and(frame, frame, mask=yellow_mask)
            
            #cv2.imshow('HoleCup', yellow_mask)
            
            blurred_frame = cv2.GaussianBlur(yellow_objects, (5, 5), 0)
            gray_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2GRAY)
            
            _, binary_frame = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            
            # 이미지 전처리 - 침식, 팽창
            kernel = np.ones((5, 5), np.uint8)
            binary_frame = cv2.erode(binary_frame, kernel, iterations=1)
            binary_frame = cv2.dilate(binary_frame, kernel, iterations=1)
            
            cv2.imshow('Binary Image', binary_frame) # 이진화된 이미지 표시
            
            contours, _ = cv2.findContours(binary_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # 노란색 홀컵 윤곽선
            
            
            ##### 가장 왼쪽과 오른쪽 점 찾기
            
            left_point_y, right_point_y = None, None
            
            if contours:
                for contour in contours:
                    for point in contour:
                        x = point[0][0]
                        y = point[0][1]

                        # 가장 왼쪽점 업데이트
                        if left_point_y is None or x < left_point_y[0]:
                            left_point_y = [x, y]

                        # 가장 오른쪽점 업데이트
                        if right_point_y is None or x > right_point_y[0]:
                            right_point_y = [x, y]

            result = frame.copy()
            if left_point_y is not None:
                cv2.circle(result, tuple(left_point_y), 5, (0, 0, 255), -1)
            if right_point_y is not None:
                cv2.circle(result, tuple(right_point_y), 5, (0, 0, 255), -1)
                
                
                
            #############여기서부터 빨간공
            
            
            # 빨간공 인식
            imgThresh = Detection.detect_ball(frame)
                
            contours, _ = cv2.findContours(imgThresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # 빨간색 골프 공 윤곽선
            
            
            ##### 가장 왼쪽과 오른쪽 점 찾기

            left_point_red, right_point_red = None, None
            
            if contours:
                for contour in contours:
                    for point in contour:
                        x_red = point[0][0]
                        y_red = point[0][1]

                        # 가장 왼쪽점 업데이트
                        if left_point_red is None or x_red < left_point_red[0]:
                            left_point_red = [x_red, y_red]

                        # 가장 오른쪽점 업데이트
                        if right_point_red is None or x_red > right_point_red[0]:
                            right_point_red = [x_red, y_red]

            if left_point_red is not None:
                cv2.circle(result, tuple(left_point_red), 5, (0, 255, 0), -1)
            if right_point_red is not None:
                cv2.circle(result, tuple(right_point_red), 5, (0, 255, 0), -1)
                
                

            ##### 홀인 여부 판단
            
            if left_point_y is not None and right_point_y is not None:
                A, A_prime = left_point_y[0], right_point_y[0]
                B, B_prime = left_point_red[0], right_point_red[0]
                
                if A < B < A_prime and A < B_prime < A_prime:
                    hole_result = "HoleIn"
                else:
                    hole_result = "NO..."
            else:
                hole_result = "NO..."
                
            return hole_result, result
        
        
        
        except Exception as e:
            print(f"Error: {e}")
            
            return f"Error: {e}"
