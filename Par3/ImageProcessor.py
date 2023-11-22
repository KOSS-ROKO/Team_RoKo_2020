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
        # img.set(3, 640)
        # img.set(4, 480)
        # img.set(5, 5)
        # cv2.imshow("imageProcessor-get_img", img)
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
    
    
    def detect_ball(self, role="call_TF"):
        
        
        origin = self.get_img()
        frame = origin.copy()

                
        imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        

        # imgThreshLow = cv2.inRange(imgHSV, (0, 100, 100), (10, 255, 255))
        # imgThreshHigh = cv2.inRange(imgHSV, (160, 100, 100), (179, 255, 255))
        
        imgThreshLow = cv2.inRange(imgHSV, (0, 50, 60), (10, 200, 200))
        imgThreshHigh = cv2.inRange(imgHSV, (150, 50, 60), (179, 200, 200))
        
        imgThresh = cv2.add(imgThreshLow, imgThreshHigh)

        imgThresh = cv2.GaussianBlur(imgThresh, (3, 3), 2)
        imgThresh = cv2.erode(imgThresh, np.ones((5, 5), np.uint8))
        imgThresh = cv2.dilate(imgThresh, np.ones((5, 5), np.uint8))
        

        if(role=="call_TF"):  
            if cv2.countNonZero(imgThresh) > 30: # 값 바꾸세요
                return True 
            else:
                return False
            
        elif(role=="call_video"):
            return imgThresh
        
        elif(role=="call_midpoint"):

            red_contours, _ = cv2.findContours(imgThresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if red_contours:
                red_max_contour = max(red_contours, key=cv2.contourArea)
                M = cv2.moments(red_max_contour)
                if M["m00"] != 0:
                    red_center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])) 
                    #print(red_center)     
                    return red_center
            else:
                return None

    
    
    
    def detect_holecup(self, role="call_TF"): # detect_holecup_area인데 detect_holecup으로 잠시 이름 바꿨음
        
        print("detect holecup start")

        origin = self.get_img()
        frame = origin.copy()

        
        
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # lower_yellow = np.array([0, 71, 122])
        # upper_yellow = np.array([36, 250, 250])
        
        lower_yellow = np.array([20, 30, 80])
        upper_yellow = np.array([36, 250, 250])

        yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
        yellow_objects = cv2.bitwise_and(frame, frame, mask=yellow_mask)
        
        blurred_frame = cv2.GaussianBlur(yellow_objects, (5, 5), 0)
        gray_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2GRAY)


        _, binary_frame = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        kernel = np.ones((5, 5), np.uint8)
        binary_frame = cv2.erode(binary_frame, kernel, iterations=1)
        binary_frame = cv2.dilate(binary_frame, kernel, iterations=1)

        contours, _ = cv2.findContours(binary_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        
        ##### distance 할 때만 필요.
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            
        

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
                    
                    

        
        if (role=="call_TF"):  ## 홀컵 인식이 됐나요? 안 됐나요?
            if cv2.countNonZero(binary_frame) > 50: # 값 바꾸세요
                #print("holecup true")
                return True 
            else:
                return False
            
        elif (role=="call_video"): ## 홀컵의 w 크기 return
            return binary_frame 
        
        elif (role=="call_midpoint"): ## 홀컵의 중앙 좌표 return

            if max_area_contour is not None:
                M = cv2.moments(max_area_contour)
                if M["m00"] != 0:
                    center_x = int(M["m10"] / M["m00"])
                    center_y = int(M["m01"] / M["m00"])

                    # 노란색 물체의 크기에 따라 초록색 원 그리기
                    # radius = int(max_area ** 0.5 / 2)
                    # cv2.circle(frame, (center_x, center_y), radius, (0, 255, 0), 2)
                    # 중심 좌표 표시
                    # cv2.circle(frame, (center_x, center_y), 2, (0, 0, 255), -1)

                    # 중심 좌표가 초록색 원 안에 있는지 확인
                    if center_x - radius >= 0 and center_x + radius < frame.shape[1] and center_y - radius >= 0 and center_y + radius < frame.shape[0]:
                        # 노란색 물체의 중심이 초록색 원 안에 있을 때, 초록색 원을 그림
                        cv2.circle(frame, (center_x, center_y), radius, (0, 255, 0), 2)

                    return (center_x, center_y)
                
                else:
                    return None


        


    #########################################
    #########################################
    ############# PAR4_DIRECTION ############
    #########################################
    #########################################
    
    
    
    def par4_direction(self):
        
        origin = self.get_img()
        frame = origin.copy()
        
        
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 230, 230])

        yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
        yellow_objects = cv2.bitwise_and(frame, frame, mask=yellow_mask)
        

        blurred_frame = cv2.GaussianBlur(yellow_objects, (5, 5), 0)
        gray_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2GRAY)


        _, binary_frame = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        #cv2.imshow('Binary Image', binary_frame)

        # 침식과 팽창 적용
        kernel = np.ones((5, 5), np.uint8)
        binary_frame = cv2.erode(binary_frame, kernel, iterations=1)
        binary_frame = cv2.dilate(binary_frame, kernel, iterations=1)


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
        
        
        
    def middle_lr_ball(self):
        print("middle_lr_ball")
                
        # 빨간색 객체 추출
        red_point = self.detect_ball("call_midpoint")
        
        if red_point == None:
            return None
        
        x_center = red_point[0]
        y_center = red_point[1]
        
        cell_width = 640 // 11

        # 빨간 공이 중앙 세로줄인 6번째 줄에서 검출되면 "stop" 출력
        if (cell_width * 6 <= x_center <= cell_width * 7):
            print("stop")
            return "stop"
        # 1~5번째 줄에서 검출되면 "go right" 출력
        elif x_center < cell_width * 6:
            print("right")
            return "right"
        # 7~11번째 줄에서 검출되면 "go left" 출력
        elif x_center > cell_width * 7:
            print("left")
            return "left"
    # else:
    #     print("go far")
    #     return "go far"



    def middle_ud_ball(self):
            
        # 빨간색 객체 추출
        red_point = self.detect_ball("call_midpoint")
        
        if red_point == None:
            return None
        
        x_center = red_point[0]
        y_center = red_point[1]
        
        cell_height = 480 // 13

        # 빨간 공이 중앙 가로줄인 6번째 줄에서 검출되면 "stop" 출력
        if (cell_height * 6 <= y_center <= cell_height * 7):
            return "stop"
        # 1~5번째 줄에서 검출되면 "go up" 출력
        elif y_center < cell_height * 6:
            return "up"
        # 7~11번째 줄에서 검출되면 "go down" 출력
        elif y_center > cell_height * 7:
            return "down"
    # else:
    #     print("go far")

    
    def middle_lr_holecup(self):
        print("middle_lr_holecup")
        
        
        # 빨간색 객체 추출
        yellow_point = self.detect_holecup("call_midpoint")
        
        if yellow_point == None:
            return None

        x_center = yellow_point[0]
        y_center = yellow_point[1]
        
        cell_width = 640 // 11

        # 빨간 공이 중앙 세로줄인 6번째 줄에서 검출되면 "stop" 출력
        if (cell_width * 5 <= x_center <= cell_width * 6):
            print("stop")
            return "stop"
        # 1~5번째 줄에서 검출되면 "go right" 출력
        elif x_center < cell_width * 5:
            print("right")
            return "right"
        # 7~11번째 줄에서 검출되면 "go left" 출력
        elif x_center > cell_width * 6:
            print("left")
            return "left"
    # else:
    #     print("go far")
    #     return "go far"



    def middle_ud_holecup(self):
        
        yellow_point = self.detect_holecup("call_midpoint")
        
        if yellow_point == None:
            return None
        
        x_center = yellow_point[0]
        y_center = yellow_point[1]
        
        cell_height = 480 // 13
        
        # 빨간 공이 중앙 가로줄인 6번째 줄에서 검출되면 "stop" 출력
        if (cell_height * 6 <= y_center <= cell_height * 7):
            return "stop"
        # 1~5번째 줄에서 검출되면 "go up" 출력
        elif y_center < cell_height * 6:
            return "up"
        # 7~11번째 줄에서 검출되면 "go down" 출력
        elif y_center > cell_height * 7:
            return "down"
        # else:
        #     return "go far"




    #########################################
    #########################################
    ########## ball_hole_straight ###########
    #########################################
    #########################################
    
    '''
    def ball_hole_straight(self):
        #여기서 cv로 일직선 판단 
        # return left right middle
        # 리턴값은 head.py의 straight로 넘어감


        # red_center = self.detect_ball("call_midpoint")
        # if not red_center:
        #     print("red no")
        yellow_center = self.detect_holecup("call_midpoint")
        if not yellow_center:
            print("yellow no")

                
        # 빨간색 물체가 왼쪽에 있는지 오른쪽에 있는지 판별
        if yellow_center:
            if 300 <= yellow_center[0] <= 340 :
                result = "middle"
            elif yellow_center[0] < 300:
                result = "left"
            else:
                result = "right"
        else:
            result = "none"

        return result
    
    '''
    
    # < Straight 원본 >

    def ball_hole_straight(self):
        #여기서 cv로 일직선 판단 
        # return left right middle
        # 리턴값은 head.py의 straight로 넘어감


        red_center = self.detect_ball("call_midpoint")
        if not red_center:
            print("red no")
        yellow_center = self.detect_holecup("call_midpoint")
        if not yellow_center:
            print("yellow no")

                
        # 빨간색 물체가 왼쪽에 있는지 오른쪽에 있는지 판별
        if red_center and yellow_center:
            if abs(red_center[0] - yellow_center[0]) < 10:
                result = "middle"

            elif red_center[0] < yellow_center[0]:
                
                result = "left"
            else:
                result = "right"
        else:
            result = "none"

        return result
            
    
        
    #########################################
    #########################################
    ############### ONEFRAME ################
    #########################################
    #########################################
        
        
    def ball_hole_oneframe(self):       
        
        r_TF = self.detect_ball("call_TF")
        y_TF = self.detect_holecup("call_TF")
        
        if r_TF == True and y_TF == True:
            return True
        else:
            return False

        '''
        # 노란색 물체를 찾았고 크기가 최소 크기 이상인지 검사
        if y_contours and cv2.contourArea(max(y_contours, key=cv2.contourArea)) >= min_yellow_size \
            and r_contours and cv2.contourArea(max(r_contours, key=cv2.contourArea)) >= min_red_size:
            return True
        else:
            return False
            
        '''
        
    #########################################
    #########################################
    ###############  FIELD  #################
    #########################################
    #########################################    
        
    def field(self):
        # return left and right 
        origin = self.get_img()
        frame = origin.copy()
    
        # HSV 색상 공간으로 변환합니다.
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 색상 범위를 정의합니다.
        lower_red1 = np.array([0, 70, 40])  # 빨간색 최소값 (Hue: 0)
        upper_red1 = np.array([50, 255, 255])  # 빨간색 최대값 (Hue: 50)
        lower_red2 = np.array([150, 60, 40])  # 빨간색 최소값 (Hue: 160)
        upper_red2 = np.array([179, 255, 255])  # 빨간색 최대값 (Hue: 179)
        lower_yellow = np.array([20, 70, 40])  # 노란색 최소값 (Hue: 20)
        upper_yellow = np.array([30, 255, 255])  # 노란색 최대값 (Hue: 30)
        lower_green = np.array([30, 70, 40])  # 초록색 최소값 (Hue: 30)
        upper_green = np.array([85, 255, 255])  # 초록색 최대값 (Hue: 85)
        lower_pink = np.array([300, 50, 50])  # 핑크색 최소값 (예: 색조: 300, 채도: 50, 명도: 50)
        upper_pink = np.array([330, 255, 255])  # 핑크색 최대값 (예: 색조: 330, 채도: 255, 명도: 255)

        # 각 색상에 대한 마스크를 만듭니다.
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        mask_pink = cv2.inRange(hsv, lower_pink, upper_pink)

        # 모든 색상의 마스크를 합칩니다.
        combined_mask = cv2.add(mask_red1, mask_red2)
        combined_mask = cv2.add(combined_mask, mask_yellow)
        combined_mask = cv2.add(combined_mask, mask_green)
        combined_mask = cv2.add(combined_mask, mask_pink)

        # 경계를 찾습니다.
        contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 내부 영역을 검정색으로 처리합니다.
        mask = np.zeros_like(combined_mask)
        cv2.drawContours(mask, contours, -1, (255,60,200), cv2.FILLED)
        mask = cv2.bitwise_not(mask)

        # 마스크를 이용하여 프레임을 업데이트합니다.
        frame = cv2.bitwise_and(frame, frame, mask=mask)

        # 화면을 왼쪽과 오른쪽으로 나눕니다.
        left_half = frame[:, :self.width // 2]
        right_half = frame[:, self.width // 2:]

        # 왼쪽 영역과 오른쪽 영역의 블랙 넓이를 계산합니다.
        left_black_area = cv2.countNonZero(cv2.inRange(left_half, (0, 0, 0), (0, 0, 0)))
        right_black_area = cv2.countNonZero(cv2.inRange(right_half, (0, 0, 0), (0, 0, 0)))

        # 블랙 넓이에 따라 'go right' 또는 'go left'를 출력합니다.
        # 왼오 넓이 비슷할때, go left하기위해 +1000 정도 오차 범위 넣음 -> 추후 수정
        if left_black_area +1000 >= right_black_area:
            result = 'left'
        else:
            result = 'right'

        # 결과 프레임을 표시합니다.
        # cv2.putText(frame, result, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        #cv2.imshow('Combined Color Detection', frame)
        return result
        #print(left_black_area, right_black_area, result)


        
    #########################################
    #########################################
    ############### HOLE IN #################
    #########################################
    #########################################
        
        
    def detect_hole_in(self):
        
        origin = self.get_img()
        frame = origin.copy()
        
        try:
            
            binary_frame = self.detect_holecup("call_video")
            
            contours, _ = cv2.findContours(binary_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # 노란색 홀컵 윤곽선
            
            
            ##### 가장 왼쪽과 오른쪽, 위쪽 아래쪽 점 찾기
            
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
                
                
                
            #############여기서부터 빨간공
            
            
            # 빨간공 인식
            imgThresh = self.detect_ball("call_video")

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
            if left_point_yellow is not None and left_point_yellow is not None:
                A, A_prime = left_point_yellow[0], right_point_yellow[0]
                B, B_prime = left_point_red[0], right_point_red[0]

                C, C_prime = up_point_yellow[1], down_point_yellow[1]
                D, D_prime = up_point_red[1], down_point_red[1]
                
                #if A < B < A_prime and A < B_prime < A_prime and C < D < C_prime and C < D_prime < C_prime:
                if A < B < B_prime < A_prime and C < D < D_prime < C_prime:
                    hole_result = True 
                else:
                    hole_result = False
            else:
                hole_result = False 
            return hole_result     
        
        except Exception as e:
            return "Error"