import cv2
import numpy as np

from ImageProcessor import ImageProccessor


class Holein:  
    
    def __init__(self):
        pass
    
    
    
    def ball_hole_oneframe():
        
        

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


        check_holecup = False
        check_ball = False

        lower_red = np.array([160, 70, 20])
        upper_red = np.array([178, 255, 255])

        red_mask = cv2.inRange(hsv_frame, lower_red, upper_red)
        red_objects = cv2.bitwise_and(frame, frame, mask=red_mask)

        # 33, 144, 144
        lower_yellow = np.array([0, 80, 50])
        upper_yellow = np.array([36, 250, 250])

        yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
        yellow_objects = cv2.bitwise_and(frame, frame, mask=yellow_mask)

        # 노란색, 빨간색 객체 표시
        cv2.imshow('Yellow Objects', yellow_objects)
        cv2.imshow('Red Objects', red_objects)

        y_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        r_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        # 노란색, 빨간색 물체의 크기를 확인할 최소 크기
        min_yellow_size = 10000 #이 수치는 프레임 크기에 따라서 나중에 조정 필요할듯요 
        min_red_size = 1000

        # 노란색 물체를 찾았고 크기가 최소 크기 이상인지 검사
        if y_contours and cv2.contourArea(max(y_contours, key=cv2.contourArea)) >= min_yellow_size \
            and r_contours and cv2.contourArea(max(r_contours, key=cv2.contourArea)) >= min_red_size:
            print("True")
        else:
            print("False")


        #cv2.imshow('Result', frame)
        #cv2.imshow('masked', yellow_mask)
        
        return 1


        
    
    def hole_in():
        
        
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
        imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        imgThreshLow = cv2.inRange(imgHSV, (0, 200, 155), (30, 255, 255))
        imgThreshHigh = cv2.inRange(imgHSV, (160, 155, 155), (179, 255, 255))
        
        imgThresh = cv2.add(imgThreshLow, imgThreshHigh)

        imgThresh = cv2.GaussianBlur(imgThresh, (3, 3), 2)
        imgThresh = cv2.erode(imgThresh, np.ones((5, 5), np.uint8))
        imgThresh = cv2.dilate(imgThresh, np.ones((5, 5), np.uint8))
        
        cv2.imshow('ball', imgThresh)
            
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
        
        