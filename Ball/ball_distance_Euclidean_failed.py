# detect_ball.py랑 유클리드 거리법으로 빨간공 거리 측정
# 9/13 오후 8시 18분 기록 - 유클리드 거리법은 안된다. 이건 테스트용 문서이다.

import cv2
import numpy as np

cap = cv2.VideoCapture('Ball/ball_video/ball4.avi')  

while True:
    # 프레임 읽기
    ret, frame = cap.read()
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # 빨간색 범위를 정의
    lower_red = np.array([170, 100, 45])
    upper_red = np.array([177, 255, 255])
    
    # HSV 이미지에서 빨간색 마스크 생성
    mask = cv2.inRange(hsv, lower_red, upper_red)
    
    # 원본 이미지에서 마스크로 빨간색 부분 추출
    red_detected = cv2.bitwise_and(frame, frame, mask=mask)

    # 빨간색 객체를 그레이 스케일로 변환
    gray_frame = cv2.cvtColor(red_detected, cv2.COLOR_BGR2GRAY)

    # 에지 검출 (Canny 사용)
    edges = cv2.Canny(gray_frame, 50, 150)

    # 객체 검출 (윤곽선 사용)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    detected_circles = []  # 감지된 원의 정보를 저장할 리스트 초기화

    # 검출된 원 정보 저장
    for contour in contours:
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) >= 6:  # 원은 최소 6개의 점을 갖습니다.
            center, _ = cv2.minEnclosingCircle(contour)
            center = tuple(map(int, center))
            radius = int(cv2.arcLength(contour, True) / (2 * np.pi))

            # 원의 중심 좌표 표시
            cv2.circle(frame, center, 2, (0, 0, 255), -1)

            # 중심 좌표까지의 거리 계산
            distance = np.sqrt((center[0] - frame.shape[1] // 2) ** 2 + (center[1] - frame.shape[0] // 2) ** 2)

            # 거리 출력
            text = f"Distance: {distance:.2f}"
            cv2.putText(frame, text, (center[0] - 20, center[1] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            print(text)
    
    # 결과 화면 표시
    cv2.imshow('Result', frame)
    
    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 작업 완료 후 리소스 해제
cap.release()
cv2.destroyAllWindows()
