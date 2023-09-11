import cv2
import numpy as np

cap = cv2.VideoCapture('trianglevideo.mp4')  

while(1):
    ret, src = cap.read()
    dst = src.copy()
    dst = cv2.resize(dst,(800,500))


    hsv = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([40, 255, 255])
    gray = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # 가장자리 검출
    edges = cv2.Canny(gray, 130, 160)


    # 윤곽선 검출
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 삼각형 검출을 위한 루프
    for contour in contours:
        # 윤곽선 근사화
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
    
        # 근사화된 윤곽선의 꼭지점 개수 확인 (삼각형은 꼭지점이 3개)
        if len(approx) == 3:
            # 삼각형 윤곽선을 그리기
            cv2.drawContours(dst, [approx], 0, (0, 255, 0), 2)

    cv2.imshow('edge', edges)
    cv2.imshow('Result', dst)

    if cv2.waitKey(1) & 0xFF == 27:
        break    # ESC 누르면 종료

cv2.destroyAllWindows()
