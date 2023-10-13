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




class ImageProcessor:
    def __init__(self, video= ""):
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



    #########################################
    #########################################
    ################ DETECTION ##############
    #########################################
    #########################################
    
    
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

        
        if cv2.countNonZero(imgThresh) > 0: # 값 바꾸세요
            return True 
        else:
            return False
        
        

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



    ############################################
    ##### detect holecup for new distance ######
    ############ return x  y  w  h #############
    ############################################

    def detect_holecup_xywh():
        
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

        ##### 홀 컵 점4개 찾기
        # 가장 왼쪽과 오른쪽, 위쪽 아래쪽 점 찾기
        xx, yy, ww, hh =0,0,0,0
        
        left_point_yellow, right_point_yellow = None, None
        up_point_yellow, down_point_yellow = None, None
        
        if contours:
            for contour in contours:
                for point in contour:
                    x = point[0][0]
                    y = point[0][1]

                    # 가장 왼쪽점 업데이트
                    if left_point_yellow is None or x < left_point_yellow[0]:
                        left_point_yellow = [x, y]

                    # 가장 오른쪽점 업데이트
                    if right_point_yellow is None or x > right_point_yellow[0]:
                        right_point_yellow = [x, y]

                    # 가장 아래점 업데이트
                    if down_point_yellow is None or y > down_point_yellow[1]:
                        down_point_yellow = [x, y]

                    diameter = 0
                    # 가장 위쪽점 업데이트
                    if down_point_yellow is not None:
                        diameter = 2 * abs(left_point_yellow[1] - down_point_yellow[1]) - 20

                    # 제일 위쪽 점 계산
                    up_point_yellow = [down_point_yellow[0], down_point_yellow[1] - diameter]


        result = frame.copy()
        if left_point_yellow is not None:
            cv2.circle(result, tuple(left_point_yellow), 5, (0, 0, 255), -1)
        if right_point_yellow is not None:
            cv2.circle(result, tuple(right_point_yellow), 5, (0, 0, 255), -1)

        if up_point_yellow is not None:
            cv2.circle(result, tuple(up_point_yellow), 5, (0, 0, 255), -1)
        if down_point_yellow is not None:
            cv2.circle(result, tuple(down_point_yellow), 5, (0, 0, 255), -1)
            
        #### x, y, w, h 계산     
        ww = right_point_yellow[0] - left_point_yellow[0]
        hh = down_point_yellow[1] - up_point_yellow[1]
        # print("lr: ",left_point_yellow, right_point_yellow)
        # print("ud: ", up_point_yellow, down_point_yellow)
        # print(left_point_yellow[0], up_point_yellow[1] ,ww, hh)

        return (left_point_yellow[0], up_point_yellow[1] ,ww, hh)

       

    
    
    
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
        
        
        
        
        
        
    #########################################
    #########################################
    ############## BALL MIDDLE ##############
    #########################################
    #########################################
        
        
        
    def middle_lr_ball(): #### origin 고치기 
        
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
        # else:
        #     print("go far")
        #     return "go far"




    #########################################
    #########################################
    ########## ball_hole_straight ###########
    #########################################
    #########################################
    
    
    def ball_hole_straight():
        #여기서 cv로 일직선 판단 
        # return left right middle
        # 리턴값은 head.py의 straight로 넘어감
        
        pass
    
    
        
        
    #########################################
    #########################################
    ############### ONEFRAME ################
    #########################################
    #########################################
        
        
    def ball_hole_oneframe():
        
        origin = ImageProcessor.get_img()
        frame = origin.copy()
    
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
        min_yellow_size = 10000 # 이 수치는 프레임 크기에 따라서 나중에 조정 필요할듯요 
        min_red_size = 1000

        # 노란색 물체를 찾았고 크기가 최소 크기 이상인지 검사
        if y_contours and cv2.contourArea(max(y_contours, key=cv2.contourArea)) >= min_yellow_size \
            and r_contours and cv2.contourArea(max(r_contours, key=cv2.contourArea)) >= min_red_size:
            return True
        else:
            return False
        
        
        
    #########################################
    #########################################
    ############### HOLE IN #################
    #########################################
    #########################################
        
        
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
            
            blurred_frame = cv2.GaussianBlur(yellow_objects, (5, 5), 0)
            gray_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2GRAY)
            
            _, binary_frame = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            
            # 이미지 전처리 - 침식, 팽창
            kernel = np.ones((5, 5), np.uint8)
            binary_frame = cv2.erode(binary_frame, kernel, iterations=1)
            binary_frame = cv2.dilate(binary_frame, kernel, iterations=1)
            
            cv2.imshow('Yellow Holecup Binary Image', binary_frame) # 이진화된 이미지 표시
            
            contours, _ = cv2.findContours(binary_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # 노란색 홀컵 윤곽선
            
            
            ##### 가장 왼쪽과 오른쪽, 위쪽 아래쪽 점 찾기
            
            left_point_y, right_point_y = None, None
            up_point_yellow, down_point_yellow = None, None
            
            if contours:
                for contour in contours:
                    for point in contour:
                        x = point[0][0]
                        y = point[0][1]

                        # 가장 왼쪽점 업데이트
                        if left_point_yellow is None or x < left_point_yellow[0]:
                            left_point_yellow = [x, y]

                        # 가장 오른쪽점 업데이트
                        if right_point_yellow is None or x > right_point_yellow[0]:
                            right_point_yellow = [x, y]

                        # 가장 아래점 업데이트
                        if down_point_yellow is None or y > down_point_yellow[1]:
                            down_point_yellow = [x, y]

                        diameter = 0
                        # 가장 위쪽점 업데이트
                        if down_point_yellow is not None:
                            diameter = 2 * abs(left_point_yellow[1] - down_point_yellow[1]) - 20

                        # 제일 위쪽 점 계산
                        up_point_yellow = [down_point_yellow[0], down_point_yellow[1] - diameter]


            result = frame.copy()
            if left_point_yellow is not None:
                cv2.circle(result, tuple(left_point_yellow), 5, (0, 0, 255), -1)
            if right_point_yellow is not None:
                cv2.circle(result, tuple(right_point_yellow), 5, (0, 0, 255), -1)

            if up_point_yellow is not None:
                cv2.circle(result, tuple(up_point_yellow), 5, (0, 0, 255), -1)
            if down_point_yellow is not None:
                cv2.circle(result, tuple(down_point_yellow), 5, (0, 0, 255), -1)
                
                
                
            #############여기서부터 빨간공
            
            
            # 빨간공 인식
            imgThresh = ImageProcessor.detect_ball(frame)

            cv2.imshow('Red Ball Binary Image', imgThresh) # 이진화된 이미지 표시
                
            contours, _ = cv2.findContours(imgThresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # 빨간색 골프 공 윤곽선
            
            
            ##### 가장 왼쪽과 오른쪽, 위쪽과 아래쪽 점 찾기

            left_point_red, right_point_red = None, None
            up_point_red, down_point_red = None, None
            
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

                        # 가장 위쪽점 업데이트
                        if up_point_red is None or y_red < up_point_red[1]:
                            up_point_red = [x_red, y_red]

                        # 가장 아래쪽점 업데이트
                        if down_point_red is None or y_red > down_point_red[1]:
                            down_point_red = [x_red, y_red]


            if left_point_red is not None:
                cv2.circle(result, tuple(left_point_red), 5, (0, 255, 0), -1)
            if right_point_red is not None:
                cv2.circle(result, tuple(right_point_red), 5, (0, 255, 0), -1)
                
            if up_point_red is not None:
                cv2.circle(result, tuple(up_point_red), 5, (0, 255, 0), -1)
            if down_point_red is not None:
                cv2.circle(result, tuple(down_point_red), 5, (0, 255, 0), -1)  



            ##### 홀인 여부 판단
            if left_point_y is not None and right_point_y is not None:
                A, A_prime = left_point_y[0], right_point_y[0]
                B, B_prime = left_point_red[0], right_point_red[0]

                C, C_prime = left_point_yellow[1], right_point_yellow[1]
                D, D_prime = left_point_red[1], right_point_red[1]
                
                if A < B < A_prime and A < B_prime < A_prime and C < D < C_prime and C < D_prime < C_prime:
                    hole_result = True
                else:
                    hole_result = False
            else:
                hole_result = False
                
            return hole_result        
        
        except Exception as e:
            return "Error"