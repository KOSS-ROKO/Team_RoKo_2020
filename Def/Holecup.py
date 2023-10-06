import cv2
import numpy as np

from ImageProcessor import ImageProccessor


class Holecup:  
    
    def __init__(self):
        pass
    
    
    
    def detect_holecup_area(self, show=False):
        
        
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_yellow = np.array([0, 80, 50])
        upper_yellow = np.array([36, 250, 250])

        yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
        yellow_objects = cv2.bitwise_and(frame, frame, mask=yellow_mask)

        cv2.imshow('Yellow Objects', yellow_objects)

        blurred_frame = cv2.GaussianBlur(yellow_objects, (5, 5), 0)
        gray_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow('Blurred Image', gray_frame)

        _, binary_frame = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        cv2.imshow('Binary Image', binary_frame)

        contours, _ = cv2.findContours(binary_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        max_area = 0  # 가장 큰 노란색 물체의 면적
        max_area_contour = None  # 가장 큰 노란색 물체의 컨투어

        for contour in contours:
            area = cv2.contourArea(contour)

            if area > max_area:
                max_area = area
                max_area_contour = contour

        if max_area_contour is not None:
            M = cv2.moments(max_area_contour)
            if M["m00"] != 0:
                center_x = int(M["m10"] / M["m00"])
                center_y = int(M["m01"] / M["m00"])

                # 노란색 물체의 크기에 따라 초록색 원 그리기
                radius = int(max_area ** 0.5 / 2)
                cv2.circle(frame, (center_x, center_y), radius, (0, 255, 0), 2)
                # 중심 좌표 표시
                cv2.circle(frame, (center_x, center_y), 2, (0, 0, 255), -1)

                # 중심 좌표가 초록색 원 안에 있는지 확인
                if center_x - radius >= 0 and center_x + radius < frame.shape[1] and center_y - radius >= 0 and center_y + radius < frame.shape[0]:
                    # 노란색 물체의 중심이 초록색 원 안에 있을 때, 초록색 원을 그림
                    cv2.circle(frame, (center_x, center_y), radius, (0, 255, 0), 2)

        #cv2.imshow('Result', frame)
        #cv2.imshow('masked', yellow_mask)
        
        return 1

            
        

    
    
    def detect_holecup_circle(self, show=False):
        
        detected_circles = []
        
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 33, 144, 144
        lower_yellow = np.array([25, 80, 50])
        upper_yellow = np.array([36, 250, 250])

        yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
        yellow_objects = cv2.bitwise_and(frame, frame, mask=yellow_mask)

        # 노란색 객체 표시
        cv2.imshow('Yellow Objects', yellow_objects)

        # Gaussian Blur를 사용하여 노이즈 제거
        blurred_frame = cv2.GaussianBlur(yellow_objects, (5, 5), 0)
        gray_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2GRAY)

        # 블러된 이미지 표시
        cv2.imshow('Blurred Image', gray_frame)

        # 이진화를 사용하여 노란색 물체 강조
        _, binary_frame = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        # 이진화된 이미지 표시
        cv2.imshow('Binary Image', binary_frame)

        # 침식과 팽창을 사용하여 이미지를 보정
        kernel = np.ones((5, 5), np.uint8)
        binary_frame = cv2.erode(binary_frame, kernel, iterations=1)
        binary_frame = cv2.dilate(binary_frame, kernel, iterations=1)

        # 침식과 팽창된 이미지 표시
        # cv2.imshow('Eroded and Dilated Image', binary_frame)

        # edges = cv2.Canny(binary_frame, 50, 150)  # 에지 검출 (Canny 사용)

        # 에지 이미지 표시
        # cv2.imshow('Edges', edges)

        contours, _ = cv2.findContours(binary_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # 객체 검출 (컨투어 사용)



        
        detected_circles = []  # 감지된 원의 정보를 저장할 리스트 초기화

        # 검출된 원 정보 저장
        for contour in contours:
            min_radius = 20
            max_radius = 160
            epsilon = 0.01 * cv2.arcLength(contour, True) # 엡실론 값 조정
            approx = cv2.approxPolyDP(contour, epsilon, True)

            if len(approx) >= 8:
                center, _ = cv2.minEnclosingCircle(contour)
                center = tuple(map(int, center))
                radius = int(cv2.arcLength(contour, True) / (2 * np.pi))

                if min_radius <= radius <= max_radius:
                    detected_circles.append((center, radius))

                    # 원 그리기
                    cv2.circle(frame, center, radius, (0, 255, 0), 2)
                    # 원의 중심 좌표 표시
                    cv2.circle(frame, center, 2, (0, 0, 255), -1)
            

        #cv2.imshow('Result', frame)
        #cv2.imshow('masked', yellow_mask)
        
        
        return 1
    
    
    
    def par4_direction(self, show=False):
        
        
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 230, 230])

        yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
        yellow_objects = cv2.bitwise_and(frame, frame, mask=yellow_mask)

        cv2.imshow('Yellow Objects', yellow_objects)

        blurred_frame = cv2.GaussianBlur(yellow_objects, (5, 5), 0)
        gray_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow('Blurred Image', gray_frame)

        _, binary_frame = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        cv2.imshow('Binary Image', binary_frame)

        # 침식과 팽창 적용
        kernel = np.ones((5, 5), np.uint8)
        binary_frame = cv2.erode(binary_frame, kernel, iterations=1)
        binary_frame = cv2.dilate(binary_frame, kernel, iterations=1)

        cv2.imshow('erode and dilate', binary_frame)

        contours, _ = cv2.findContours(binary_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        max_area = 0  # 가장 큰 노란색 물체의 면적
        max_area_contour = None  # 가장 큰 노란색 물체의 컨투어

        for contour in contours:
            area = cv2.contourArea(contour)

            if area > max_area:
                max_area = area
                max_area_contour = contour

        if max_area_contour is not None:
            M = cv2.moments(max_area_contour)
            if M["m00"] != 0:
                center_x = int(M["m10"] / M["m00"])
                center_y = int(M["m01"] / M["m00"])

                # 노란색 물체의 크기에 따라 초록색 원 그리기
                radius = int(max_area ** 0.5 / 2)
                cv2.circle(frame, (center_x, center_y), radius, (0, 255, 0), 2)
                # 중심 좌표 표시
                cv2.circle(frame, (center_x, center_y), 2, (0, 0, 255), -1)

                # 중심 좌표가 초록색 원 안에 있는지 확인
                if center_x - radius >= 0 and center_x + radius < frame.shape[1] and center_y - radius >= 0 and center_y + radius < frame.shape[0]:
                    # 노란색 물체의 중심이 초록색 원 안에 있을 때, 초록색 원을 그림
                    cv2.circle(frame, (center_x, center_y), radius, (0, 255, 0), 2)

        #cv2.imshow('Result', frame)
        #cv2.imshow('masked', yellow_mask)
    
        return 1




    