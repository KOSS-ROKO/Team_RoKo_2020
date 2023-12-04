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

    # lower_red_low = np.array([0, 100, 155])
    # upper_red_low = np.array([50, 255, 255])

    # lower_red_high = np.array([160, 40, 50])
    # upper_red_high = np.array([179, 255, 255])
    
    # imgThreshLow = cv2.inRange(imgHSV, lower_red_low, upper_red_low)
    # imgThreshHigh = cv2.inRange(imgHSV, lower_red_high, upper_red_high)
    last_values = {'yellow_low_h': 10, 'yellow_high_h': 36, 'yellow_low_s': 99,
                    'yellow_high_s': 255, 'yellow_low_v': 128, 'yellow_high_v': 255}

    lower_yellow = np.array([10, 99, 128])
    upper_yellow = np.array([36, 255, 255])
    imgThreshLow = cv2.inRange(imgHSV, lower_yellow, upper_yellow)
    imgThreshHigh = cv2.inRange(imgHSV, lower_yellow, upper_yellow)
    
    imgThresh = cv2.bitwise_or(imgThreshLow, imgThreshHigh)
    red_contours, _ = cv2.findContours(imgThresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.imshow("d",imgThresh)
    if red_contours:
        red_max_contour = max(red_contours, key=cv2.contourArea)

        M = cv2.moments(red_max_contour)
        if M["m00"] != 0:
            red_center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            return red_center

def top_point(image):
    imgHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    upper_yellow = np.array([40, 250, 255])
    lower_yellow = np.array([10, 54, 130])
    mask = cv2.inRange(imgHSV, lower_yellow, upper_yellow)
    # yellow_part = cv2.bitwise_and(frame, frame, mask=mask)
    # yellow_gray = cv2.cvtColor(yellow_part, cv2.COLOR_BGR2GRAY)
    yellow_mask = cv2.inRange(imgHSV, lower_yellow, upper_yellow)
    yellow_objects = cv2.bitwise_and(frame, frame, mask=yellow_mask)
    
    blurred_frame = cv2.GaussianBlur(yellow_objects, (5, 5), 0)
    gray_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2GRAY)
    _, binary_frame = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    kernel = np.ones((5, 5), np.uint8)
    binary_frame = cv2.erode(binary_frame, kernel, iterations=1)
    binary_frame = cv2.dilate(binary_frame, kernel, iterations=1)
        
    
    
    cv2.imshow("tp", binary_frame)
    
    y_max, x_max = np.unravel_index(binary_frame.argmax(), binary_frame.shape)

    return x_max,y_max

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
    tp = top_point(frame)
    print(" tp : ",tp)
    if red_center:
        #print("빨간색 공의 중심 좌표:", red_center)
        #print(red_center)
        cv2.circle(frame, red_center, 2, (255, 0, 0), -1)
        cv2.circle(frame, tp, 2, (0,0,255),3)
        cv2.imshow(window_name, frame)
    if clicked_point:
        cv2.putText(frame, f'Clicked Point: {clicked_point}', (10, H_View_size - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC Key
        break

cap.release()
cv2.destroyAllWindows()