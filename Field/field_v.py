import cv2
import numpy as np

# 동영상 파일을 열고 초기화합니다.
video_path = '/home/user/Downloads/CV_EmbededSWC/src/f_v_long.avi'  # 동영상 파일 경로를 지정하세요.
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

    # 경기장 색깔 범위 HSV : 색조, 채도, 명도
    # 경기장 초록색만                
    # lower_green = np.array([30, 30, 40])
    # lower_green = np.array([30, 70, 40])
    # upper_green = np.array([85, 255, 255])

    #빨간색 노란색까지 다 
    #
    lower_green = np.array([0, 70, 30])
    upper_green = np.array([85, 255, 255])

    # 초록색 영역을 마스킹합니다.
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # 마스크와 프레임을 비트 AND 연산합니다.
    masked_frame = cv2.bitwise_and(frame, frame, mask=mask)

    # 그레이스케일로 변환합니다.
    gray = cv2.cvtColor(masked_frame, cv2.COLOR_BGR2GRAY)

    # 가우시안 블러를 적용합니다. (노이즈 감소)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Canny 엣지 검출을 수행합니다.
    edges = cv2.Canny(blurred, 50, 150)

    # 경계를 찾습니다.
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 경계를 그립니다.
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

    # 결과 프레임을 표시합니다.
    cv2.imshow('Edge Detection', frame)

    # 'q' 키를 누르면 루프를 종료합니다.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 동영상 파일 사용 종료
cap.release()
cv2.destroyAllWindows()
