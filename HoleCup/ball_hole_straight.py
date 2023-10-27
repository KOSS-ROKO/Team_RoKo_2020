import cv2
import numpy as np

# 빨간색 범위 (OpenCV에서는 BGR 형식을 사용하므로 순서가 바뀝니다)
lower_red = np.array([170, 100, 45])
upper_red = np.array([177, 255, 255])

# 노란색 범위
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])

# 영상에서 빨간색만 추출하는 함수
def extract_red_objects(frame):
    # BGR에서 HSV로 변환
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # 빨간색 범위로 이진화
    mask = cv2.inRange(hsv, lower_red, upper_red)
    
    # 이진화된 이미지에서 빨간색 객체만 추출
    red_objects = cv2.bitwise_and(frame, frame, mask=mask)
    
    return red_objects

# 영상에서 노란색만 추출하는 함수
def extract_yellow_objects(frame):
    # BGR에서 HSV로 변환
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # 노란색 범위로 이진화
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
    # 이진화된 이미지에서 노란색 객체만 추출
    yellow_objects = cv2.bitwise_and(frame, frame, mask=mask)
    
    return yellow_objects

# 화면을 11x11 그리드로 나누는 함수
def divide_screen(frame):
    height, width = frame.shape[:2]
    cell_height = height // 11
    cell_width = width // 11
    
    # 그리드 라인 그리기
    for i in range(1, 11):
        cv2.line(frame, (0, i * cell_height), (width, i * cell_height), (0, 255, 0), 2)  # 녹색
        cv2.line(frame, (i * cell_width, 0), (i * cell_width, height), (0, 255, 0), 2)
    
    return frame

# 객체의 중심을 찾는 함수
def find_object_center(object_image):
    # 객체 이미지를 그레이 스케일로 변환
    gray = cv2.cvtColor(object_image, cv2.COLOR_BGR2GRAY)
    
    # 객체 이미지에서 경계 상자를 찾습니다.
    contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) > 0:
        # 객체의 경계 상자 중심을 계산합니다.
        moments = cv2.moments(contours[0])
        if moments['m00'] != 0:
            center_x = int(moments['m10'] / moments['m00'])
            center_y = int(moments['m01'] / moments['m00'])
            return (center_x, center_y)
    
    # 객체가 없는 경우 None을 반환합니다.
    return None


# 저장된 영상을 읽어옵니다. 파일 경로를 적절히 수정하세요.
cap = cv2.VideoCapture('HoleCup/ball_holecup_straight.avi')

# 전체 화면 결과 창 크기 설정
cv2.namedWindow('Full Frame', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Full Frame', 800, 600)  # 적절한 크기로 조정

# 빨간 공만 보이는 창 생성
cv2.namedWindow('Red Objects', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Red Objects', 400, 300)

# 노란 공만 보이는 창 생성
cv2.namedWindow('Yellow Objects', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Yellow Objects', 400, 300)

while True:
    # 영상 프레임 읽기
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # 빨간색 객체 추출
    red_objects = extract_red_objects(frame)
    
    # 노란색 객체 추출
    yellow_objects = extract_yellow_objects(frame)
    
    # 화면을 11x11 그리드로 나누고 그리드 라인 그리기
    divided_frame = divide_screen(frame)
    
  # 빨간색 및 노란색 객체 검출 및 위치 계산
    red_center = find_object_center(red_objects)
    yellow_center = find_object_center(yellow_objects)

    cell_width = divided_frame.shape[1] // 11

    # 빨간 공과 노란 공이 모두 검출되었는지 확인
    if red_center is not None and yellow_center is not None:
        # 빨간 공과 노란 공이 모두 가운데 세로줄인 6번째 줄에서 검출되면 "stop" 출력
        if (cell_width * 5 <= red_center[0] <= cell_width * 6) and (cell_width * 5 <= yellow_center[0] <= cell_width * 6):
            print("stop")
        # 빨간 공이 가운데 세로줄인 6번째 줄에 있고 노란 공이 왼쪽에 검출되면 "go right" 출력
        elif (cell_width * 5 <= red_center[0] <= cell_width * 6) and (yellow_center[0] < cell_width * 5):
            print("go right")
        # 빨간 공이 가운데 세로줄인 6번째 줄에 있고 노란 공이 오른쪽에 검출되면 "go left" 출력
        elif (cell_width * 5 <= red_center[0] <= cell_width * 6) and (yellow_center[0] > cell_width * 6):
            print("go left")
        # 그 외의 경우 "go far" 출력
        else:
            print("go far")
    else:
        # 객체가 하나라도 검출되지 않은 경우 "no object" 출력
        print("no object")

    cell_width = divided_frame.shape[1] // 11

    # 빨간 공과 노란 공이 모두 가운데 세로줄인 6번째 줄에서 검출되면 "stop" 출력
    if (cell_width * 5 <= red_center[0] <= cell_width * 6) and (cell_width * 5 <= yellow_center[0] <= cell_width * 6):
        print("stop")
    # 빨간 공이 가운데 세로줄인 6번째 줄에 있고 노란 공이 왼쪽에 검출되면 "go right" 출력
    elif (cell_width * 5 <= red_center[0] <= cell_width * 6) and (yellow_center[0] < cell_width * 5):
        print("go right")
    # 빨간 공이 가운데 세로줄인 6번째 줄에 있고 노란 공이 오른쪽에 검출되면 "go left" 출력
    elif (cell_width * 5 <= red_center[0] <= cell_width * 6) and (yellow_center[0] > cell_width * 6):
        print("go left")

    # 그 외의 경우 "go far" 출력
    else:
        print("go far")

    # 빨간 공만 보이는 창에 이미지 표시
    cv2.imshow('Red Objects', red_objects)
    
    # 노란 공만 보이는 창에 이미지 표시
    cv2.imshow('Yellow Objects', yellow_objects)
    
    # 전체 화면에 영상 출력
    cv2.imshow('Full Frame', frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

# 종료 후 리소스 해제
cap.release()
cv2.destroyAllWindows()
