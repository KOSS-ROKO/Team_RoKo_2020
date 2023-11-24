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

    cv2.imshow("yellow", binary_frame)

    contours, _ = cv2.findContours(binary_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        
    
    bottom_point = (0,0)
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

    if contours is not None:
        cv2.circle(frame, bottom_point, 1, (0, 255, 0), 2)
        print(bottom_point)
             

    else:
        #return None
        print("None")


    cv2.imshow('Original', frame)
    
    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 작업 완료 후 리소스 해제
cap.release()
cv2.destroyAllWindows()
