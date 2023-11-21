# 빨간색 hsv로만 공 인식했더라면 low, high를 나누고 팽창 침식 필터링 추가

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)
cap.set(5, 5)

while True:
    # 프레임 읽기
    ret, frame = cap.read()
    
    # 빨간공 인식
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # imgThreshLow = cv2.inRange(imgHSV, (0, 200, 55), (50, 255, 255))
    # imgThreshHigh = cv2.inRange(imgHSV, (160, 155, 50), (179, 255, 255))

    imgThreshLow = cv2.inRange(imgHSV, (0, 100, 100), (10, 255, 255))
    imgThreshHigh = cv2.inRange(imgHSV, (160, 100, 100), (179, 255, 255))


    
    imgThresh = cv2.add(imgThreshLow, imgThreshHigh)

    imgThresh = cv2.GaussianBlur(imgThresh, (3, 3), 2)
    imgThresh = cv2.erode(imgThresh, np.ones((5, 5), np.uint8))
    imgThresh = cv2.dilate(imgThresh, np.ones((5, 5), np.uint8))

    red_detected = cv2.bitwise_and(frame, frame, mask=imgThresh)
    
    
    
    ''' 원본 코드(hsv 빨간색으로만 인식)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # 빨간색 범위를 정의
    lower_red = np.array([170, 100, 45])
    upper_red = np.array([177, 255, 255])
    
    # HSV 이미지에서 빨간색 마스크 생성
    mask = cv2.inRange(hsv, lower_red, upper_red)
    
    # 원본 이미지에서 마스크로 빨간색 부분 추출
    red_detected = cv2.bitwise_and(frame, frame, mask=mask)
    '''
    
    # 결과 화면 표시
    cv2.imshow('Original', frame)
    cv2.imshow('Red Detected', red_detected)
    
    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 작업 완료 후 리소스 해제
cap.release()
cv2.destroyAllWindows()
