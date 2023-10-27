# 최종 : 공이 중앙에 위치하면 stop
# go left & go right
# 빨간 공 잘 검출되는지 확인하기 위해, 빨간 공만 띄우는 창 추가함

import cv2
import numpy as np

# 빨간색 범위 (OpenCV에서는 BGR 형식을 사용하므로 순서가 바뀝니다)
lower_red = np.array([170, 100, 45])
upper_red = np.array([177, 255, 255])

# 영상에서 빨간색만 추출하는 함수
def extract_red_objects(frame):
    # BGR에서 HSV로 변환
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
    imgThreshLow = cv2.inRange(imgHSV, (0, 200, 155), (50, 255, 255))
    imgThreshHigh = cv2.inRange(imgHSV, (160, 155, 50), (179, 255, 255))
    
    imgThresh = cv2.add(imgThreshLow, imgThreshHigh)

    imgThresh = cv2.GaussianBlur(imgThresh, (3, 3), 2)
    imgThresh = cv2.erode(imgThresh, np.ones((5, 5), np.uint8))
    imgThresh = cv2.dilate(imgThresh, np.ones((5, 5), np.uint8))

    return imgThresh

# 화면을 11x11 그리드로 나누는 함수
def divide_screen(frame):
    height, width = frame.shape[:2]
    cell_height = height // 11
    cell_width = width // 11
    
    # 그리드 라인 그리기
    for i in range(1, 11):
        cv2.line(frame, (0, i * cell_height), (width, i * cell_height), (0, 255, 0), 1)  # 녹색
        cv2.line(frame, (i * cell_width, 0), (i * cell_width, height), (0, 255, 0), 1)
    
    return frame

# 저장된 영상을 읽어옵니다. 파일 경로를 적절히 수정하세요.
cap = cv2.VideoCapture('ball_video/ball4.avi')

# 전체 화면 결과 창 크기 설정
cv2.namedWindow('Full Frame', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Full Frame', 800, 600)  # 적절한 크기로 조정

# 빨간 공만 보이는 창 생성
cv2.namedWindow('Red Objects', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Red Objects', 400, 300)

while True:
    # 영상 프레임 읽기
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # 빨간색 객체 추출
    red_objects = extract_red_objects(frame)
    
    # 화면을 11x11 그리드로 나누고 그리드 라인 그리기
    divided_frame = divide_screen(frame)
    
    #여기에 새로운 코드 추가
    # 빨간색 객체 검출 및 위치 계산
    non_zero_pixels = np.transpose(np.nonzero(red_objects))

    if non_zero_pixels.size > 0:
        x_center = non_zero_pixels[:, 1].mean()
        y_center = non_zero_pixels[:, 0].mean()
        
        cell_height = divided_frame.shape[0] // 11

        # 빨간 공이 중앙 가로줄인 6번째 줄에서 검출되면 "stop" 출력
        if (cell_height * 5 <= y_center <= cell_height * 6):
            print("stop")
        # 1~5번째 줄에서 검출되면 "go up" 출력
        elif y_center < cell_height * 5:
            print("go up")
        # 7~11번째 줄에서 검출되면 "go down" 출력
        elif y_center > cell_height * 6:
            print("go down")
    else:
        print("go far")

    # 빨간 공만 보이는 창에 이미지 표시
    cv2.imshow('Red Objects', red_objects)
    
    # 전체 화면에 영상 출력
    cv2.imshow('Full Frame', frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

# 종료 후 리소스 해제
cap.release()
cv2.destroyAllWindows()
