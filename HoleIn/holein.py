# 값이 아주 살짝 튀는데 이건 무시해도 될 거 같지만, 신경 쓰이면 확실하게 해두든 말든 니 알아서 하삼

import cv2
import numpy as np

def detect_hole_in_golf_ball(frame):
    
    # 노란색 홀컵 검출
    yellow_lower = np.array([20, 20, 100])
    yellow_upper = np.array([36, 250, 250])
    
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    yellow_mask = cv2.inRange(hsv_frame, yellow_lower, yellow_upper)
    
    yellow_objects = cv2.bitwise_and(frame, frame, mask=yellow_mask)
    
    cv2.imshow('holeCup', yellow_mask)
    
    blurred_frame = cv2.GaussianBlur(yellow_objects, (5, 5), 0)
    gray_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2GRAY)
    
    _, binary_frame = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    # 침식과 팽창을 사용하여 이미지를 보정
    kernel = np.ones((5, 5), np.uint8)
    binary_frame = cv2.erode(binary_frame, kernel, iterations=1)
    binary_frame = cv2.dilate(binary_frame, kernel, iterations=1)
    
    # 이진화된 이미지 표시
    cv2.imshow('Binary Image', binary_frame)
    
    # 노란색 홀컵 윤곽선 binary_frame
    contours, _ = cv2.findContours(binary_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    left_point, right_point = None, None
    
    # 가장 왼쪽과 오른쪽 점 찾기
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
        cv2.circle(result, tuple(left_point), 5, (0, 0, 255), -1)
    if right_point is not None:
        cv2.circle(result, tuple(right_point), 5, (0, 0, 255), -1)
        
        
        
    #################################################여기서부터 빨간공
    
    
    
    # 빨간공 인식
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    imgThreshLow = cv2.inRange(imgHSV, (0, 200, 155), (30, 255, 255))
    imgThreshHigh = cv2.inRange(imgHSV, (160, 155, 155), (179, 255, 255))
    
    imgThresh = cv2.add(imgThreshLow, imgThreshHigh)

    imgThresh = cv2.GaussianBlur(imgThresh, (3, 3), 2)
    imgThresh = cv2.erode(imgThresh, np.ones((5, 5), np.uint8))
    imgThresh = cv2.dilate(imgThresh, np.ones((5, 5), np.uint8))
    
    
    cv2.imshow('ball', imgThresh)
        
    # 빨간색 골프 공 윤곽선 찾기
    contours, _ = cv2.findContours(imgThresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    
    left_point_red, right_point_red = None, None
    
    # 가장 왼쪽과 오른쪽 점 찾기
    if contours:
        for contour in contours:
            for point in contour:
                x_red = point[0][0]
                y_red = point[0][1]

                # 가장 왼쪽에 있는 점 업데이트
                if left_point_red is None or x_red < left_point_red[0]:
                    left_point_red = [x_red, y_red]

                # 가장 오른쪽에 있는 점 업데이트
                if right_point_red is None or x_red > right_point_red[0]:
                    right_point_red = [x_red, y_red]

    # 결과 이미지에 표시
    if left_point is not None:
        cv2.circle(result, tuple(left_point_red), 5, (0, 255, 0), -1)
    if right_point is not None:
        cv2.circle(result, tuple(right_point_red), 5, (0, 255, 0), -1)
        
        
        

    # 홀인 여부 판단
    if left_point is not None and right_point is not None:
        A, A_prime = left_point[0], right_point[0]
        B, B_prime = left_point_red[0], right_point_red[0]
        
        if A < B < A_prime and A < B_prime < A_prime:
            hole_result = "HoleIn"
        else:
            hole_result = "NO"
    else:
        hole_result = "NO"
        
    return hole_result, result

# 영상 파일 경로 설정
video_path = "video/holein.avi"

# 영상 파일 열기
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # 골프 홀 인식 수행
    result, frame_with_points = detect_hole_in_golf_ball(frame)
    print(result)
    
    cv2.imshow('Video', frame_with_points)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
