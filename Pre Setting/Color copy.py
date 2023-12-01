import cv2
import numpy as np

# 초기화
mouse_x, mouse_y = 0, 0

# 마우스 이벤트 콜백 함수 정의
def mouse_callback(event, x, y, flags, param):
    global mouse_x, mouse_y
    mouse_x, mouse_y = x, y

# 내장 카메라 열기
cap = cv2.VideoCapture(0)

# 해상도, 프레임 설정
cap.set(3, 640)
cap.set(4, 480)
cap.set(5, 5)

# 윈도우 생성
cv2.namedWindow('Camera')

# 마우스 이벤트 콜백 함수 등록
cv2.setMouseCallback('Camera', mouse_callback)

# 트랙바 초기화
cv2.createTrackbar('Red_Low_H', 'Camera', 0, 255, lambda x: None)
cv2.createTrackbar('Red_High_H', 'Camera', 17, 255, lambda x: None)
cv2.createTrackbar('Red_Low_S', 'Camera', 80, 255, lambda x: None)
cv2.createTrackbar('Red_High_S', 'Camera', 120, 255, lambda x: None)
cv2.createTrackbar('Red_Low_V', 'Camera', 210, 255, lambda x: None)
cv2.createTrackbar('Red_High_V', 'Camera', 255, 255, lambda x: None)

cv2.createTrackbar('Yellow_Low_H', 'Camera', 10, 255, lambda x: None)
cv2.createTrackbar('Yellow_High_H', 'Camera', 36, 255, lambda x: None)
cv2.createTrackbar('Yellow_Low_S', 'Camera', 100, 255, lambda x: None)
cv2.createTrackbar('Yellow_High_S', 'Camera', 250, 255, lambda x: None)
cv2.createTrackbar('Yellow_Low_V', 'Camera', 170, 255, lambda x: None)
cv2.createTrackbar('Yellow_High_V', 'Camera', 255, 255, lambda x: None)

while True:
    # 프레임 읽기
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to read a frame.")
        break

    # 트랙바 값 얻기
    # red 1
    red1_low_h = cv2.getTrackbarPos('Red1_Low_H', 'Camera')
    red1_high_h = cv2.getTrackbarPos('Red1_High_H', 'Camera')
    red1_low_s = cv2.getTrackbarPos('Red1_Low_S', 'Camera')
    red1_high_s = cv2.getTrackbarPos('Red1_High_S', 'Camera')
    red1_low_v = cv2.getTrackbarPos('Red1_Low_V', 'Camera')
    red1_high_v = cv2.getTrackbarPos('Red1_High_V', 'Camera')

    #red 2
    red2_low_h = cv2.getTrackbarPos('Red2_Low_H', 'Camera')
    red2_high_h = cv2.getTrackbarPos('Red2_High_H', 'Camera')
    red2_low_s = cv2.getTrackbarPos('Red2_Low_S', 'Camera')
    red2_high_s = cv2.getTrackbarPos('Red2_High_S', 'Camera')
    red2_low_v = cv2.getTrackbarPos('Red2_Low_V', 'Camera')
    red2_high_v = cv2.getTrackbarPos('Red2_High_V', 'Camera')

    #yellow
    yellow_low_h = cv2.getTrackbarPos('Yellow_Low_H', 'Camera')
    yellow_high_h = cv2.getTrackbarPos('Yellow_High_H', 'Camera')
    yellow_low_s = cv2.getTrackbarPos('Yellow_Low_S', 'Camera')
    yellow_high_s = cv2.getTrackbarPos('Yellow_High_S', 'Camera')
    yellow_low_v = cv2.getTrackbarPos('Yellow_Low_V', 'Camera')
    yellow_high_v = cv2.getTrackbarPos('Yellow_High_V', 'Camera')

    # 빨간색 공 인식
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    imgThresh_Low = cv2.inRange(imgHSV, np.array([red1_low_h, red1_low_s, red1_low_v]),
                               np.array([red1_high_h, red1_high_s, red1_high_v]))
    imgThresh_High = cv2.inRange(imgHSV, np.array([red2_low_h, red2_low_s, red2_low_v]),
                               np.array([red2_high_h, red2_high_s, red2_high_v]))

    imgThresh = cv2.add(imgThresh_Low, imgThresh_High)

    # 노란색 홀컵 인식
    yellow_low = np.array([yellow_low_h, yellow_low_s, yellow_low_v])
    yellow_high = np.array([yellow_high_h, yellow_high_s, yellow_high_v])
    yellow_mask = cv2.inRange(imgHSV, yellow_low, yellow_high)

    # 빨간색, 노란색 감지된 이미지
    red_detected = cv2.bitwise_and(frame, frame, mask=imgThresh)
    yellow_detected = cv2.bitwise_and(frame, frame, mask=yellow_mask)

    # 빨간색, 노란색을 동시에 표시
    both_detected = cv2.bitwise_or(red_detected, yellow_detected)

    # 마우스 포인터 현재 위치 표시
    cv2.putText(frame, f'coordinate: ({mouse_x},{mouse_y})', (mouse_x, mouse_y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

    # 마우스 포인터 위치의 색상값 (BGR) 출력
    if mouse_y < frame.shape[0] and mouse_x < frame.shape[1]:
        color_bgr = frame[mouse_y, mouse_x]

        # BGR을 HSV로 변환
        color_hsv = cv2.cvtColor(np.uint8([[color_bgr]]), cv2.COLOR_BGR2HSV)[0][0]
        cv2.putText(frame, f'HSV: {color_hsv}', (mouse_x, mouse_y + 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

    cv2.imshow('Camera', frame)
    cv2.imshow('red', red_detected)
    cv2.imshow('yellow', yellow_detected)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 종료할 때 카메라 해제 및 윈도우 닫기
cap.release()
cv2.destroyAllWindows()
