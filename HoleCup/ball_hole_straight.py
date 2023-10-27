import cv2
import numpy as np

def red_object_position(video_path):
    cap = cv2.VideoCapture(video_path)
    result = None

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break  # 비디오가 종료되면 루프를 빠져나옴

        # BGR에서 HSV로 색상 공간 변환
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 빨간색 범위 정의 (OpenCV에서는 HSV로 색상을 표현)
        lower_red = np.array([160, 70, 20])
        upper_red = np.array([178, 255, 255])

        # 노란색 범위 정의
        lower_yellow = np.array([0, 50, 50])
        upper_yellow = np.array([45, 255, 255])

        # 빨간색과 노란색 마스크 생성
        red_mask = cv2.inRange(hsv_frame, lower_red, upper_red)
        yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)

        # 빨간색과 노란색 물체 검출
        red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        yellow_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cv2.imshow("red_contours", red_mask)
        cv2.imshow("yellow_contours", yellow_mask)

        # 빨간색과 노란색 물체의 중심 좌표 계산
        red_center = None
        yellow_center = None

        if red_contours:
            red_max_contour = max(red_contours, key=cv2.contourArea)
            M = cv2.moments(red_max_contour)
            if M["m00"] != 0:
                red_center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if yellow_contours:
            yellow_max_contour = max(yellow_contours, key=cv2.contourArea)
            M = cv2.moments(yellow_max_contour)
            if M["m00"] != 0:
                yellow_center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                
        # 빨간색 물체가 왼쪽에 있는지 오른쪽에 있는지 판별
        if red_center and yellow_center:
            if abs(red_center[0] - yellow_center[0]) < 10:
                result = "middle"

            elif red_center[0] < yellow_center[0]:
                
                result = "left"
            else:
                result = "right"
        else:
            result = "none"

        # 결과 표시
        cv2.putText(frame, result, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # 화면에 결과 표시
        cv2.imshow('Video', frame)
        cv2.waitKey(1)  # 키 입력 대기 (1ms)

    # OpenCV 창 닫기
    cv2.destroyAllWindows()
    cap.release()

# 함수 사용 예제
video_path = 'video/ball_holecup_straight.avi'  # 실제 영상 파일 경로로 대체
red_object_position(video_path)