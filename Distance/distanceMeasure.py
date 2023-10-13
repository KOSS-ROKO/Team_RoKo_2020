import cv2
import numpy as np

# 빨간 공의 크기 (미터 단위로)
W = 0.04  # 예시로 10cm로 가정합니다.

# 빨간 공의 이미지에서의 가로 크기 (픽셀 단위로)
w = None  # 초점 거리 계산 후 설정합니다.

cap = cv2.VideoCapture('Distance/ball_video/ball60.avi')  

while True:
    # 프레임 읽기
    ret, frame = cap.read()
    
    if not ret:
        print("비디오 종료")
        break
    
    
    '''
    
    ##################### 노란 홀컵 인식
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
    
    '''
    
            
    ##################### 빨간 공 인식

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 빨간색 범위를 정의
    lower_red = np.array([150, 90, 40])
    upper_red = np.array([190, 255, 255])

    # HSV 이미지에서 빨간색 마스크 생성
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # 원본 이미지에서 마스크로 빨간색 부분 추출
    red_detected = cv2.bitwise_and(frame, frame, mask=mask)


    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # 객체 검출 (컨투어 사용)


    # 빨간 공의 가로 크기를 측정 (w)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        print("this is w : ", w)

    # 초점 거리(f) 계산
    if w is not None:
        #f = (w * 30) / W  q
        # 실제 거리(d) 계산
        d = (W * 250) / w
        #print("this is focal lenght:", f)
        print("빨간 공까지의 거리 (미터):", d)

    # 결과 화면 표시
    cv2.imshow('Original', frame)
    cv2.imshow('Red Detected', red_detected)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 작업 완료 후 리소스 해제
cap.release()
cv2.destroyAllWindows()