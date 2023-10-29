import cv2
import numpy as np

# 화면을 11x11 그리드로 나누는 함수
def divide_screen(frame):
    height, width = frame.shape[:2]
    cell_height = height // 11
    cell_width = width // 11

    return frame

# 저장된 영상을 읽어옵니다. 파일 경로를 적절히 수정하세요.
cap = cv2.VideoCapture('HoleCup/flag_video/flag2.avi')

# 노란색 객체의 최소 넓이 설정
min_yellow_area = 10  # 이 값을 조정하여 객체의 크기에 대한 필터링을 변경할 수 있습니다.

while True:
    # 영상 프레임 읽기
    ret, frame = cap.read()

    if not ret:
        break

    # 화면을 11x11 그리드로 나누고 그리드 라인 그리기
    divided_frame = divide_screen(frame)

    # 이미지에서 노란색 객체를 찾기 위한 HSV 범위
    yellow_lower = np.array([10, 80, 50])
    yellow_upper = np.array([36, 250, 250])

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    yellow_mask = cv2.inRange(hsv_frame, yellow_lower, yellow_upper)
    yellow_objects = cv2.bitwise_and(frame, frame, mask=yellow_mask)
    cv2.imshow("yellow", yellow_objects)

    # 이미지 이진화
    gray_frame = cv2.cvtColor(yellow_objects, cv2.COLOR_BGR2GRAY)
    _, binary_frame = cv2.threshold(gray_frame, 1, 255, cv2.THRESH_BINARY)

    # 객체 윤곽 찾기
    contours, _ = cv2.findContours(binary_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 가장 왼쪽과 오른쪽 점 찾기
    leftmost = tuple(frame.shape[1::-1])
    rightmost = (0, 0)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area >= min_yellow_area:
            for point in contour:
                x = point[0][0]
                y = point[0][1]

                # 가장 왼쪽 점 업데이트
                if x < leftmost[0]:
                    leftmost = (x, y)

                # 가장 오른쪽 점 업데이트
                if x > rightmost[0]:
                    rightmost = (x, y)

    if leftmost != tuple(frame.shape[1::-1]) and rightmost != (0, 0):
        # 왼쪽과 오른쪽 점의 x, y 좌표 평균 계산
        midpoint = ((leftmost[0] + rightmost[0]) // 2, (leftmost[1] + rightmost[1]) // 2)
        cell_height = divided_frame.shape[0] // 11

        # 빨간 공이 중앙 가로줄인 6번째 줄에서 검출되면 "stop" 출력
        if (cell_height * 5 <= midpoint[1] <= cell_height * 6):
            print("stop")
        # 1~5번째 줄에서 검출되면 "go up" 출력
        elif midpoint[1] < cell_height * 5:
            print("go up")
        # 7~11번째 줄에서 검출되면 "go down" 출력
        elif midpoint[1] > cell_height * 6:
            print("go down")
        else:
            print("go far")

        # 결과 이미지에 중간점 그리기
        cv2.circle(frame, midpoint, 5, (0, 0, 255), -1)

    # 전체 화면에 영상 출력
    cv2.imshow('Full Frame', frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

# 종료 후 리소스 해제
cap.release()
cv2.destroyAllWindows()
