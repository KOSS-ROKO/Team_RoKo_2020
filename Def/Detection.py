import cv2
import numpy as np

from Def.VideoCall import ImageProcessor

class Detection:
    def __init__(self):
        pass

    def detect_ball():
        
        origin = ImageProcessor.get_img()
        frame = origin.copy()
        
        imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        imgThreshLow = cv2.inRange(imgHSV, (0, 200, 155), (50, 255, 255))
        imgThreshHigh = cv2.inRange(imgHSV, (160, 155, 50), (179, 255, 255))
        
        imgThresh = cv2.add(imgThreshLow, imgThreshHigh)

        imgThresh = cv2.GaussianBlur(imgThresh, (3, 3), 2)
        imgThresh = cv2.erode(imgThresh, np.ones((5, 5), np.uint8))
        imgThresh = cv2.dilate(imgThresh, np.ones((5, 5), np.uint8))

        red_detected = cv2.bitwise_and(frame, frame, mask=imgThresh)

        
        if cv2.countNonZero(imgThresh) > 100:
            return imgThresh  # 이진화 이미지 리턴
        
        return imgThresh

    def detect_arrow():
        
        origin = ImageProcessor.get_img()
        frame = origin.copy()
        
        lower_yellow = np.array([0, 50, 50])
        upper_yellow = np.array([45, 255, 255])

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # 노란색 화살표 부분 표시
        yellow_arrow = cv2.bitwise_and(frame, frame, mask=yellow_mask)

        # 노란색 화살표의 윤곽선 검출
        contours, hierarchy = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 화살표의 꼭짓점 표시
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 500:  # 화살표로 판단할 최소한의 면적 조건
                # 윤곽선 근사화(복잡한 윤곽선을 간단한 다각형으로 대체)
                epsilon = 0.02 * cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, epsilon, True)  # 다각형 꼭지점 반환

                if len(approx) == 7:  # 화살표로 판단할 근사화 결과의 꼭지점 개수 조건

                    # 화살표 7개 꼭지점의 중간값 찾기
                    center = np.mean(approx, axis=0)
                    center_x = int(round(center[0][0]))
                    center_y = int(round(center[0][1]))
                    cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

                    # 각 점과 중심점 사이의 거리 계산
                    distances = [np.linalg.norm(point - center) for point in approx]

                    # 거리가 가장 먼 두 점의 인덱스 찾기
                    far_indices = np.argsort(distances)[:2]

                    # 가장 가까운 두 꼭지점의 좌표
                    closest_points = [approx[i][0] for i in far_indices]

                    # 가장 가까운 두 꼭지점의 중간값 찾기
                    far_center = np.mean(closest_points, axis=0)
                    far_center_x = int(round(far_center[0]))
                    far_center_y = int(round(far_center[1]))
                    cv2.circle(frame, (far_center_x, far_center_y), 5, (255, 0, 0), -1)

                    #방향 계산
                    arrow_angle = np.arctan2(far_center_y - center_y, far_center_x - center_x)
                    angle = np.degrees(arrow_angle)

                    font = cv2.FONT_HERSHEY_SIMPLEX
                    if -45 <= angle < 45:
                        #cv2.putText(frame, 'RIGHT', (10, 85), font, 1, (255, 255, 0))
                        return 'RIGHT'
                    elif 45 <= angle < 135:
                        #cv2.putText(frame, 'DOWN', (10, 85), font, 1, (255, 255, 0))
                        return 'DOWN'
                    elif -180 <= angle <= -135:
                        #cv2.putText(frame, 'LEFT', (10, 85), font, 1, (255, 255, 0))
                        return 'LEFT'
                    elif 135 <= angle <= 180:
                        cv2.putText(frame, 'LEFT', (10, 85), font, 1, (255, 255, 0))
                        return 'LEFT'
                    elif -135 < angle < -45:
                        #cv2.putText(frame, 'UP', (10, 85), font, 1, (255, 255, 0))
                        return 'UP'
                return False
                    

    
    def detect_field():
        
        origin = ImageProcessor.get_img()
        frame = origin.copy()

        # HSV 색상 공간으로 변환합니다.
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 경기장 초록색만 검출하기 위한 색상 범위
        # 경기장 색깔 범위 HSV : 색조, 채도, 명도
        lower_green = np.array([30, 70, 40])  # 초록색 최소값
        upper_green = np.array([85, 255, 255])  # 초록색 최대값

        # 초록색 영역을 마스킹합니다.
        mask = cv2.inRange(hsv, lower_green, upper_green)

        # 경계를 찾습니다.
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 경계를 그립니다.
        cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

        # 결과 프레임을 표시합니다.
        cv2.imshow('Edge Detection', frame)
        
        return 1

    
    
    
    
    def detect_holecup_area():
        
        origin = ImageProcessor.get_img()
        frame = origin.copy()
        
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
        
        return (center_x, center_y)

            
        

    
    
    def detect_holecup_circle():
        
        origin = ImageProcessor.get_img()
        frame = origin.copy()
        
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
        
        
        return center
    
    
    
    def par4_direction():
        
        origin = ImageProcessor.get_img()
        frame = origin.copy()
        
        
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
    
        return (center_x, center_y)
        
        