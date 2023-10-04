# 타원검출해서 홀컵 찾기 
# 홀컵 기본 인식 때 쓰일 예정1

import cv2
import numpy as np

cap = cv2.VideoCapture('Flag/flag_video/flag2.avi')

detected_circles = []

while True:
    ret, frame = cap.read()

    if not ret:
        break

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 33, 144, 144
    lower_yellow = np.array([25, 80, 50])
    upper_yellow = np.array([36, 250, 250])

    yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
    yellow_objects = cv2.bitwise_and(frame, frame, mask=yellow_mask)

    # 노란색 객체 표시
    cv2.imshow('Yellow Objects', yellow_objects)

    # Gaussian Blur를 사용하여 노이즈 제거
    blurred_frame = cv2.GaussianBlur(yellow_objects, (5, 5), 0)
    gray_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2GRAY)

    # 블러된 이미지 표시
    cv2.imshow('Blurred Image', gray_frame)

    # 이진화를 사용하여 노란색 물체 강조
    _, binary_frame = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # 이진화된 이미지 표시
    cv2.imshow('Binary Image', binary_frame)

    # 침식과 팽창을 사용하여 이미지를 보정
    kernel = np.ones((5, 5), np.uint8)
    binary_frame = cv2.erode(binary_frame, kernel, iterations=1)
    binary_frame = cv2.dilate(binary_frame, kernel, iterations=1)

    # 침식과 팽창된 이미지 표시
    # cv2.imshow('Eroded and Dilated Image', binary_frame)

    # edges = cv2.Canny(binary_frame, 50, 150)  # 에지 검출 (Canny 사용)

    # 에지 이미지 표시
    # cv2.imshow('Edges', edges)

    contours, _ = cv2.findContours(binary_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # 객체 검출 (컨투어 사용)



    
    detected_circles = []  # 감지된 원의 정보를 저장할 리스트 초기화

    # 검출된 원 정보 저장
    for contour in contours:
        min_radius = 20
        max_radius = 160
        epsilon = 0.01 * cv2.arcLength(contour, True) # 엡실론 값 조정
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) >= 8:
            center, _ = cv2.minEnclosingCircle(contour)
            center = tuple(map(int, center))
            radius = int(cv2.arcLength(contour, True) / (2 * np.pi))

            if min_radius <= radius <= max_radius:
                detected_circles.append((center, radius))

                # 원 그리기
                cv2.circle(frame, center, radius, (0, 255, 0), 2)
                # 원의 중심 좌표 표시
                cv2.circle(frame, center, 2, (0, 0, 255), -1)
        

    cv2.imshow('Result', frame)
    cv2.imshow('masked', yellow_mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 


cap.release()
cv2.destroyAllWindows()

