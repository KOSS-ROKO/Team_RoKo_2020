import cv2
import numpy as np

# 빨간색 범위 (OpenCV에서는 BGR 형식을 사용하므로 순서가 바뀝니다)
lower_red = np.array([0, 100, 100])
upper_red = np.array([20, 255, 255])

# 영상에서 빨간색만 추출하는 함수
def extract_red_objects(frame):
    # BGR에서 HSV로 변환
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # 빨간색 범위로 이진화
    mask = cv2.inRange(hsv, lower_red, upper_red)
    
    # 이진화된 이미지에서 빨간색 객체만 추출
    red_objects = cv2.bitwise_and(frame, frame, mask=mask)
    
    return red_objects

# 화면을 3x3 그리드로 나누는 함수
def divide_screen(frame):
    height, width = frame.shape[:2]
    cell_height = height // 3
    cell_width = width // 3
    
    # 그리드 라인 그리기
    for i in range(1, 3):
        cv2.line(frame, (0, i * cell_height), (width, i * cell_height), (255, 255, 255), 2)
        cv2.line(frame, (i * cell_width, 0), (i * cell_width, height), (255, 255, 255), 2)
    
    return frame

# 영상을 읽어옵니다.
cap = cv2.VideoCapture(0)

while True:
    # 영상 프레임 읽기
    ret, frame = cap.read()
    
    # 빨간색 객체 추출
    red_objects = extract_red_objects(frame)
    
    # 그리드로 화면 나누기
    divided_frame = divide_screen(frame)
    
    # 중앙 아래 칸 검사
    cell_height = divided_frame.shape[0] // 3
    cell_width = divided_frame.shape[1] // 3
    center_bottom_cell = divided_frame[cell_height * 2:cell_height * 3, cell_width:cell_width * 2]
    red_objects_in_cell = extract_red_objects(center_bottom_cell)
    
    # 빨간색 객체가 있는지 확인
    if np.count_nonzero(red_objects_in_cell) > 0:
        print("stop")
    else:
        print("go")
    
    # 화면에 영상 출력
    cv2.imshow('Frame', frame)
    
    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 종료 후 리소스 해제
cap.release()
cv2.destroyAllWindows()
