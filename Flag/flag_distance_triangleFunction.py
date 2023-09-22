# 삼각함수로 홀컵가지의 거리 측정 - 9/15 오후 3시

import cv2
import numpy as np

cap = cv2.VideoCapture('Flag/flag_video/flag1.avi')
#cap = cv2.VideoCapture('Flag/triangle_function_data/angle10_161.avi')

detected_circles = []

real_distance = 0

def triangle_function():  
    real_distance = 33 / 3**(1/2)     # 로봇 높이 / tan(로봇 고개 내린 각도) 값
    return real_distance  
    
# 19.0531177

while True:
    ret, frame = cap.read()

    if not ret:
        break
    

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 33, 144, 144
    lower_yellow = np.array([0, 80, 50])
    upper_yellow = np.array([36, 250, 250])

    yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
    yellow_objects = cv2.bitwise_and(frame, frame, mask=yellow_mask)

    gray_frame = cv2.cvtColor(yellow_objects, cv2.COLOR_BGR2GRAY) # 노란색 객체를 그레이 스케일로 변환

    edges = cv2.Canny(gray_frame, 50, 150) # 에지 검출 (Canny 사용)
    
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # 객체 검출 (컨투어 사용)
    
    # 카메라 센서 w 크기 측정
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)

    detected_circles = []  # 감지된 원의 정보를 저장할 리스트 초기화

    # 검출된 원 정보 저장
    for contour in contours:
        min_radius = 20
        max_radius = 80
        epsilon = 0.04 * cv2.arcLength(contour, True) # 엡실론 값 조정
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) >= 6:
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
