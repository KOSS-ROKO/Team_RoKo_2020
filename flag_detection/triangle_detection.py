import cv2
import numpy as np

cap = cv2.VideoCapture('ballandflag.mp4')  

while(1):
    ret, src = cap.read()
    dst = src.copy()
    dst = cv2.resize(dst,(450,700))


    hsv = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([40, 255, 255])
    gray = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # 가장자리 검출
    edges = cv2.Canny(gray, 210, 210)


    #깃대 검출 
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=70, minLineLength = 90, maxLineGap =20)


    # 검출된 선분 그리기
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(dst, (x1, y1), (x2, y2), (0, 0, 255), 2)

    cv2.imshow('Result', dst)

    if cv2.waitKey(1) & 0xFF == 27:
        break    # ESC 누르면 종료

cv2.destroyAllWindows()
