# 빨간색 hsv로만 공 인식했더라면 low, high를 나누고 팽창 침식 필터링 추가

import cv2
import numpy as np
from ImageProcessor import ImageProcessor

cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)
cap.set(5, 5)



def detect_ball(role="call_TF"):
        

            
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    

    imgThreshLow = cv2.inRange(imgHSV, (0, 100, 100), (10, 255, 255))
    imgThreshHigh = cv2.inRange(imgHSV, (160, 20, 100), (179, 255, 255))
    
    # imgThreshLow = cv2.inRange(imgHSV, (0, 150, 60), (24, 255, 255))
    # imgThreshHigh = cv2.inRange(imgHSV, (150, 50, 60), (179, 255, 255))

    # imgThreshLow = cv2.inRange(imgHSV, (0, 150, 60), (10, 255, 255))
    # imgThreshHigh = cv2.inRange(imgHSV, (160, 150, 150), (179, 255, 255))

    # imgThreshLow = cv2.inRange(imgHSV, (0, 40, 160), (10, 255, 255))
    # imgThreshHigh = cv2.inRange(imgHSV, (160, 130, 200), (179, 255, 255))

    # minju dongbang
    # imgThreshLow = cv2.inRange(imgHSV, (0, 120, 130), (10, 255, 255))
    # imgThreshHigh = cv2.inRange(imgHSV, (165, 100, 100), (180, 255, 255))
    
    imgThresh = cv2.add(imgThreshLow, imgThreshHigh)

    imgThresh = cv2.GaussianBlur(imgThresh, (3, 3), 2)
    imgThresh = cv2.erode(imgThresh, np.ones((5, 5), np.uint8))
    imgThresh = cv2.dilate(imgThresh, np.ones((5, 5), np.uint8))

    
    cv2.imshow("red", imgThresh)

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
            
            
def detect_holecup(role="call_TF"): # detect_holecup_area인데 detect_holecup으로 잠시 이름 바꿨음
        
    print("detect holecup start")



    
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # lower_yellow = np.array([0, 71, 122])
    # upper_yellow = np.array([36, 250, 250])
    
    # lower_yellow = np.array([10, 30, 20])
    # upper_yellow = np.array([40, 255, 255])

    # minju dongbang
    # lower_yellow = np.array([10, 60, 150])
    # upper_yellow = np.array([36, 200, 255])

    lower_yellow = np.array([0, 40, 122])
    upper_yellow = np.array([40, 250, 255])

    yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
    yellow_objects = cv2.bitwise_and(frame, frame, mask=yellow_mask)
    
    blurred_frame = cv2.GaussianBlur(yellow_objects, (5, 5), 0)
    gray_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2GRAY)


    _, binary_frame = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    kernel = np.ones((5, 5), np.uint8)
    binary_frame = cv2.erode(binary_frame, kernel, iterations=1)
    binary_frame = cv2.dilate(binary_frame, kernel, iterations=1)

    cv2.imshow("yellow", yellow_objects)

    contours, _ = cv2.findContours(binary_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)       
                

    
    if (role=="call_TF"):  ## 홀컵 인식이 됐나요? 안 됐나요?
        if cv2.countNonZero(binary_frame) > 50: # 값 바꾸세요
            print("holecup TTTTTTTTTTrue")
            return True 
        else:
            return False
        
    elif (role=="call_video"):
        return binary_frame 
    
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




def ball_hole_straight():
    #여기서 cv로 일직선 판단 
    # return left right middle
    # 리턴값은 head.py의 straight로 넘어감


    red_center = detect_ball("call_midpoint")
    if not red_center:
        print("red no")
    yellow_center = detect_holecup("call_midpoint")
    if not yellow_center:
        print("yellow no")

            
    # 빨간색 물체가 왼쪽에 있는지 오른쪽에 있는지 판별
    if red_center and yellow_center:
        print("Red ", red_center[0], "// Yellow ", yellow_center[0])
        if abs(red_center[0] - yellow_center[0]) < 10:
            result = "middle"

        elif red_center[0] < yellow_center[0]:
            
            result = "left"
        else:
            result = "right"
    else:
        print("none")
        result = "none"

    return result
            
            
while True:
    # 프레임 읽기
    ret, frame = cap.read()
    
    print("hi")
    ball_hole_straight()
    
    
    cv2.imshow('Original', frame)
    #cv2.imshow('Red Detected', red_detected)
    
    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 작업 완료 후 리소스 해제
cap.release()
cv2.destroyAllWindows()
