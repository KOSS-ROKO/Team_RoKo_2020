import cv2
left_and_right = []
hl=0
hr=0 
bl=0
br=0

def find_left_right_points(contours):
    leftmost_point = None
    rightmost_point = None

    for contour in contours:
        for point in contour:
            x = point[0][0]
            y = point[0][1]

            # 가장 왼쪽에 있는 점 업데이트
            if leftmost_point is None or x < leftmost_point[0]:
                leftmost_point = [x, y]

            # 가장 오른쪽에 있는 점 업데이트
            if rightmost_point is None or x > rightmost_point[0]:
                rightmost_point = [x, y]

    print(leftmost_point, rightmost_point)
    return leftmost_point, rightmost_point

# 영상 파일 경로
video_paths = ['video/out.MOV', 'video/out_ball.MOV']

# 결과 이미지를 표시할 창 생성
cv2.namedWindow('Hole Cup', cv2.WINDOW_NORMAL)
cv2.namedWindow('Ball', cv2.WINDOW_NORMAL)

# 두 이미지 창을 위한 변수 생성
image_window1 = 'Hole Cup'
image_window2 = 'Ball'

# 영상 캡처 객체 생성
caps = [cv2.VideoCapture(path) for path in video_paths]

# 프레임 수와 초당 프레임 수 가져오기
frame_counts = [int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) for cap in caps]
fps_list = [cap.get(cv2.CAP_PROP_FPS) for cap in caps]

# 최소 프레임 수 가져오기
min_frame_count = min(frame_counts)

# 딜레이 계산
delays = [int(1000 / (fps * 0.7)) for fps in fps_list]

# 종료 여부 플래그 초기화
exit_flag = False

for frame_idx in range(min_frame_count):
    # 프레임 읽기
    frames = [cap.read()[1] for cap in caps]

    for idx, frame in enumerate(frames):
        # 이미지 전처리
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)

        # 외곽 경계 검출
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 가장 왼쪽과 오른쪽에 있는 점 검출
        left_point, right_point = find_left_right_points(contours)

        # 결과 이미지에 표시
        result = frame.copy()
        cv2.circle(result, left_point, 5, (0, 255, 0), -1)
        cv2.circle(result, right_point, 5, (0, 0, 255), -1)

        # 홀컵의 왼오, 공의 왼오 점 좌표 저장
        left_and_right.append(left_point)
        left_and_right.append(right_point)

        print(left_and_right)

        # 이미지 창에 결과 표시
        if idx == 0:
            cv2.imshow(image_window1, result)
        else:
            cv2.imshow(image_window2, result)

        # 왼오점의 x좌표들 비교 시작! > 홀컵, 공 순서
        if hl< bl and br < hr: 
        #(left_and_right[0][0] < left_and_right[2][0]) and (left_and_right[3][0] < left_and_right[1][0]):
            print("Congratulation Hole In !!")
        elif (left_and_right[0][0]< left_and_right[1][0]):
            print("---")
        else:
            print("It was close... Retry!")

        # 'q' 키를 누르면 종료
        if cv2.waitKey(delays[idx]) & 0xFF == ord('q'):
            exit_flag = True
            break

    if exit_flag:
        break

# 영상 캡처 객체 해제
for cap in caps:
    cap.release()

# 모든 이미지 처리 완료 후에 창 닫기
cv2.destroyAllWindows()

