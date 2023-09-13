import cv2
import numpy as np

cap = cv2.VideoCapture('arrow.avi') 

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # BGR 색상 공간에서 노란색 범위 지정
    lower_yellow = np.array([0, 50, 50])
    upper_yellow = np.array([45, 255, 255])

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

            if len(approx) == 7:  # 화살표로 판단할 근사화 결과의 꼭지점 개수 조건
                # 꼭짓점 표시
                # for point in approx:
                #     x, y = point[0]
                #     cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)

                # 화살표 7개 꼭지점의 중간값 찾기
                center = np.mean(approx, axis=0)
                center_x = int(round(center[0][0]))
                center_y = int(round(center[0][1]))
                cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

                # 각 점과 중심점 사이의 거리 계산
                distances = [np.linalg.norm(point - center) for point in approx]

                # 거리가 가장 먼 두 점의 인덱스 찾기
                far_indices = np.argsort(distances)[:2]

                # 가장 먼 두 꼭지점의 좌표
                closest_points = [approx[i][0] for i in far_indices]

                # 가장 가까운 두 꼭지점의 중간값 찾기
                far_center = np.mean(closest_points, axis=0)
                far_center_x = int(round(far_center[0]))
                far_center_y = int(round(far_center[1]))
                cv2.circle(frame, (far_center_x, far_center_y), 5, (255, 0, 0), -1)

                arrow_angle = np.arctan2(far_center_y - center_y, far_center_x - center_x)
                angle = np.degrees(arrow_angle)

                font = cv2.FONT_HERSHEY_SIMPLEX
                if -45 <= angle < 45:
                    cv2.putText(frame, 'RIGHT', (10, 85), font, 1, (255, 255, 0))
                elif 45 <= angle < 135:
                    cv2.putText(frame, 'DOWN', (10, 85), font, 1, (255, 255, 0))
                elif -180 <= angle <= -135:
                    cv2.putText(frame, 'LEFT', (10, 85), font, 1, (255, 255, 0))
                elif 135 <= angle <= 180:
                    cv2.putText(frame, 'LEFT', (10, 85), font, 1, (255, 255, 0))
                elif -135 < angle < -45:
                    cv2.putText(frame, 'UP', (10, 85), font, 1, (255, 255, 0))

                # 화살표 표시
                cv2.drawContours(frame, [approx], 0, (0, 255, 0), 2)

    cv2.imshow('Yellow Arrow Detection', frame)
    cv2.imshow('Yellow area', yellow_mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
