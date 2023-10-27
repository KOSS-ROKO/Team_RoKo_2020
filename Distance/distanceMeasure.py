import cv2
import numpy as np

# 빨간 공의 크기 (미터 단위로)
W = 0.04  # 예시로 10cm로 가정합니다04

# 빨간 공의 이미지에서의 가로 크기 (픽셀 단위로)
w = None  # 초점 거리 계산 후 설정합니다.

cap = cv2.VideoCapture('Distance/ball_video/ball150.avi')  

while True:
    # 프레임 읽기
    ret, frame = cap.read()
    
    if not ret:
        print("비디오 종료")
        break
    
    
    
    '''
    ##################### 노란 홀컵 인식
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
    '''
    
    
    
    ##################### 빨간 공 인식

    
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    imgThreshLow = cv2.inRange(imgHSV, (0, 200, 155), (50, 255, 255))
    imgThreshHigh = cv2.inRange(imgHSV, (160, 125, 50), (179, 255, 255))
    
    imgThresh = cv2.add(imgThreshLow, imgThreshHigh)

    imgThresh = cv2.GaussianBlur(imgThresh, (3, 3), 2)
    imgThresh = cv2.erode(imgThresh, np.ones((5, 5), np.uint8))
    imgThresh = cv2.dilate(imgThresh, np.ones((5, 5), np.uint8))

    red_detected = cv2.bitwise_and(frame, frame, mask=imgThresh)

    

    # 빨간 공의 가로 크기를 측정 (w)
    contours, _ = cv2.findContours(imgThresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)

        
        print("this is w :", w)

    # 초점 거리(f) 계산
    if w is not None:
        #f = (w * 30) / W 
        # 실제 거리(d) 계산
        d = (W * 450) / w
        #print("this is focal lenght:", f)
        print("빨간 공까지의 거리 (미터):", d)

    # 결과 화면 표시
    cv2.imshow('Original', frame)
    cv2.imshow('Red Detected', red_detected)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# 작업 완료 후 리소스 해제
cap.release()
cv2.destroyAllWindows()