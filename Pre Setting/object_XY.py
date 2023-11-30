import cv2
import numpy as np
import os
import time

def clock():
    return cv2.getTickCount() / cv2.getTickFrequency()

W_View_size = 640
H_View_size = 480
FPS = 5

cap = cv2.VideoCapture(0)
cap.set(3, W_View_size)
cap.set(4, H_View_size)
cap.set(5, 30)

clicked_point = None

def detect_red_color(image):
    imgHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_red_low = np.array([0, 100, 155])
    upper_red_low = np.array([50, 255, 255])

    lower_red_high = np.array([160, 40, 50])
    upper_red_high = np.array([179, 255, 255])

    imgThreshLow = cv2.inRange(imgHSV, lower_red_low, upper_red_low)
    imgThreshHigh = cv2.inRange(imgHSV, lower_red_high, upper_red_high)

    imgThresh = cv2.bitwise_or(imgThreshLow, imgThreshHigh)

    red_contours, _ = cv2.findContours(imgThresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cv2.imshow("d",imgThresh)
    if red_contours:
        red_max_contour = max(red_contours, key=cv2.contourArea)

        M = cv2.moments(red_max_contour)
        if M["m00"] != 0:
            red_center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            return red_center

def on_mouse_click(event, x, y, flags, param):
    global clicked_point
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_point = (x, y)
        print(f'Clicked Point: {clicked_point}')

window_name = "Video Test"
cv2.namedWindow(window_name)
cv2.setMouseCallback(window_name, on_mouse_click)

old_time = clock()

while True:
    time.sleep(1)
    Frame_time = 1000 / ((clock() - old_time) * 1000.)
    old_time = clock()

    ret, frame = cap.read()

    if not ret:
        print("비디오 프레임을 읽을 수 없습니다.")
        break
    red_center = detect_red_color(frame)

    if red_center:
        #print("빨간색 공의 중심 좌표:", red_center)
        print(red_center)
        cv2.circle(frame, red_center, 2, (255, 0, 0), -1)

        cv2.imshow(window_name, frame)

    if clicked_point:
        cv2.putText(frame, f'Clicked Point: {clicked_point}', (10, H_View_size - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC Key
        break

cap.release()
cv2.destroyAllWindows()