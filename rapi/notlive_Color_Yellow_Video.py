import cv2
import numpy as np

# 초기화
mouse_x, mouse_y = 0, 0

# 마지막으로 저장한 트랙바 값 초기화
last_values = {'yellow_low_h': 10, 'yellow_high_h': 36, 'yellow_low_s': 99, 'yellow_high_s': 255, 'yellow_low_v': 147, 'yellow_high_v': 255}

# 마우스 이벤트 콜백 함수 정의
def mouse_callback(event, x, y, flags, param):
    global mouse_x, mouse_y
    mouse_x, mouse_y = x, y

video_path = 'VIDEO/real.avi'
cap = cv2.VideoCapture(video_path)

# 해상도, 프레임 설정
cap.set(3, 640)
cap.set(4, 480)
cap.set(5, 5)

# 윈도우 생성
cv2.namedWindow('Trackbar', cv2.WINDOW_NORMAL)

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


    # 노란색 홀컵 인식
    yellow_low = np.array([last_values['yellow_low_h'], last_values['yellow_low_s'], last_values['yellow_low_v']])
    yellow_high = np.array([last_values['yellow_high_h'], last_values['yellow_high_s'], last_values['yellow_high_v']])
    yellow_mask = cv2.inRange(imgHSV, yellow_low, yellow_high)


    yellow_detected = cv2.bitwise_and(frame, frame, mask=yellow_mask)

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
    cv2.imshow('Yellow', yellow_detected)
    
    # 창의 위치 조정
    # cv2.moveWindow('Real Window', 600, 0)
    # cv2.moveWindow('Yellow', 900, 300)


    # 'q' 키를 누르면 종료
    key = cv2.waitKey(100) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):  # Press 's' to save the last trackbar values to the code
        with open('rapi/last_values_yellow.py', 'w') as file:
            file.write(f"last_values = {last_values}")

# 종료할 때 카메라 해제 및 윈도우 닫기
cap.release()
cv2.destroyAllWindows()
