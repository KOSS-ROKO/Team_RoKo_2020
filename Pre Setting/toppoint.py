import cv2
import numpy as np

def find_max_yellow_pixel_coordinates(frame):
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    upper_yellow = np.array([30, 180, 255])
    lower_yellow = np.array([15, 100, 140])
    mask = cv2.inRange(imgHSV, lower_yellow, upper_yellow)
    yellow_part = cv2.bitwise_and(frame, frame, mask=mask)
    yellow_gray = cv2.cvtColor(yellow_part, cv2.COLOR_BGR2GRAY)
    y_max, x_max = np.unravel_index(yellow_gray.argmax(), yellow_gray.shape)

    return x_max, y_max

# 비디오 파일 경로 지정

# 비디오 캡처 객체 생성
cap = cv2.VideoCapture(0)

while cap.isOpened():
    # 비디오에서 한 프레임 읽기
    ret, frame = cap.read()

    if not ret:
        break

    # 함수 호출
    result = find_max_yellow_pixel_coordinates(frame)

    # 결과 출력
    print("가장 높은 y좌표의 픽셀 좌표:", result)

    # 결과를 빨간색 점으로 이미지에 표시
    cv2.circle(frame, (result[0], result[1]), 5, (0, 0, 255), -1)

    # 표시된 결과 확인을 위해 화면에 프레임 표시 (선택적)
    cv2.imshow('Video', frame)

    # 'q' 키를 누르면 루프 탈출
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 비디오 캡처 객체 해제
cap.release()

# 모든 창 닫기
cv2.destroyAllWindows()
