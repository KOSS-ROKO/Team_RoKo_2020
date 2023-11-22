# -*- coding: utf-8 -*-
from Robo import Robo
from Head import Head
from Motion import Motion
import Distance
import cv2
import numpy as np
import os
import time
import platform
from imutils.video import WebcamVideoStream
from imutils.video import FileVideoStream
from imutils.video import FPS

ACT = "TEESFOTA"
# TEESHOTA = 1          # 1. 맨 처음 티샷  
# TEESHOTB = 2
# WALK_BALL = 3        # 2. 공까지 걸어가기 (걸음수)
# PUTTING_POS = 4      # 3. 퍼팅 위치에 서기
# PUTTING = 5          # 4. 퍼팅
# HOLEIN = 6           # 5. 홀인




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

    #frame.set(3, 640)
    #frame.set(4, 480)
    #frame.set(5, 5)
    cv2.imshow('frame', frame)
            
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # imgThreshLow = cv2.inRange(imgHSV, (0, 50, 155), (50, 255, 255))
    # imgThreshHigh = cv2.inRange(imgHSV, (160, 50, 50), (179, 255, 255))

    imgThreshLow = cv2.inRange(imgHSV, (0, 100, 100), (10, 255, 255))
    imgThreshHigh = cv2.inRange(imgHSV, (160, 100, 100), (179, 255, 255))
    
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

    lower_yellow = np.array([0, 71, 122])
    upper_yellow = np.array([36, 250, 250])

    yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
    yellow_objects = cv2.bitwise_and(frame, frame, mask=yellow_mask)
    
    blurred_frame = cv2.GaussianBlur(yellow_objects, (5, 5), 0)
    gray_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2GRAY)


    _, binary_frame = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    #cv2.imshow('Binary Image', binary_frame)

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
        
    elif (role=="call_w"): ## 홀컵의 w 크기 return
        return w 
    
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
        # 노란색 홀컵 검출
        yellow_lower = np.array([0, 50, 100])
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
        
#=======================================================#
#                        Head def                       #         
#=======================================================#
def big_UD(object="ball"):
    big_ud_angle = 100
    # big UD head
    while True:
        is_object_in_frame, Distance.Head_ud_angle = head.big_UD_head(object, big_ud_angle)
        if is_object_in_frame == True:
            return "Success"
        elif is_object_in_frame == False:
            big_ud_angle = Distance.Head_ud_angle
        
            if Distance.Head_ud_angle == 64: # Distance.Head_UD_Middle_Value_Measures - 100 + 10 + 45:  # big ud 한 사이클이 끝남. / 9는 바뀔 수 있는 값
                #Distance.Head_ud_angle = Distance.Head_UD_Middle_Value_Measures # 고개값을 다시 정면100으로 
                #go_to = "big_lr"  # LR로 갈지 구분
                return "Except"
            else: 
                continue
                
                
def big_LR(object="ball"):
    Distance.head_lr_angle = 100
    max_right_flag = 0
    print("THis is ", object)
    # big LR head
    while True:
        is_object_in_frame, small_lr_temp, max_right_flag = head.big_LR_head(object, Distance.head_lr_angle, max_right_flag)
        if is_object_in_frame == True:
            break
        elif is_object_in_frame == False:
            Distance.head_lr_angle = small_lr_temp
            print("head_lr_angle : ", Distance.head_lr_angle)
            continue
        #if big_lr_angle == -90: #왼쪽 max까지 갔는데 공 못찾으면 
            #head.big_UD_head()
            # 예외처리 : big up down 코드
    #고개 정면 코드 추가하기

def ball_small_LR(object="ball"):   # ball은 small lr끝난뒤 몸 돌리고 고개 default함
    Distance.head_lr_angle = 100
    while True:
        print("---------start small lr head")
        is_vertical_middle, small_lr_temp = head.small_LR_head(object, Distance.head_lr_angle)
        if is_vertical_middle == True:
            return "Success" #break

        elif is_vertical_middle == False:
            Distance.head_lr_angle = small_lr_temp
            continue
        else : # is_vertical_middle == Except_
            return "Except"
        
def small_LR(object="ball"):    # ball은 small lr끝난뒤 몸, 고개 그대로, 끝.
    #Distance.head_lr_angle = 100
    while True:
        print("---------start small lr head")
        is_vertical_middle, small_lr_temp = head.small_LR_head(object, Distance.head_lr_angle)
        if is_vertical_middle == True:
            return "Success" #break

        elif is_vertical_middle == False:
            Distance.head_lr_angle = small_lr_temp
            continue
        else : # is_vertical_middle == Except_
            return "Except"
                    

def UD_for_dist(object="ball"): # small ud head 변형
    small_ud_angle = Distance.Head_UD_Middle_Value_Measures
    # 거리를 위한 고개 각도 내리기 
    while True:
        print("---------start ud for dist")
        is_horizontal_middle, small_ud_temp = head.head_for_dist(object, small_ud_angle)
        if is_horizontal_middle == True: #최종 중앙 맞춰짐 
            #act = "PUTTING_POS 
            #variable.Head_ud_angle = 
            Distance.Head_ud_angle = small_ud_temp
            print(Distance.Head_ud_angle)
            break
        elif is_horizontal_middle == False:
            small_ud_angle = small_ud_temp
            Distance.Head_ud_angle = small_ud_temp
            continue

def holecup_UD_for_dist(): # small ud head 변형
    small_ud_angle = 10
    
    # 거리를 위한 고개 각도 올리기 
    while True:
        print("---------start HOlECUP ud for dist")
        is_horizontal_middle, small_ud_temp = head.head_for_dist("holecup", small_ud_angle)
        if is_horizontal_middle == True: #최종 중앙 맞춰짐 
            #act = "PUTTING_POS 
            #variable.Head_ud_angle = 
            Distance.Head_ud_angle = small_ud_temp
            print("holecup ud angle : ",Distance.Head_ud_angle)
            break
        elif is_horizontal_middle == False:
            if small_ud_angle > small_ud_temp : # 홀컵중점 바껴서 갇히는 현상 해결
                Distance.Head_ud_angle = small_ud_temp  #(상관없) 더 최근 고개값 = 더 먼 거리값
                break
            small_ud_angle = small_ud_temp
            Distance.Head_ud_angle = small_ud_temp

            continue
    
    
def is_point_inside_rectangle(point, rectangle):
    x, y = point
    x1, y1, x2, y2, x3, y3, x4, y4 = rectangle
    return x1 <= x <= x2 and y1 <= y <= y4


# 좌표가 사각형 밖에 있다면 기준 좌표로부터 얼마나 떨어져 있는지 계산하는 함수 정의
def calculate_distance_from_reference(center, reference):
    cx, cy = center
    rx, ry = reference
    dx = cx - rx
    dy = cy - ry
    return dx, dy



if __name__ == '__main__':
    while True:    
        #=======================================================#
        #                      1. Teeshot A                     #         
        #=======================================================#

        if ACT == "TEESHOTA":                 ##### 1. 시작 및 티샷 #################
            print("ACT: ", ACT, "Teeshot A") # Debug

            is_ball = robo._image_processor.detect_ball()

            ### False면, big UD LR 해라
            if is_ball == False:                
                while True:
                    # big UD head
                    is_big_UD = big_UD("ball")

                    #if go_to == "big_lr" :
                    if is_big_UD == "Except" :  # big UD 검출안됨 -> big LR 로 넘어감
                        big_LR("ball")  # big은 알아서 고개 디폴트 함 
                    
                    is_small_LR = ball_small_LR("ball")
                    
                    if is_small_LR == "Except" :
                        motion.head("DEFAULT", 2) # small_LR 한 후 고개 디폴트
                        # big 알고리즘으로 넘어감
                        # is_big_LR = big_LR("ball") 하러 처음으로 올라감 
                        big_LR("ball") # 이거 한번만 실행하면 무조건 찾을 거라고 생각해서 while로 안 돌아감.
                    else:
                        break
                    
            else:
                ball_small_LR("ball") # small lr 함으로써 중앙 맞춰짐

            # ud_for_dist 하기전에 고개 세팅
            motion.head("DEFAULT", 2) # 고개 디폴트
            Distance.Head_ud_angle = Distance.Head_UD_Middle_Value_Measures
            motion.head("DEFAULT", 1) # 고개 디폴트
            
            UD_for_dist("ball")
            motion.head("DEFAULT", 1) # ud for dist 이후 고개 상하 디폴트
            time.sleep(2)
            

            # length = 거리 
            ball_dist = Distance.Length_ServoAngle_dict.get(Distance.Head_ud_angle)
            print(Distance.Length_ServoAngle_dict)
            print("==========================================")
            print("ball dist: ", ball_dist , "===========","head angle: ", Distance.Head_ud_angle)
            print("==========================================")



            if ball_dist > 18:
                motion.walk("FORWARD", ball_dist - 18)
                    
            elif ball_dist == 18:
                print("correct!")
            else :      # 최소 거리 18보다 더 가까이 있을 경우: 뒷걸음질
                motion.walk("BACKWARD", ball_dist - 18)

            # PUTTING
            time.sleep(3)
            motion.putting("left", 3, 2)
            print("putting")
            time.sleep(5)


            # turn body left, 몸을 왼쪽으로 90도 돌림.
            motion.turn("LEFT", 60)
            #time.sleep(7)
            motion.turn("LEFT", 60)
            time.sleep(2)
            print("turn LEFT")

            ACT = "WALK_BALL"
            
            motion.walk("FORWARD10", 1)
            time.sleep(15)
            
            # return True
            
            
        #=======================================================#
        #                      1. Teeshot B                     #         
        #=======================================================#


        elif ACT == "TEESHOTB":                 ##### 1. 시작 및 티샷 #################
            print("ACT: ", ACT, "Teeshot B") # Debug
            
            is_ball = robo._image_processor.detect_ball()
            
            ### False면, big UD LR 해라
            if is_ball == False:                
                while True:
                    # big UD head
                    is_big_UD = big_UD("ball")
                    motion.head("DOWN", 9)
                    motion.head("DOWN", 6)
                    Distance.Head_ud_angle -= 15

                    #if go_to == "big_lr" :
                    if is_big_UD == "Except" :  # big UD 검출안됨 -> big LR 로 넘어감
                        big_LR("ball2")  # big은 알아서 고개 디폴트 함 
                    
                    is_small_LR = small_LR("ball2")
                    
                    if is_small_LR == "Except" :
                        motion.head("DEFAULT", 2) # small_LR 한 후 고개 디폴트
                        # big 알고리즘으로 넘어감
                        # is_big_LR = big_LR("ball") 하러 처음으로 올라감 
                        big_LR("ball2") # 이거 한번만 실행하면 무조건 찾을 거라고 생각해서 while로 안 돌아감.
                    else:
                        break
                    
            else:
                small_LR("ball2") # small lr 함으로써 중앙 맞춰짐
                
            point = 0
            if Distance.head_lr_angle <= 80:
                motion.walk_side("LEFT70") # loop문 추가 / 수정 필수
                time.sleep(1)
                motion.walk_side("LEFT70")
                time.sleep(1)
                motion.walk_side("LEFT70")
                time.sleep(1)
                motion.walk_side("LEFT70")
                time.sleep(1)
                motion.pose("RIGHT", True)
                time.sleep(1)
                print("1번 점에서 확인")
                point = 1
            elif Distance.head_lr_angle >= 120:
                motion.walk_side("RIGHT70") # loop문 추가
                time.sleep(1)
                motion.walk_side("RIGHT70")
                time.sleep(1)
                motion.walk_side("RIGHT70")
                time.sleep(1)
                motion.walk_side("RIGHT70")
                time.sleep(1)
                motion.pose("LEFT")
                time.sleep(1)
                print("3번 점에서 확인")
                point = 3
            else:
                print("2번 점에서 확인")
                motion.pose("LEFT", True)
                time.sleep(1)
                point = 2
            
            #-----------------------------------------------------------------------------------------------------

            # ud_for_dist 하기전에 고개 세팅
            motion.head("DEFAULT", 2) # 고개 디폴트
            Distance.Head_ud_angle = Distance.Head_UD_Middle_Value_Measures
            motion.head("DEFAULT", 1) # 고개 디폴트
            
            UD_for_dist("ball")
            motion.head("DEFAULT", 1) # ud for dist 이후 고개 상하 디폴트
            time.sleep(2)
            

            # length = 거리 
            ball_dist = Distance.Length_ServoAngle_dict.get(Distance.Head_ud_angle)
            print(Distance.Length_ServoAngle_dict)
            print("==========================================")
            print("ball dist: ", ball_dist , "===========","head angle: ", Distance.Head_ud_angle)
            print("==========================================")



            if ball_dist > 18:
                motion.walk("FORWARD", ball_dist - 18)
            elif ball_dist == 18:
                print("correct!")
            else :      # 최소 거리 18보다 더 가까이 있을 경우: 뒷걸음질
                motion.walk("BACKWARD", ball_dist - 18)

            
            if point == 1:
                time.sleep(1)
                motion.turn("RIGHT", 15)
                time.sleep(1)
                motion.putting("right", 3)
                time.sleep(5)
                
                motion.turn("RIGHT", 60)
                time.sleep(6)
                motion.turn("RIGHT", 45)
                time.sleep(2)
            elif point == 2:
                time.sleep(1)
                motion.putting("left", 3)
                time.sleep(5)
                
                motion.turn("LEFT", 60)
                time.sleep(6)
                motion.turn("LEFT", 60)
                time.sleep(2)
            elif point == 3:
                time.sleep(1)
                motion.turn("LEFT", 15)
                time.sleep(1)
                motion.putting("left", 3)
                time.sleep(5)
                
                motion.turn("LEFT", 60)
                time.sleep(5)
                motion.turn("LEFT", 60)
                time.sleep(2)
                motion.turn("LEFT", 10)
                time.sleep(2)
                    
            ACT = "WALK_BALL"
            time.sleep(1)
            motion.walk("FORWARD12", 1)
            time.sleep(25)
            
            # return True
                
            '''
            # PUTTING
            time.sleep(3)
            motion.putting("left", 3, 2)
            print("putting")
            time.sleep(5)


            # turn body left, 몸을 왼쪽으로 90도 돌림.
            motion.turn("LEFT", 60)
            time.sleep(7)
            motion.turn("LEFT", 60)
            time.sleep(2)
            print("turn LEFT")

            ACT = "WALK_BALL
            
            motion.walk("FORWARD10", 1)
            time.sleep(15)
            
            return True
            '''

        #=======================================================#
        #                        2. Walk                        #         
        #=======================================================#

        elif ACT == "WALK_BALL": 
        ##### 2. 공을 향해 걸어간다 #################

            print("^^^^222222")
            print("^^^^222222")
            print("^^^^222222")
            print("^^^^222222")
            
            #motion.head("DEFAULT", 1)
            #motion.head("DOWN", 45) # 고개 45도로 내리고 공 detect 시작 !
            #time.sleep(5)

            
            is_ball = robo._image_processor.detect_ball()

            ### False면, big UD LR 해라
            if is_ball == False:                
                while True:
                    # big UD head
                    is_big_UD = big_UD("ball")
                    print("controller === big ud ")

                    #if go_to == "big_lr" :
                    if is_big_UD == "Except" :  # big UD 검출안됨 -> big LR 로 넘어감
                        motion.head("UP", 9) # after Teeshot 고개 60
                        motion.head("UP", 6)
                        big_LR("ball")  # big은 알아서 고개 디폴트 함 
                    
                    is_small_LR = ball_small_LR("ball")
                    
                    if is_small_LR == "Except" :
                        motion.head("DEFAULT", 2) # small_LR 한 후 고개 디폴트
                        big_LR("ball") # 이거 한번만 실행하면 무조건 찾을 거라고 생각해서 while로 안 돌아감.
                    else:
                        break
            else:
                ball_small_LR("ball") # small lr 함으로써 중앙 맞춰짐
            
            # ud_for_dist 하기전에 고개 세팅
            motion.head("DEFAULT", 2) # 고개 디폴트
            Distance.Head_ud_angle = Distance.Head_UD_Middle_Value_Measures
            motion.head("DEFAULT", 1) # 고개 디폴트
            time.sleep(1)
            
            print("ball detected")
            UD_for_dist("ball")
            motion.head("DEFAULT", 1) # ud for dist 이후 고개 상하 디폴트
            time.sleep(2)

            # length = 거리 
            ball_dist = Distance.Length_ServoAngle_dict.get(Distance.Head_ud_angle)
            print("ball distance :", ball_dist)
            

            # 무지성 10번 걸은 후, 남은 거리 측정 후 걷기
            if ball_dist > 26:  # 18+8 (화면에 여유있게 들어오도록)
                motion.walk("FORWARD", ball_dist - 26)
                    
            elif ball_dist == 26:
                print("correct!")
            else :      # 최소 거리 18보다 더 가까이 있을 경우: 뒷걸음질
                motion.walk("BACKWARD", ball_dist - 26)            
            
            
            ACT = "PUTTING_POS"
            
            #return True
            
        #=======================================================#
        #                     3. Putting Pos                    #         
        #=======================================================#
            
        elif ACT == "PUTTING_POS":             ##### 3. 퍼팅 위치에 서기 #################
            ###### 홀컵 중앙 맞추기 #######################
            
            print("^^^^333333")
            print("^^^^333333")
            print("^^^^333333")
            print("^^^^333333")

            motion.head("DOWN", 45) # 고개 45도로 내리고 공 detect 시작 !
            time.sleep(1)
            Distance.Head_UD_Angle = 55
            
            
            is_holecup_in_frame = robo._image_processor.detect_holecup()
            
            motion.head("DEFAULT", 1) # 고개 상하 디폴트
            
            if is_holecup_in_frame == False:    
                print("holecup NONONONONONO")
                # big UD head
                while True:
                    is_big_UD = big_UD("holecup")
                    if is_big_UD == "Except" :  # big UD 검출안됨 -> big LR 로 넘어감
                        print("holecup big UD except")
                        big_LR("holecup")
                        
                    is_small_LR = small_LR("holecup")
                    print("small lr finished")

                    if is_small_LR == "Except" :
                        motion.head("DEFAULT", 2) # small_LR 한 후 고개 디폴트
                        
                        big_LR("holecup") # 이거 한번만 실행하면 무조건 찾을 거라고 생각해서 while로 안 돌아감.
                    else:
                        break

                
                #====== holecup 고개 방향만큼 꽃게 걸음 ======#
                side_walk = int(abs(100-Distance.head_lr_angle)//10) # 식은 시행착오거치면서 변경예정

                print("**꽃게 걸음 시작**")
                # side walk 방향 설정 
                if  Distance.head_lr_angle < 100:
                    # 고개가 왼쪽L이면 오른쪽R으로 side walk해라
                    print("꽃게 걸음 오른쪽")
                    side_lr = "RIGHT"
                elif Distance.head_lr_angle > 100 : 
                    # 고개가 오른쪽R이면 왼쪽L으로 side walk해라
                    print("꽃게 걸음 왼쪽")
                    side_lr = "LEFT"

                print("side walk -------", side_walk)
                # motion.py에 walk_side for문이 없어서 임시로 여기다 넣음
                for _ in range(side_walk):
                    motion.walk_side(side_lr)
                
            motion.head("DEFAULT", 2) # LR 한 후 고개 디폴트
                    
            print("holecup YES")
            ###### 홀컵 찾음, 중앙 맞췄음. 일직선 맞추고, 이제 거리 재야됨

            
            '''
            while True:
                # 공 홀컵 일직선 맞추기 => 홀컵만으로 판별
                print("!!call straight ")
                check_straight = head.straight()
                if check_straight == True: # 거리 알고리즘으로 넘어감
                    print("straight true!!")
                    break
                elif check_straight == "Except":
                    print("straight except")
                    while True:
                        # straight의 Except 처리
                        # 홀컵이 안보이는 경우이므로, 홀컵을 찾는 과정
                        # 문제점 : 홀컵 UD는 몸을 움직이지 않음. 근데 몸 움직여야함ㅠ

                        motion.head("DEFAULT", 1)
                        is_big_UD = big_UD("holecup")
                        
                        if is_big_UD == "Except":
                            big_LR("holecup")
                        is_small_LR = small_LR("holecup")
                        
                        if is_small_LR == "Except" :
                            motion.head("DEFAULT", 2) # small_LR 한 후 고개 디폴트
                            # big 알고리즘으로 넘어감

                            big_LR("holecup") # 이거 한번만 실행하면 무조건 찾을 거라고 생각해서 while로 안 돌아감.
                        else:
                            break
                else:
                    continue   
            '''   

            
            while True:
                # 공 홀컵 일직선 맞추기
                print("!!call straight ")
                check_straight = head.straight()
                if check_straight == True: # 거리 알고리즘으로 넘어감
                    print("straight true!!")
                    break
                elif check_straight == "Except":
                    print("straight except")
                    
                    while True:
                        motion.head("DEFAULT", 1)
                        Distance.Head_ud_angle =100
                        # 매번 고개 디폴트했다가 54도로 갔다가 하는 거
                        is_big_UD = big_UD("ball")
                        
                        if is_big_UD == "Except":
                            big_LR("ball")
                        is_small_LR = ball_small_LR("ball")
                        

                        if is_small_LR == "Except" :
                            motion.head("DEFAULT", 2) # small_LR 한 후 고개 디폴트
                            # big 알고리즘으로 넘어감
                            # is_big_LR = big_LR("ball") 하러 처음으로 올라감 
                            big_LR("ball") # 이거 한번만 실행하면 무조건 찾을 거라고 생각해서 while로 안 돌아감.
                        else:

                            break
                else:
                    continue
                        
                    
                
            ##### straight 알고리즘하다가 중앙이 흐트려졌을 거라 판단하여 -> 중앙 맞추기 시작
            
            ### field 블랙 판별 => 좌우 퍼팅 결정   
            Distance.field = robo._image_processor.field() #return left, right
            Distance.field = "left" ##temp
            #몸 퍼팅 위치에 서기
            if Distance.field == "left" :
                print("field left!!")
                motion.pose("LEFT")
            elif Distance.field == "right" :
                print("field right!!")
                motion.pose("RIGHT")

            
            ''' 홀컵 찾기, 홀컵 거리 재기 안 할 거라 일단 주석처리했음
            
            # 거리 알고리즘    
            # ud_for_dist 하기전에 고개 세팅
            motion.head("DEFAULT", 2) # 고개 디폴트
            Distance.Head_ud_angle = Distance.Head_UD_Middle_Value_Measures
            motion.head("DEFAULT", 1) # 고개 디폴트
            
            motion.head("DOWN", 45)
            time.sleep(2)
            
            # ud_for_dist 하기전에 holecup 찾기
            # holecup찾기 (고개 O, 몸 X)
            while True:
                big_LR("holecup")
                is_small_LR = small_LR("holecup")

                if is_small_LR == "Except" :
                    print("holecup small lr except")
                    motion.head("DEFAULT", 2) # small_LR 한 후 고개 디폴트
                    
                    big_LR("holecup") # 이거 한번만 실행하면 무조건 찾을 거라고 생각해서 while로 안 돌아감.
                else:
                    break
            
            
            motion.head("DOWN", 45)
            Distance.Head_UD_Angle = 10
            holecup_UD_for_dist() # 홀컵 거리 재기
            motion.head("DEFAULT", 1) # ud for dist 이후 고개 상하 디폴트
            time.sleep(2)
                            
            # 홀컵 거리 재기
            Distance.holecup_dist = Distance.Length_ServoAngle_dict.get(Distance.Head_ud_angle)
            
            print("holecup dist : ", Distance.holecup_dist)
            # 이 length를 퍼팅 파워로 바꿔주는 코드 필요 -> 직접해보면서 조절
            '''

            ACT = "PUTTING"


            # 공 거리는 Act 4(PUTTING)에서 재기

            #return True


        #=======================================================#
        #                      4. Putting                       #         
        #=======================================================#

        elif ACT == "PUTTING":             ##### 4. 퍼팅 #################
            
            print("^^^^444444")
            print("^^^^444444")
            print("^^^^444444")
            print("^^^^444444")


            # ud_for_dist 하기전에 고개 세팅
            motion.head("DEFAULT", 2) # 고개 디폴트
            Distance.Head_ud_angle = Distance.Head_UD_Middle_Value_Measures
            motion.head("DEFAULT", 1) # 고개 디폴트

            UD_for_dist("ball") # 공 거리 재기
            motion.head("DEFAULT", 1) # ud for dist 이후 고개 상하 디폴트
            time.sleep(2)

            # length = 거리 
            ball_dist = Distance.Length_ServoAngle_dict.get(Distance.Head_ud_angle)
            print(Distance.Length_ServoAngle_dict)
            print("=====================================")
            print("balL dist:" , ball_dist , " head ud angle:", Distance.Head_ud_angle)
            print("=====================================")
            
            while True:
                print("ball dist :", ball_dist)
                if 16 <= ball_dist <= 20: # 거리 값 조정 필요!
                    break
                elif ball_dist < 16:
                    motion.walk("2JBACKWARD")
                    ball_dist += 2
                elif ball_dist > 20:
                    motion.walk("2JFORWARD")
                    ball_dist -= 2

            time.sleep(3)
            
            ### 건웅 오빠 필독!
            
            motion.head("DEFAULT",63)
            red_center = robo._image_processor.detect_ball("call_midpoint")
            print("++++++++++++++++++")
            print(red_center)
            print("++++++++++++++++++")
            is_center = False
            while not is_center:
                rectangle_coordinates = [388, 140, 422, 140, 422, 180, 388, 180]
                if is_point_inside_rectangle(red_center, rectangle_coordinates):
                    is_center = True
                else:
                    reference_point = [400, 160]
                    dx, dy = calculate_distance_from_reference(red_center, reference_point) # 15에 1cm
                    x,y = dx/2, dy
                    if(abs(dx)>=25):
                        if (dx<0):
                            while(abs(dx)//30):
                                robo._motion.walk_side("LEFT10")
                                time.sleep(1)
                        else:
                            while(abs(dx)//30):
                                robo._motion.walk_side("Right10")
                                time.sleep(1)
                    if(abs(dy)>=25):
                        if (dy<0):
                            while(abs(dy)//30):
                                robo._motion.walk_side("2JBACKWARD")
                                time.sleep(1)
                        else:
                            while(abs(dy)//30):
                                robo._motion.walk_side("2JFORWARD")
                                time.sleep(1)
                        
                    
            ### 퍼팅 직전 공의 위치 정확히 두는 코드 여기 들어가야함! 꽃게걸음으로 좌우 조절 
                
                
            ### 진짜 퍼팅
            motion.putting(Distance.field, 1, 2)
            time.sleep(5)
                
                
            ACT = "HOLEIN"

            motion.turn("LEFT", 45)
            time.sleep(5)
            motion.turn("LEFT", 45)
            time.sleep(3)

            #return True


        elif ACT == "HOLEIN":             ##### 5. 홀인 #################
        
        print("^^^^^^^^5555555")
        print("^^^^^^^^5555555")
        print("^^^^^^^^5555555")
        print("^^^^^^^^5555555")
        
        ###### Find ball for HOLEIN ######
        is_ball = robo._image_processor.detect_ball()

        ### False면, big UD LR 해라
        if is_ball == False:          
            while True:
                print("FAIL ball detect 555")   
                # big UD head
                is_big_UD = big_UD("ball")
                print(" === big ud === for holeIN")

                #if go_to == "big_lr" :
                if is_big_UD == "Except" :  # big UD 검출안됨 -> big LR 로 넘어감
                    print("big ud except 555")
                    # big LR 시행하기전에 UD 45도로
                    motion.head("DOWN", 45)
                    
                    big_LR("ball")  # big은 알아서 고개 디폴트 함 
                
                is_small_LR = ball_small_LR("ball")
                
                if is_small_LR == "Except" :
                    print("small lr except 555")
                    motion.head("DEFAULT", 2) # small_LR 한 후 고개 디폴트
                    # big 알고리즘으로 넘어감
                    # is_big_LR = big_LR("ball") 하러 처음으로 올라감 
                    big_LR("ball") # 이거 한번만 실행하면 무조건 찾을 거라고 생각해서 while로 안 돌아감.
                else:
                    break
        else:
            print("ball detect 555 => small lr할 거야")
            ball_small_LR("ball") # small lr 함으로써 중앙 맞춰짐

        
        oneframe = robo._image_processor.ball_hole_oneframe()
        if oneframe == True:
            print("is oneframe? yesss")
            check_holein = robo._image_processor.detect_hole_in()
            if check_holein == True:
                print("ceremony hehehehehe")
                # 세레모니
                motion.ceremony()
                return True
            else:
                print("holein fail")
                # 몰라. 3번을 더 간단히?
                ACT = "WALK_BALL"
                
                motion.head("DEFAULT", 1)
                time.sleep(1)
                motion.head("DOWN", 45)
                time.sleep(1)

        else:   
            print('go putting pos')
            # 원프레임이 아니라서 다시 WALK BALL로
            ACT = "WALK_BALL"
        
        
        return True