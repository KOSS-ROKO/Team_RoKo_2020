
'''import cv2
import numpy as np

# 초기화
mouse_x, mouse_y = 0, 0

# 마지막으로 저장한 트랙바 값 초기화
last_values = {
    'red1_low_h': 0, 'red1_high_h': 17, 'red1_low_s': 80, 'red1_high_s': 120, 'red1_low_v': 210, 'red1_high_v': 255,
    'red2_low_h': 0, 'red2_high_h': 17, 'red2_low_s': 80, 'red2_high_s': 120, 'red2_low_v': 210, 'red2_high_v': 255
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
cv2.resizeWindow('Trackbar', 500, 1000)

# 마우스 이벤트 콜백 함수 등록
cv2.setMouseCallback('Trackbar', mouse_callback)

# 트랙바 초기화
for name, value in last_values.items():
    cv2.createTrackbar(name, 'Trackbar', value, 255, lambda x: None)

while True:
    # 프레임 읽기
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to read a frame.")
        break

    # 트랙바 값 얻기
    for name in last_values.keys():
        last_values[name] = cv2.getTrackbarPos(name, 'Trackbar')

    # 빨간색 공 인식
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    imgThresh_Low = cv2.inRange(imgHSV, np.array([last_values['red1_low_h'], last_values['red1_low_s'], last_values['red1_low_v']]),
                               np.array([last_values['red1_high_h'], last_values['red1_high_s'], last_values['red1_high_v']]))
    imgThresh_High = cv2.inRange(imgHSV, np.array([last_values['red2_low_h'], last_values['red2_low_s'], last_values['red2_low_v']]),
                                np.array([last_values['red2_high_h'], last_values['red2_high_s'], last_values['red2_high_v']]))

    imgThresh = cv2.add(imgThresh_Low, imgThresh_High)


    # 빨간색, 노란색 감지된 이미지
    red_detected = cv2.bitwise_and(frame, frame, mask=imgThresh)


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
    cv2.imshow('Real Window', frame)
    cv2.imshow('Red', red_detected)
    
    # 창의 위치 조정
    cv2.moveWindow('Real Window', 600, 0)
    cv2.moveWindow('Red', 900, 0)


    # 'q' 키를 누르면 종료
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):  # Press 's' to save the last trackbar values to the code
        with open('Pre Setting/last_values_red.py', 'w') as file:
            file.write(f"last_values = {last_values}")

# 종료할 때 카메라 해제 및 윈도우 닫기
cap.release()
cv2.destroyAllWindows()
'''



import cv2
import numpy as np

# 초기화
mouse_x, mouse_y = 0, 0

# 마지막으로 저장한 트랙바 값 초기화
last_values = {
    'red1_low_h': 0, 'red1_high_h': 17, 'red1_low_s': 80, 'red1_high_s': 120, 'red1_low_v': 210, 'red1_high_v': 255,
    'red2_low_h': 0, 'red2_high_h': 17, 'red2_low_s': 80, 'red2_high_s': 120, 'red2_low_v': 210, 'red2_high_v': 255
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
num_trackbars = len(last_values)
num_columns = 2
trackbars_per_column = num_trackbars // num_columns

for idx, (name, value) in enumerate(last_values.items()):
    column = idx % num_columns
    row = idx // num_columns
    cv2.createTrackbar(name, 'Trackbar', value, 255, lambda x: None)
    cv2.moveWindow('Trackbar', column * 250, row * 200)
    cv2.setTrackbarPos(name, 'Trackbar', value)

while True:
    # 프레임 읽기
    ret, frame = cap.read()

    if not ret:
        print("Failed to read a frame.")
        break

    # 트랙바 값 얻기
    for name in last_values.keys():
        last_values[name] = cv2.getTrackbarPos(name, 'Trackbar')

    # 빨간색 공 인식
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    imgThresh_Low = cv2.inRange(imgHSV, np.array([last_values['red1_low_h'], last_values['red1_low_s'], last_values['red1_low_v']]),
                               np.array([last_values['red1_high_h'], last_values['red1_high_s'], last_values['red1_high_v']]))
    imgThresh_High = cv2.inRange(imgHSV, np.array([last_values['red2_low_h'], last_values['red2_low_s'], last_values['red2_low_v']]),
                                np.array([last_values['red2_high_h'], last_values['red2_high_s'], last_values['red2_high_v']]))

    imgThresh = cv2.add(imgThresh_Low, imgThresh_High)

    # 빨간색 감지된 이미지
    red_detected = cv2.bitwise_and(frame, frame, mask=imgThresh)

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
    cv2.imshow('Real Window', frame)
    cv2.imshow('Red', red_detected)

    # 창의 위치 조정
    cv2.moveWindow('Real Window', 600, 0)
    cv2.moveWindow('Red', 600, 500)

    # 'q' 키를 누르면 종료
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):  # Press 's' to save the last trackbar values to the code
        with open('Pre Setting/last_values_red.py', 'w') as file:
            file.write(f"last_values = {last_values}")

# 종료할 때 카메라 해제 및 윈도우 닫기
cap.release()
cv2.destroyAllWindows()
