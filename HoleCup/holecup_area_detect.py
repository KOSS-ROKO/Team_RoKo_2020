# 가장 넓이가 큰 노란색 인식하기
# <홀컵 기본 인식> 때 쓰일 예정 2
### 이 파일이 전처리 값 정확 ###

import cv2
import numpy as np

cap = cv2.VideoCapture('HoleCup/flag_video/flag1.avi')

while True:
    ret, frame = cap.read()

    if not ret:
        break

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

    contours, _ = cv2.findContours(binary_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0  # 가장 큰 노란색 물체의 면적
    max_area_contour = None  # 가장 큰 노란색 물체의 컨투어

    for contour in contours:
        area = cv2.contourArea(contour)

        if area > max_area:
            max_area = area
            max_area_contour = contour

    if max_area_contour is not None:
        M = cv2.moments(max_area_contour)
        if M["m00"] != 0:
            center_x = int(M["m10"] / M["m00"])
            center_y = int(M["m01"] / M["m00"])

            # 노란색 물체의 크기에 따라 초록색 원 그리기
            radius = int(max_area ** 0.5 / 2)
            cv2.circle(frame, (center_x, center_y), radius, (0, 255, 0), 2)
            # 중심 좌표 표시
            cv2.circle(frame, (center_x, center_y), 2, (0, 0, 255), -1)

            # 중심 좌표가 초록색 원 안에 있는지 확인
            if center_x - radius >= 0 and center_x + radius < frame.shape[1] and center_y - radius >= 0 and center_y + radius < frame.shape[0]:
                # 노란색 물체의 중심이 초록색 원 안에 있을 때, 초록색 원을 그림
                cv2.circle(frame, (center_x, center_y), radius, (0, 255, 0), 2)

    cv2.imshow('Result', frame)
    cv2.imshow('masked', yellow_mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
