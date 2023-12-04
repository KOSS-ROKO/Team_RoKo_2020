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
            #cv2.imshow("imageProcessor-get_img", img)
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

        
        # inside dongbang
        # imgThreshLow = cv2.inRange(imgHSV, (0, 100, 100), (10, 255, 255))
        # imgThreshHigh = cv2.inRange(imgHSV, (160, 40, 50), (179, 255, 255))
        # outside dongbang
        # imgThreshLow = cv2.inRange(imgHSV, (0, 100, 100), (10, 255, 255))
        # imgThreshHigh = cv2.inRange(imgHSV, (160, 100, 100), (179, 255, 255))
        imgThreshLow = cv2.inRange(imgHSV, (0, 40, 120), (10, 155, 255))
        imgThreshHigh = cv2.inRange(imgHSV, (160, 50, 100), (179, 255, 255))
    

        # imgThreshLow = cv2.inRange(imgHSV, (0, 150, 60), (24, 255, 255))
        # imgThreshHigh = cv2.inRange(imgHSV, (150, 50, 60), (179, 255, 255))
        # imgThreshLow = cv2.inRange(imgHSV, (0, 150, 60), (10, 255, 255))
        # imgThreshHigh = cv2.inRange(imgHSV, (160, 150, 150), (179, 255, 255))
        # imgThreshLow = cv2.inRange(imgHSV, (0, 40, 160), (10, 255, 255))
        # imgThreshHigh = cv2.inRange(imgHSV, (160, 130, 200), (179, 255, 255))
        # minju dongbang
        # imgThreshLow = cv2.inRange(imgHSV, (0, 120, 130), (10, 255, 255))
        # imgThreshHigh = cv2.inRange(imgHSV, (165, 100, 100), (180, 255, 255))
        # minju dongbang22

        # self.upper_red1 = np.array([10, 255, 255])
        # self.lower_red1 = np.array([0, 180, 60]) 
        # self.upper_red2 = np.array([180, 230, 230]) 
        # self.lower_red2 = np.array([150, 70, 60])
        # imgThreshLow = cv2.inRange(imgHSV, self.lower_red1, self.upper_red1)
        # imgThreshHigh = cv2.inRange(imgHSV, self.lower_red2, self.upper_red2)

        # 445
        # imgThreshLow = cv2.inRange(imgHSV, (0, 80, 210), (17, 120, 255))
        # imgThreshHigh = cv2.inRange(imgHSV, (160, 30, 200), (180, 200, 255))

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
        # #outside dongbang    
        # lower_yellow = np.array([10, 54, 130])
        # upper_yellow = np.array([40, 250, 255])
        lower_yellow = np.array([10, 80, 110])
        upper_yellow = np.array([36, 230, 255])
        #inside dongbang
        # lower_yellow = np.array([0, 71, 122])
        # upper_yellow = np.array([36, 250, 250])
        
        # lower_yellow = np.array([10, 30, 20])
        # upper_yellow = np.array([40, 255, 255])
        # minju dongbang
        # lower_yellow = self.lower_yellow
        # upper_yellow = self.upper_yellow

        # 445
        # lower_yellow = np.array([10, 100, 170])
        # upper_yellow = np.array([36, 250, 255])
        
        yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
        yellow_objects = cv2.bitwise_and(frame, frame, mask=yellow_mask)
        
        blurred_frame = cv2.GaussianBlur(yellow_objects, (5, 5), 0)
        gray_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2GRAY)
        _, binary_frame = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        kernel = np.ones((5, 5), np.uint8)
        binary_frame = cv2.erode(binary_frame, kernel, iterations=1)
        binary_frame = cv2.dilate(binary_frame, kernel, iterations=1)
        contours, _ = cv2.findContours(binary_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)       
                    
        
        if (role=="call_TF"):  ## 홀컵 인식이 됐나요? 안 됐나요?
            if cv2.countNonZero(binary_frame) > 50: # 값 바꾸세요
                print("holecup TTTTTTTTTTrue")
                return True 
            else:
                return False
            
        elif (role=="call_video"):
            return binary_frame 
        
        
        elif (role=="call_toppoint"):
            y_max, x_max = np.unravel_index(binary_frame.argmax(), binary_frame.shape)
            return (x_max, y_max)
        
        elif (role=="call_midpoint"): ## 홀컵의 가장 아래 좌표 return
            
            bottom_point = (0,0)
            max_area = 0  # 가장 큰 노란색 물체의 면적
            max_area_contour = None  # 가장 큰 노란색 물체의 컨투어
            for contour in contours: 
                area = cv2.contourArea(contour)
                if area > max_area:
                    max_area = area
                    max_area_contour = contour
                    # 최대 영역의 물체 중 가장 아래의 좌표 찾기
                    x, y, w, h = cv2.boundingRect(max_area_contour)
                    bottom_point = (x + w // 2, y + h)           
            
            if contours is not None:
                cv2.circle(frame, bottom_point, 3, (0, 255, 0), 2)
                return bottom_point
            else:
                return None
    
    '''
    def detect_ball(self, role="call_TF"):
        origin = self.get_img()
        frame = origin.copy()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
        red_mask = cv2.inRange(hsv_frame, self.lower_red2, self.upper_red2)
        mask = cv2.erode(red_mask, None, iterations=1)
        mask = cv2.dilate(mask, None, iterations=1)
        mask = cv2.GaussianBlur(mask, (3,3), 2)
        is_red_object = False
        contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]      
        if contours:
            c = max(contours, key=cv2.contourArea)
            Area = cv2.contourArea(c) / self.min_area[1]
            if Area > self.min_area[1]:
                x, y, w, h = cv2.boundingRect(c)
                a, b, c, d = (x+w/2,y),(x+w,y+h/2),(x+w/2,y+h),(x,y+h/2)
                #up right down left 
                is_red_object, red_object_center = True, (x+w/2,y+h)
            else:
                is_red_object, red_object_center = False, None
        else:
            is_red_object, red_object_center = False, None
                 
        # is_red_object = False
        # c = max(contours, key=cv2.contourArea)
        # Area = cv2.contourArea(c) / self.min_area[1]
        
        # if Area > self.min_area[1]:
        #         x, y, w, h = cv2.boundingRect(c)
        #         a, b, c, d = (x+w/2,y),(x+w,y+h/2),(x+w/2,y+h),(x,y+h/2)
        #         #up right down left 
        #         is_red_object, red_object_center = True, (x+w/2,y+h)
        # else:
        #     is_red_object = False
        

        if(role=="call_TF"):
            return is_red_object
            
        elif(role=="call_video"):
            return mask
        
        elif(role=="call_midpoint"):
            return red_object_center
        
        elif(role == "call_4point"):
            return  a[1],b[0],c[1],d[0]
    
    
    
    def detect_holecup(self, role="call_TF"): # detect_holecup_area인데 detect_holecup으로 잠시 이름 바꿨음
        
        print("detect holecup start")

        origin = self.get_img()
        frame = origin.copy()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
        is_yellow_object = False
        yellow_mask = cv2.inRange(hsv_frame, self.lower_yellow, self.upper_yellow)
        mask = cv2.erode(yellow_mask, None, iterations=1)
        mask = cv2.dilate(mask, None, iterations=1)
        mask = cv2.GaussianBlur(mask, (3,3), 2)
        
        contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]   

        if contours:
            c = max(contours, key=cv2.contourArea)
            Area = cv2.contourArea(c) / self.min_area[1]
            if Area > self.min_area[1]:
                x, y, w, h = cv2.boundingRect(c)
                a, b, c, d = (x+w/2,y),(x+w,y+h/2),(x+w/2,y+h),(x,y+h/2)
                #up right down left 
                is_yellow_object, yellow_object_center = True, (x+w/2,y+h)
            else:
                is_yellow_object, yellow_object_center = False, None     
        else:
            is_yellow_object, yellow_object_center = False, None   
                
                
        
        if (role=="call_TF"):  ## 홀컵 인식이 됐나요? 안 됐나요?
            return is_yellow_object
            
        elif (role=="call_video"):
            return mask 
        
        elif (role=="call_midpoint"): ## 홀컵의 가장 아래 좌표 return
            if is_yellow_object:
                return yellow_object_center
            else:
                return None

        elif (role == "call_4point"):
            return a[1],b[0],c[1],d[0]
        
        '''
        
    #########################################
    #########################################
    ############## BALL MIDDLE ##############
    #########################################
    #########################################
        
        
        
    def middle_lr_ball(self):
                
        # 빨간색 객체 추출
        red_point = self.detect_ball("call_midpoint")
        
        if red_point == None:
            return None
        
        x_center = red_point[0]
        y_center = red_point[1]
        
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
            if abs(red_center[0] - yellow_center[0]) <= 150:
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
        
    # def field(self):
    #     # return left and right 
    #     origin = self.get_img()
    #     frame = origin.copy()
    
    #     # HSV 색상 공간으로 변환합니다.
    #     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)

    #     # 색상 범위를 정의합니다.
    #     lower_red1 = self.lower_red1  # 빨간색 최소값 (Hue: 0)
    #     upper_red1 = self.upper_red1  # 빨간색 최대값 (Hue: 50)
    #     lower_red2 = self.lower_red2  # 빨간색 최소값 (Hue: 160)
    #     upper_red2 = self.upper_red2  # 빨간색 최대값 (Hue: 179)
    #     lower_yellow = self.lower_yellow  # 노란색 최소값 (Hue: 20)
    #     upper_yellow = self.upper_yellow  # 노란색 최대값 (Hue: 30)
    #     lower_green = self.lower_green  # 초록색 최소값 (Hue: 30)
    #     upper_green = self.upper_green  # 초록색 최대값 (Hue: 85)
    #     #범위가 이상해요
    #     lower_pink = np.array([300, 50, 50])  # 핑크색 최소값 (예: 색조: 300, 채도: 50, 명도: 50)
    #     upper_pink = np.array([330, 255, 255])  # 핑크색 최대값 (예: 색조: 330, 채도: 255, 명도: 255)

    #     # 각 색상에 대한 마스크를 만듭니다.
    #     mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    #     mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    #     mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    #     mask_green = cv2.inRange(hsv, lower_green, upper_green)
    #     mask_pink = cv2.inRange(hsv, lower_pink, upper_pink)

    #     # 모든 색상의 마스크를 합칩니다.
    #     combined_mask = cv2.add(mask_red1, mask_red2)
    #     combined_mask = cv2.add(combined_mask, mask_yellow)
    #     combined_mask = cv2.add(combined_mask, mask_green)
    #     combined_mask = cv2.add(combined_mask, mask_pink)

    #     # 경계를 찾습니다.
    #     contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #     # 내부 영역을 검정색으로 처리합니다.
    #     mask = np.zeros_like(combined_mask)
    #     cv2.drawContours(mask, contours, -1, (255,60,200), cv2.FILLED)
    #     mask = cv2.bitwise_not(mask)

    #     # 마스크를 이용하여 프레임을 업데이트합니다.
    #     frame = cv2.bitwise_and(frame, frame, mask=mask)

    #     # 화면을 왼쪽과 오른쪽으로 나눕니다.
    #     left_half = frame[:, :self.width // 2]
    #     right_half = frame[:, self.width // 2:]

    #     # 왼쪽 영역과 오른쪽 영역의 블랙 넓이를 계산합니다.
    #     left_black_area = cv2.countNonZero(cv2.inRange(left_half, (0, 0, 0), (0, 0, 0)))
    #     right_black_area = cv2.countNonZero(cv2.inRange(right_half, (0, 0, 0), (0, 0, 0)))

    #     # 블랙 넓이에 따라 'go right' 또는 'go left'를 출력합니다.
    #     # 왼오 넓이 비슷할때, go left하기위해 +1000 정도 오차 범위 넣음 -> 추후 수정
    #     if left_black_area +1000 >= right_black_area:
    #         result = 'left'
    #     else:
    #         result = 'right'

    #     # 결과 프레임을 표시합니다.
    #     # cv2.putText(frame, result, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    #     #cv2.imshow('Combined Color Detection', frame)
    #     return result
    #     #print(left_black_area, right_black_area, result)


        
    #########################################
    #########################################
    ############### HOLE IN #################
    #########################################
    #########################################
        
    '''
    def detect_hole_in(self):
        try:
            hup,hright, hdown,hleft = self.detect_holecup("call_4point")
            rup,rright,rdown,rleft = self.detect_ball("call_4point")
            print(hup,hright, hdown,hleft)
            print(rup,rright,rdown,rleft)
            if hup <= rup <= rdown <= hdown and hleft <= rleft <= rright <= hright:
                return True
            else:
                return False 
        except Exception as e:
            return "Error"

    '''

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
                            diameter = 2 * abs(left_point_yellow[1] - down_point_yellow[1]) + 15
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