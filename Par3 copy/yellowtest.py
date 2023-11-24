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
    
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # lower_yellow = np.array([0, 71, 122])
    # upper_yellow = np.array([36, 250, 250])
    
    # lower_yellow = np.array([15, 100, 100])
    # upper_yellow = np.array([30, 255, 255])

    # minju dongbang
    lower_yellow = np.array([10, 60, 150])
    upper_yellow = np.array([36, 200, 255])


    yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
    yellow_objects = cv2.bitwise_and(frame, frame, mask=yellow_mask)
    
    blurred_frame = cv2.GaussianBlur(yellow_objects, (5, 5), 0)
    gray_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2GRAY)


    _, binary_frame = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    kernel = np.ones((5, 5), np.uint8)
    binary_frame = cv2.erode(binary_frame, kernel, iterations=1)
    binary_frame = cv2.dilate(binary_frame, kernel, iterations=1)


    
    cv2.imshow('Original', frame)
    cv2.imshow('Red Detected', binary_frame)
    
    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 작업 완료 후 리소스 해제
cap.release()
cv2.destroyAllWindows()
