import cv2
import numpy as np

cap = cv2.VideoCapture('Flag/flag_video/robot_flag.avi') 

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # BGR 색상 공간에서 노란색 범위 지정
    lower_yellow = np.array([0, 100, 100])
    upper_yellow = np.array([30, 255, 255])

    # 이미지를 HSV 색상 공간으로 변환
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 노란색 범위에 해당하는 영역 마스크 생성
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # 노란색 화살표 부분 표시
    yellow_arrow = cv2.bitwise_and(frame, frame, mask=yellow_mask)

    # 노란색 화살표의 윤곽선 검출
    contours, hierarchy = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 화살표의 꼭짓점 표시
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:  # 화살표로 판단할 최소한의 면적 조건
            # 윤곽선 근사화(복잡한 윤곽선을 간단한 다각형으로 대체)
            epsilon = 0.02 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)  # 다각형 꼭지점 반환

            if len(approx) == 3:  # 화살표로 판단할 근사화 결과의 꼭지점 개수 조건
                # 꼭짓점 표시
                for point in approx:
                    x, y = point[0]
                    cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
                    
    # 화살표 표시
                cv2.drawContours(frame, [approx], 0, (0, 255, 0), 2)



    cv2.imshow('Yellow Arrow Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
