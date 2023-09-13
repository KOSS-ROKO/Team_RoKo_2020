# 컨투어 + 유클리드 거리
# 9/13 8시 기록 - 이건 잘 안됨.
import cv2
import numpy as np

video_capture = cv2.VideoCapture('Flag/flag_video/flag1.avi')

while True:
    ret, frame = video_capture.read()

    if not ret:
        break

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_yellow = np.array([0, 50, 100])
    upper_yellow = np.array([36, 250, 255])

    yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
    yellow_objects = cv2.bitwise_and(frame, frame, mask=yellow_mask)

    # 노란색 객체를 그레이 스케일로 변환
    gray_frame = cv2.cvtColor(yellow_objects, cv2.COLOR_BGR2GRAY)

    # 에지 검출 (Canny 사용)
    edges = cv2.Canny(gray_frame, 50, 150)

    # 객체 검출 (윤곽선 사용)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 검출된 원 그리기
    for contour in contours:
        # 원 검출을 위한 미니멈 픽셀 거리 및 최소/최대 반지름 설정
        min_radius = 20
        max_radius = 80
        epsilon = 0.05 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) >= 6:  # 원은 최소 6개의 점을 갖습니다.
            center, _ = cv2.minEnclosingCircle(contour)
            center = tuple(map(int, center))
            radius = int(cv2.arcLength(contour, True) / (2 * np.pi))

            if min_radius <= radius <= max_radius:
                # 원 그리기
                cv2.circle(frame, center, radius, (0, 255, 0), 2)
                # 원의 중심 좌표 표시
                cv2.circle(frame, center, 2, (0, 0, 255), -1)
                # 중심 좌표까지의 거리 측정
                distance = np.sqrt((center[0] - frame.shape[1] // 2) ** 2 + (center[1] - frame.shape[0] // 2) ** 2)
                # 거리 출력
                text = f"Distance: {distance:.2f}"
                cv2.putText(frame, text, (center[0] - 20, center[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                print(text)

    cv2.imshow('Result', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()