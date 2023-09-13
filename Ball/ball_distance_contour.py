import cv2
import numpy as np

W = 0.0427  # 빨간 공 크기 : 4.27 cm

# 빨간 공의 이미지에서의 가로 크기 (픽셀 단위로)
w = None  # 초점 거리 계산 후 설정합니다.

cap = cv2.VideoCapture('Ball/ball_video/ball1.avi')  

# 프레임 번호 초기화
frame_number = 0

while True:
    # 프레임 읽기
    ret, frame = cap.read()
    
    if frame_number % 8 == 1: # 특정 프레임에서만 거리 계산 출력
    
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # 빨간색 범위를 정의
        lower_red = np.array([150, 90, 40])
        upper_red = np.array([190, 255, 255])
        
        # HSV 이미지에서 빨간색 마스크 생성
        mask = cv2.inRange(hsv, lower_red, upper_red)
        
        # 원본 이미지에서 마스크로 빨간색 부분 추출
        red_detected = cv2.bitwise_and(frame, frame, mask=mask)
        
        # 빨간 공의 가로 크기를 카메라 센서 단위로 측정 (w)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            #print("this is w : ", w)
        
        if w is not None:
            
            #f = (w * 30) / W # 초점 거리(f) 계산
            #print("this is focal length: ", f)
            d = (W * 510) / w # 510 -> focal length, 실제 거리(d) 계산
            print(f"Ball Distance: {d:.2f} m")

        
        # 결과 화면 표시
        cv2.imshow('Original', frame)
        cv2.imshow('Red Detected', red_detected)
    
    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    frame_number += 1 # 다음 프레임 번호 증가

# 작업 완료 후 리소스 해제
cap.release()
cv2.destroyAllWindows()
