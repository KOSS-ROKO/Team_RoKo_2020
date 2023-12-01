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

while True:
    # 프레임 읽기
    ret, frame = cap.read()
    
    # 마우스 포인터 현재 위치 표시
    cv2.putText(frame, f'coordinate: ({mouse_x},{mouse_y})', (mouse_x, mouse_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

    # 마우스 포인터 위치의 색상값 (BGR) 출력
    if mouse_y < frame.shape[0] and mouse_x < frame.shape[1]:
        color_bgr = frame[mouse_y, mouse_x]

        # BGR을 HSV로 변환
        color_hsv = cv2.cvtColor(np.uint8([[color_bgr]]), cv2.COLOR_BGR2HSV)[0][0]
        cv2.putText(frame, f'HSV: {color_hsv}', (mouse_x, mouse_y + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

    
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    
    # ------------ 빨간색 공 인식 ---------------------------------------
    imgThreshLow = cv2.inRange(imgHSV, (0, 100, 100), (10, 255, 255))
    imgThreshHigh = cv2.inRange(imgHSV, (160, 100, 100), (179, 255, 255))
        
    # ------------ 노란색 홀컵 인식 -------------------------------------
    lower_yellow = np.array([10, 54, 130])
    upper_yellow = np.array([40, 250, 255])
    # ------------------------------------------------------------------

    
    imgThresh = cv2.add(imgThreshLow, imgThreshHigh)

    imgThresh = cv2.GaussianBlur(imgThresh, (3, 3), 2)
    imgThresh = cv2.erode(imgThresh, np.ones((5, 5), np.uint8))
    imgThresh = cv2.dilate(imgThresh, np.ones((5, 5), np.uint8))

    
    yellow_mask = cv2.inRange(imgHSV, lower_yellow, upper_yellow)

    # 빨간색, 노란색 감지된 이미지
    red_detected = cv2.bitwise_and(frame, frame, mask=imgThresh)
    yellow_detected = cv2.bitwise_and(frame, frame, mask=yellow_mask)

    # 빨간색, 노란색을 동시에 표시
    both_detected = cv2.bitwise_or(red_detected, yellow_detected)

    cv2.imshow('Camera', frame)
    cv2.imshow('red', red_detected)
    cv2.imshow('yellow', yellow_detected)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 종료할 때 카메라 해제 및 윈도우 닫기
cap.release()
cv2.destroyAllWindows()
