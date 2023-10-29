import cv2
import numpy as np

# 동영상 파일을 열고 초기화합니다.
video_path = 'Field/f_v_long.avi'  # 동영상 파일 경로를 지정하세요.
cap = cv2.VideoCapture(video_path)

# 출력 동영상의 크기를 조정합니다.
output_width = 640  # 원하는 출력 폭(가로 크기)
output_height = 360  # 원하는 출력 높이(세로 크기)

while cap.isOpened():
    # 동영상에서 프레임을 읽어옵니다.
    ret, frame = cap.read()

    if not ret:
        break  # 더 이상 프레임을 읽을 수 없으면 루프를 종료합니다.

    # 프레임 크기를 조정합니다.
    frame = cv2.resize(frame, (output_width, output_height))

    # HSV 색상 공간으로 변환합니다.
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 색상 범위를 정의합니다.
    lower_red1 = np.array([0, 70, 40])  # 빨간색 최소값 (Hue: 0)
    upper_red1 = np.array([50, 255, 255])  # 빨간색 최대값 (Hue: 50)
    lower_red2 = np.array([150, 60, 40])  # 빨간색 최소값 (Hue: 160)
    upper_red2 = np.array([179, 255, 255])  # 빨간색 최대값 (Hue: 179)
    lower_yellow = np.array([20, 70, 40])  # 노란색 최소값 (Hue: 20)
    upper_yellow = np.array([30, 255, 255])  # 노란색 최대값 (Hue: 30)
    lower_green = np.array([30, 70, 40])  # 초록색 최소값 (Hue: 30)
    upper_green = np.array([85, 255, 255])  # 초록색 최대값 (Hue: 85)
    lower_pink = np.array([300, 50, 50])  # 핑크색 최소값 (예: 색조: 300, 채도: 50, 명도: 50)
    upper_pink = np.array([330, 255, 255])  # 핑크색 최대값 (예: 색조: 330, 채도: 255, 명도: 255)

    # 각 색상에 대한 마스크를 만듭니다.
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_pink = cv2.inRange(hsv, lower_pink, upper_pink)

    # 모든 색상의 마스크를 합칩니다.
    combined_mask = cv2.add(mask_red1, mask_red2)
    combined_mask = cv2.add(combined_mask, mask_yellow)
    combined_mask = cv2.add(combined_mask, mask_green)
    combined_mask = cv2.add(combined_mask, mask_pink)

    # 경계를 찾습니다.
    contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 내부 영역을 검정색으로 처리합니다.
    mask = np.zeros_like(combined_mask)
    cv2.drawContours(mask, contours, -1, (255,60,200), cv2.FILLED)
    mask = cv2.bitwise_not(mask)

    # 마스크를 이용하여 프레임을 업데이트합니다.
    frame = cv2.bitwise_and(frame, frame, mask=mask)


    # 화면을 왼쪽과 오른쪽으로 나눕니다.
    left_half = frame[:, :output_width // 2]
    right_half = frame[:, output_width // 2:]

    # 왼쪽 영역과 오른쪽 영역의 블랙 넓이를 계산합니다.
    left_black_area = cv2.countNonZero(cv2.inRange(left_half, (0, 0, 0), (0, 0, 0)))
    right_black_area = cv2.countNonZero(cv2.inRange(right_half, (0, 0, 0), (0, 0, 0)))

    # 블랙 넓이에 따라 'go right' 또는 'go left'를 출력합니다.
    if left_black_area +1000 >= right_black_area:
        result = 'go left'
    else:
        result = 'go right'

    # 결과 프레임을 표시합니다.
    cv2.putText(frame, result, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Combined Color Detection', frame)

    print(left_black_area, right_black_area, result)


    # 'q' 키를 누르면 루프를 종료합니다.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 동영상 파일 사용 종료
cap.release()
cv2.destroyAllWindows()
