import cv2
import numpy as np

# 초기화
paused = False  # Flag to indicate if the video is paused

# 마지막으로 저장한 트랙바 값 초기화
last_values_red1 = {'low_h': 0, 'high_h': 10, 'low_s': 40, 'high_s': 155, 'low_v': 120, 'high_v': 255}
last_values_red2 = {'low_h': 160, 'high_h': 180, 'low_s': 50, 'high_s': 255, 'low_v': 100, 'high_v': 255}

# 비디오 파일 경로
video_path = 'VIDEO/par4 ball.avi'
cap = cv2.VideoCapture(video_path)

# 해상도, 프레임 설정
cap.set(3, 640)
cap.set(4, 480)
cap.set(5, 5)

# 윈도우 생성
cv2.namedWindow('Trackbar1', cv2.WINDOW_NORMAL)
cv2.namedWindow('Trackbar2', cv2.WINDOW_NORMAL)

# 이미지 창에 표시될 색상값을 저장할 변수 초기화
clicked_hsv = None

for name, value in last_values_red1.items():
    cv2.createTrackbar(f'trackbar1_{name}', 'Trackbar1', value, 255, lambda x: None)

for name, value in last_values_red2.items():
    cv2.createTrackbar(f'trackbar2_{name}', 'Trackbar2', value, 255, lambda x: None)

def get_hsv_from_click(event, x, y, flags, param):
    global clicked_hsv
    if event == cv2.EVENT_LBUTTONDOWN:
        # Extract the region around the clicked point
        clicked_region = frame[y-5:y+5, x-5:x+5, :]

        # Calculate the average HSV values of the clicked region
        average_hsv = np.mean(cv2.cvtColor(clicked_region, cv2.COLOR_BGR2HSV), axis=(0, 1))
        print(f"Clicked HSV: {average_hsv}")
        # Store the HSV values to be displayed
        clicked_hsv = average_hsv

# 마우스 이벤트 콜백 함수 등록
cv2.setMouseCallback('Trackbar1', get_hsv_from_click)
cv2.setMouseCallback('Trackbar2', get_hsv_from_click)

while True:
    # 프레임 읽기
    if not paused:
        ret, frame = cap.read()

        if not ret:
            print("Failed to read a frame.")
            break

    # 트랙바 값 얻기
    for name in last_values_red1.keys():
        last_values_red1[name] = cv2.getTrackbarPos(f'trackbar1_{name}', 'Trackbar1')

    for name in last_values_red2.keys():
        last_values_red2[name] = cv2.getTrackbarPos(f'trackbar2_{name}', 'Trackbar2')

    # 빨간색 공 인식
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    imgThresh_Low1 = cv2.inRange(imgHSV, np.array([last_values_red1['low_h'], last_values_red1['low_s'], last_values_red1['low_v']]),
                                np.array([last_values_red1['high_h'], last_values_red1['high_s'], last_values_red1['high_v']]))

    imgThresh_High1 = cv2.inRange(imgHSV, np.array([last_values_red2['low_h'], last_values_red2['low_s'], last_values_red2['low_v']]),
                                 np.array([last_values_red2['high_h'], last_values_red2['high_s'], last_values_red2['high_v']]))

    imgThresh1 = cv2.add(imgThresh_Low1, imgThresh_High1)

    # 빨간색 감지된 이미지
    red_detected1 = cv2.bitwise_and(frame, frame, mask=imgThresh1)

    cv2.imshow('Trackbar1', frame)
    cv2.imshow('Trackbar2', frame)
    cv2.imshow('Real Window', frame)
    cv2.imshow('Red1', red_detected1)

    # 마우스 클릭으로 얻은 색상값 출력
    if clicked_hsv is not None:
        cv2.putText(frame, f'Clicked HSV: {clicked_hsv}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        
        # 클릭된 색상값을 초기화
        clicked_hsv = None

    # 'q' 키를 누르면 종료
    key = cv2.waitKey(100) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):  # Press 's' to save the last trackbar values to the code
        with open('rapi/last_values_red1.py', 'w') as file:
            file.write(f"last_values_red1 = {last_values_red1}")
        with open('rapi/last_values_red2.py', 'w') as file:
            file.write(f"last_values_red2 = {last_values_red2}")
    elif key == ord(' '):  # Press space bar to toggle pause
        paused = not paused

# 종료할 때 카메라 해제 및 윈도우 닫기
cap.release()
cv2.destroyAllWindows()
