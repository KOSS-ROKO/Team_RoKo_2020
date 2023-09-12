import cv2
import numpy as np

cap = cv2.VideoCapture('robot_ball.avi')  


while True:
    # 프레임 읽기
    ret, frame = cap.read()
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # 빨간색 범위를 정의
    lower_red = np.array([170, 100, 45])
    upper_red = np.array([177, 255, 255])
    
    # HSV 이미지에서 빨간색 마스크 생성
    mask = cv2.inRange(hsv, lower_red, upper_red)
    
    # 원본 이미지에서 마스크로 빨간색 부분 추출
    red_detected = cv2.bitwise_and(frame, frame, mask=mask)
    
    # 결과 화면 표시
    cv2.imshow('Original', frame)
    cv2.imshow('Red Detected', red_detected)
    
    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 작업 완료 후 리소스 해제
cap.release()
cv2.destroyAllWindows()
