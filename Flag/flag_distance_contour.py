# 컨투어로 깃발의 원형을 찾은 후, focal length로 거리 측정
# 아직은 깃발 인식하는 코드 전처리 + 정확하게 할 필요 ㅇ


import cv2
import numpy as np

cap = cv2.VideoCapture('Flag/flag_video/flag3.avi')

detected_circles = []

W = 0.18  # 실제 홀컵 가로 크기(미터 단위, ex) 0.18 m -> 18cm )

frame_number = 0 # 프레임 번호 초기화

while True:
    ret, frame = cap.read()

    if not ret:
        break
    
    if frame_number % 5 == 1: # 특정 프레임에서만 거리 계산 출력

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_yellow = np.array([0, 50, 100])
        upper_yellow = np.array([36, 250, 255])

        yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
        yellow_objects = cv2.bitwise_and(frame, frame, mask=yellow_mask)

        gray_frame = cv2.cvtColor(yellow_objects, cv2.COLOR_BGR2GRAY) # 노란색 객체를 그레이 스케일로 변환

        edges = cv2.Canny(gray_frame, 50, 150) # 에지 검출 (Canny 사용)
        
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # 객체 검출 (컨투어 사용)
        
        # 카메라 센서 w 크기 측정
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            #print("this is w : ", w)

        detected_circles = []  # 감지된 원의 정보를 저장할 리스트 초기화

        # 검출된 원 정보 저장
        for contour in contours:
            min_radius = 20
            max_radius = 80
            epsilon = 0.05 * cv2.arcLength(contour, True) # 엡실론 값 조정
            approx = cv2.approxPolyDP(contour, epsilon, True)

            if len(approx) >= 6:
                center, _ = cv2.minEnclosingCircle(contour)
                center = tuple(map(int, center))
                radius = int(cv2.arcLength(contour, True) / (2 * np.pi))

                if min_radius <= radius <= max_radius:
                    detected_circles.append((center, radius))
                     
                    #f = (w * 30) / W # 초점 거리(f) 계산
                    #print("this is focal length: ", f)
                    d = (W * 230) / w # 230 -> focal length, 실제 거리(d) 계산
                    print(f"Flag Distance: {d:.2f} m")

                    # 원 그리기
                    cv2.circle(frame, center, radius, (0, 255, 0), 2)
            

        cv2.imshow('Result', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    frame_number += 1 # 프레임 번호 증가

cap.release()
cv2.destroyAllWindows()
