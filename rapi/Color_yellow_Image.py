import cv2
import numpy as np

# 초기화
paused = False  # Flag to indicate if the video is paused

# 마지막으로 저장한 트랙바 값 초기화
last_values = {'yellow_low_h': 10, 'yellow_high_h': 36, 'yellow_low_s': 99, 'yellow_high_s': 255,
               'yellow_low_v': 147, 'yellow_high_v': 255}

# 비디오 파일 경로
video_path = 'VIDEO/par3-5.avi'
cap = cv2.VideoCapture(video_path)

# 해상도, 프레임 설정
cap.set(3, 640)
cap.set(4, 480)
cap.set(5, 5)

# 윈도우 생성
cv2.namedWindow('Trackbar', cv2.WINDOW_NORMAL)

# 트랙바 초기화
for name, value in last_values.items():
    cv2.createTrackbar(name, 'Trackbar', value, 255, lambda x: None)

def get_hsv_from_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Extract the region around the clicked point
        clicked_region = frame[y-5:y+5, x-5:x+5, :]

        # Calculate the average HSV values of the clicked region
        average_hsv = np.mean(cv2.cvtColor(clicked_region, cv2.COLOR_BGR2HSV), axis=(0, 1))

        # Display the HSV values on the image window
        cv2.putText(frame, f'Clicked HSV: {average_hsv}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        print(f"Clicked HSV: {average_hsv}")

# 마우스 이벤트 콜백 함수 등록
cv2.setMouseCallback('Trackbar', get_hsv_from_click)

while True:
    # 프레임 읽기
    if not paused:
        ret, frame = cap.read()

        if not ret:
            print("Failed to read a frame.")
            break

    # 트랙바 값 얻기
    for name in last_values.keys():
        last_values[name] = cv2.getTrackbarPos(name, 'Trackbar')

    # 노란색 홀컵 인식
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    yellow_low = np.array([last_values['yellow_low_h'], last_values['yellow_low_s'], last_values['yellow_low_v']])
    yellow_high = np.array([last_values['yellow_high_h'], last_values['yellow_high_s'], last_values['yellow_high_v']])
    yellow_mask = cv2.inRange(imgHSV, yellow_low, yellow_high)
    yellow_detected = cv2.bitwise_and(frame, frame, mask=yellow_mask)

    cv2.imshow('Trackbar', frame)
    cv2.imshow('Real Window', frame)
    cv2.imshow('Yellow', yellow_detected)

    # 'q' 키를 누르면 종료
    key = cv2.waitKey(100) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):  # Press 's' to save the last trackbar values to the code
        with open('rapi/last_values_yellow.py', 'w') as file:
            file.write(f"last_values = {last_values}")
    elif key == ord(' '):  # Press space bar to toggle pause
        paused = not paused

# 종료할 때 카메라 해제 및 윈도우 닫기
cap.release()
cv2.destroyAllWindows()
