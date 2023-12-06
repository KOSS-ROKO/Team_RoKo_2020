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

def top_point(image):
    imgHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([10, 80, 110])
    upper_yellow = np.array([36, 230, 255])
    mask = cv2.inRange(imgHSV, lower_yellow, upper_yellow)
    yellow_mask = cv2.inRange(imgHSV, lower_yellow, upper_yellow)
    yellow_objects = cv2.bitwise_and(frame, frame, mask=yellow_mask)
    
    blurred_frame = cv2.GaussianBlur(yellow_objects, (3, 3), 0)  # Adjust kernel size
    gray_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2GRAY)
    _, binary_frame = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    kernel = np.ones((5, 5), np.uint8)
    binary_frame = cv2.erode(binary_frame, kernel, iterations=1)
    binary_frame = cv2.dilate(binary_frame, kernel, iterations=1)
    cv2.imshow("tp", binary_frame)
    
    y_max, x_max = np.unravel_index(binary_frame.argmax(), binary_frame.shape)

    return x_max, y_max

def on_mouse_click(event, x, y, flags, param):
    global clicked_point
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_point = (x, y)
        print(f'Clicked Point: {clicked_point}')

window_name = "Video Test"
cv2.namedWindow(window_name)
cv2.setMouseCallback(window_name, on_mouse_click)

old_time = clock()
skip_frames = 5  # Adjust as needed

while True:
    for _ in range(skip_frames):
        ret, frame = cap.read()

    Frame_time = 1000 / ((clock() - old_time) * 1000.)
    old_time = clock()

    if not ret:
        print("비디오 프레임을 읽을 수 없습니다.")
        break
    tp = top_point(frame)
    print(" tp : ",tp)
    cv2.imshow(window_name, frame)
    if clicked_point:
        cv2.putText(frame, f'Clicked Point: {clicked_point}', (10, H_View_size - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC Key
        break

cap.release()
cv2.destroyAllWindows()
