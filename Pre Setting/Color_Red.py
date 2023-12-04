import cv2
import numpy as np

# 초기화
mouse_x, mouse_y = 0, 0

# 마지막으로 저장한 트랙바 값 초기화
last_values_red1 = {
    'low_h': 0, 'high_h': 17, 'low_s': 80, 'high_s': 120, 'low_v': 210, 'high_v': 255,
}

last_values_red2 = {
    'low_h': 0, 'high_h': 17, 'low_s': 80, 'high_s': 120, 'low_v': 210, 'high_v': 255,
}

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
cv2.namedWindow('Trackbar', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Trackbar', 500, 400)

# 마우스 이벤트 콜백 함수 등록
cv2.setMouseCallback('Trackbar', mouse_callback)

# 트랙바 초기화
for name, value in last_values_red1.items():
    cv2.createTrackbar(f'trackbar1_{name}', 'Trackbar', value, 255, lambda x: None)

for name, value in last_values_red2.items():
    cv2.createTrackbar(f'trackbar2_{name}', 'Trackbar', value, 255, lambda x: None)

while True:
    # 프레임 읽기
    ret, frame = cap.read()

    if not ret:
        print("Failed to read a frame.")
        break

    # 트랙바 값 얻기
    for name in last_values_red1.keys():
        last_values_red1[name] = cv2.getTrackbarPos(f'trackbar1_{name}', 'Trackbar')

    for name in last_values_red2.keys():
        last_values_red2[name] = cv2.getTrackbarPos(f'trackbar2_{name}', 'Trackbar')

    # 빨간색 공 인식
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    imgThresh_Low1 = cv2.inRange(imgHSV, np.array([last_values_red1['low_h'], last_values_red1['low_s'], last_values_red1['low_v']]),
                                np.array([last_values_red1['high_h'], last_values_red1['high_s'], last_values_red1['high_v']]))

    imgThresh_High1 = cv2.inRange(imgHSV, np.array([last_values_red2['low_h'], last_values_red2['low_s'], last_values_red2['low_v']]),
                                 np.array([last_values_red2['high_h'], last_values_red2['high_s'], last_values_red2['high_v']]))

    imgThresh1 = cv2.add(imgThresh_Low1, imgThresh_High1)

    # 빨간색 감지된 이미지
    red_detected1 = cv2.bitwise_and(frame, frame, mask=imgThresh1)

    # 마우스 포인터 현재 위치 표시
    cv2.putText(frame, f'coordinate: ({mouse_x},{mouse_y})', (mouse_x, mouse_y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

    # 마우스 포인터 위치의 색상값 (BGR) 출력
    if mouse_y < frame.shape[0] and mouse_x < frame.shape[1]:
        color_bgr = frame[mouse_y, mouse_x]

        # BGR을 HSV로 변환
        color_hsv = cv2.cvtColor(np.uint8([[color_bgr]]), cv2.COLOR_BGR2HSV)[0][0]
        cv2.putText(frame, f'HSV: {color_hsv}', (mouse_x, mouse_y + 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

    cv2.imshow('Trackbar', frame)
    cv2.imshow('Red1', red_detected1)

    # 창의 위치 조정
    cv2.moveWindow('Real Window', 600, 0)
    cv2.moveWindow('Red1', 600, 500)

    # 'q' 키를 누르면 종료
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):  # Press 's' to save the last trackbar values to the code
        with open('Pre Setting/last_values_red1.py', 'w') as file:
            file.write(f"last_values_red1 = {last_values_red1}")
        with open('Pre Setting/last_values_red2.py', 'w') as file:
            file.write(f"last_values_red2 = {last_values_red2}")

# 종료할 때 카메라 해제 및 윈도우 닫기
cap.release()
cv2.destroyAllWindows()
