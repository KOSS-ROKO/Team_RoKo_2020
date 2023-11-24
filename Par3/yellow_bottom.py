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
    
    lower_yellow = np.array([0, 71, 122])
    upper_yellow = np.array([36, 250, 250])

    yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
    yellow_objects = cv2.bitwise_and(frame, frame, mask=yellow_mask)
    
    blurred_frame = cv2.GaussianBlur(yellow_objects, (5, 5), 0)
    gray_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2GRAY)


    _, binary_frame = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    kernel = np.ones((5, 5), np.uint8)
    binary_frame = cv2.erode(binary_frame, kernel, iterations=1)
    binary_frame = cv2.dilate(binary_frame, kernel, iterations=1)

    contours, _ = cv2.findContours(binary_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        
    ##### distance 할 때만 필요.
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        
    

    max_area = 0  # 가장 큰 노란색 물체의 면적
    max_area_contour = None  # 가장 큰 노란색 물체의 컨투어

    for contour in contours: 
        area = cv2.contourArea(contour)

        if area > max_area:
            max_area = area
            max_area_contour = contour
            # 최대 영역의 물체 중 가장 아래의 좌표 찾기
            x, y, w, h = cv2.boundingRect(max_area_contour)
            bottom_point = (x + w // 2, y + h)  # 사각형의 가장 아래 중심 좌표로 설정

    if bottom_point is not None:
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
             
    #elif (role=="call_midpoint"): ## 홀컵의 중앙 좌표 return
                print(center_x, center_y)
        
        else:
            #return None
            print("else4")


    cv2.imshow('Original', frame)
    cv2.imshow('Red Detected', binary_frame)
    
    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 작업 완료 후 리소스 해제
cap.release()
cv2.destroyAllWindows()
