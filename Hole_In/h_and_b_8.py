import cv2
import time

# 영상 파일 경로
video_paths = ['video/in.MOV', 'video/in_ball.MOV']

# 결과 이미지를 표시할 창 생성
cv2.namedWindow('Hole Cup', cv2.WINDOW_NORMAL)
cv2.namedWindow('Ball', cv2.WINDOW_NORMAL)

# 두 이미지 창을 위한 변수 생성
image_window1 = 'Hole Cup'
image_window2 = 'Ball'

# 영상 캡처 객체 생성
caps = [cv2.VideoCapture(path) for path in video_paths]

# 최소 프레임 수 가져오기
min_frame_count = min([int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) for cap in caps])

# 종료 여부 플래그 초기화
exit_flag = False

# 영상 재생 속도 조절을 위한 딜레이 값 계산
delay = int(1000 / (0.8 * caps[0].get(cv2.CAP_PROP_FPS)))

frame_idx = 0
last_print_time = time.time()

# 결과 창의 위치 설정
cv2.moveWindow('Hole Cup', 200, 200)
cv2.moveWindow('Ball', 700, 230)

# 이전 프레임의 좌표를 저장할 변수 초기화
prev_left_points = [None, None]
prev_right_points = [None, None]

while True:
    # 프레임 읽기
    frames = [cap.read()[1] for cap in caps]

    # 왼쪽과 오른쪽 좌표 초기화
    left_points = [None, None]
    right_points = [None, None]

    for idx, frame in enumerate(frames):
        # 이미지 전처리
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)

        # 외곽 경계 검출
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 가장 왼쪽과 오른쪽에 있는 점 검출
        left_point, right_point = None, None

        if contours:
            for contour in contours:
                for point in contour:
                    x = point[0][0]
                    y = point[0][1]

                    # 가장 왼쪽에 있는 점 업데이트
                    if left_point is None or x < left_point[0]:
                        left_point = [x, y]

                    # 가장 오른쪽에 있는 점 업데이트
                    if right_point is None or x > right_point[0]:
                        right_point = [x, y]

        # 결과 이미지에 표시
        result = frame.copy()
        if left_point is not None:
            cv2.circle(result, tuple(left_point), 5, (0, 255, 0), -1)
        if right_point is not None:
            cv2.circle(result, tuple(right_point), 5, (0, 0, 255), -1)

        # 첫 번째 영상의 좌표 저장
        if idx == 0:
            left_points[0] = left_point
            right_points[0] = right_point
        # 두 번째 영상의 좌표 저장
        elif idx == 1:
            # 현재 좌표가 None일 경우 이전 프레임의 값을 가져옴
            if left_point is None:
                left_point = prev_left_points[1] if prev_left_points[1] is not None else prev_left_points[0]
            if right_point is None:
                right_point = prev_right_points[1] if prev_right_points[1] is not None else prev_right_points[0]

            left_points[1] = left_point
            right_points[1] = right_point


        # 1초에 2번만 출력
        current_time = time.time()
        if current_time - last_print_time >= 0.5:
            last_print_time = current_time
            #print(left_points, right_points)
            if (left_points[0] is not None and left_points[1] is not None and
                right_points[0] is not None and right_points[1] is not None and
                left_points[0][0] < left_points[1][0] and right_points[0][0] > right_points[1][0]):
                print("Hole In !!")
            else:
                print("It was close...")

        # 이미지 창에 결과 표시
        if idx == 0:
            cv2.imshow(image_window1, result)
        else:
            cv2.imshow(image_window2, result)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(delay) & 0xFF == ord('q'):
            exit_flag = True
            break

    frame_idx += 1

    if exit_flag or frame_idx >= min_frame_count:
        break

    # 이전 프레임의 좌표 업데이트
    prev_left_points = left_points
    prev_right_points = right_points

# 영상 캡처 객체 해제
for cap in caps:
    cap.release()

# 모든 이미지 처리 완료 후에 창 닫기
cv2.destroyAllWindows()

