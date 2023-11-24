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

    # imgThreshLow = cv2.inRange(imgHSV, (0, 40, 160), (10, 255, 255))
    # imgThreshHigh = cv2.inRange(imgHSV, (160, 130, 200), (179, 255, 255))

    # minju dongbang
    imgThreshLow = cv2.inRange(imgHSV, (0, 120, 130), (10, 255, 255))
    imgThreshHigh = cv2.inRange(imgHSV, (165, 100, 100), (180, 255, 255))

    # red_lower = np.array([165, 100, 170])
    # red_upper = np.array([180, 230, 255])


    
    imgThresh = cv2.add(imgThreshLow, imgThreshHigh)

    imgThresh = cv2.GaussianBlur(imgThresh, (3, 3), 2)
    imgThresh = cv2.erode(imgThresh, np.ones((5, 5), np.uint8))
    imgThresh = cv2.dilate(imgThresh, np.ones((5, 5), np.uint8))

    red_detected = cv2.bitwise_and(frame, frame, mask=imgThresh)

    
    cv2.imshow('Original', frame)
    cv2.imshow('Red Detected', red_detected)
    
    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 작업 완료 후 리소스 해제
cap.release()
cv2.destroyAllWindows()
