import cv2
import numpy as np

# 빨간 공의 크기 (미터 단위로)
W = 0.04  # 예시로 10cm로 가정합니다

# 빨간 공의 이미지에서의 가로 크기 (픽셀 단위로)
w = None  # 초점 거리 계산 후 설정합니다.

cap = cv2.VideoCapture('Distance/holecup_video/holecup30.avi')  

while True:
    # 프레임 읽기
    ret, frame = cap.read()
    
    if not ret:
        print("비디오 종료")
        break
    
    
    
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_yellow = np.array([0, 80, 50])
    upper_yellow = np.array([36, 250, 250])

    yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
    yellow_objects = cv2.bitwise_and(frame, frame, mask=yellow_mask)

    blurred_frame = cv2.GaussianBlur(yellow_objects, (5, 5), 0)
    gray_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2GRAY)

    _, binary_frame = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    cv2.imshow('Binary Image', binary_frame)

    contours, _ = cv2.findContours(binary_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)        
    
    #cv2.drawContours(frame, [contours[0]], -1, (0, 255, 0), 2)

    ##### 홀 컵 점4개 찾기
    # 가장 왼쪽과 오른쪽, 위쪽 아래쪽 점 찾기
    xx, yy, ww, hh = 0,0,0,0
    
    left_point_yellow, right_point_yellow = None, None
    up_point_yellow, down_point_yellow = None, None
    
    if contours:
        for contour in contours:
            for point in contour:
                x = point[0][0]
                y = point[0][1]

                # 가장 왼쪽점 업데이트
                if left_point_yellow is None or x < left_point_yellow[0]:
                    left_point_yellow = [x, y]

                # 가장 오른쪽점 업데이트
                if right_point_yellow is None or x > right_point_yellow[0]:
                    right_point_yellow = [x, y]

                # 가장 아래점 업데이트
                if down_point_yellow is None or y > down_point_yellow[1]:
                    down_point_yellow = [x, y]

                diameter = 0
                # 가장 위쪽점 업데이트
                if down_point_yellow is not None:
                    diameter = 2 * abs(left_point_yellow[1] - down_point_yellow[1]) - 20

                # 제일 위쪽 점 계산
                up_point_yellow = [down_point_yellow[0], down_point_yellow[1] - diameter]


    result = frame.copy()
    if left_point_yellow is not None:
        cv2.circle(result, tuple(left_point_yellow), 5, (0, 0, 255), -1)
    if right_point_yellow is not None:
        cv2.circle(result, tuple(right_point_yellow), 5, (0, 0, 255), -1)

    if up_point_yellow is not None:
        cv2.circle(result, tuple(up_point_yellow), 5, (0, 0, 255), -1)
    if down_point_yellow is not None:
        cv2.circle(result, tuple(down_point_yellow), 5, (0, 0, 255), -1)
        
    #### x, y, w, h 계산     
    ww = right_point_yellow[0] - left_point_yellow[0]
    hh = down_point_yellow[1] - up_point_yellow[1]
    

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        print("-------------------", contours)
        x, y, w, h = cv2.boundingRect(largest_contour)
        cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)
        
        print("this is w :", ww, w)    


    #(left_point_yellow[0], up_point_yellow[1] ,ww, hh)   
    
    cv2.imshow("res", result)

    
    
    
    
    
    
    '''
    
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_yellow = np.array([0, 80, 50])
    upper_yellow = np.array([36, 250, 250])

    yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
    yellow_objects = cv2.bitwise_and(frame, frame, mask=yellow_mask)

    cv2.imshow('Yellow Objects', yellow_objects)

    blurred_frame = cv2.GaussianBlur(yellow_objects, (5, 5), 0)
    gray_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('Blurred Image', gray_frame)

    _, binary_frame = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    cv2.imshow('Binary Image', binary_frame)

    contours, _ = cv2.findContours(binary_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    

    max_area = 0  # 가장 큰 노란색 물체의 면적
    max_area_contour = None  # 가장 큰 노란색 물체의 컨투어

    for contour in contours:
        area = cv2.contourArea(contour)

        if area > max_area:
            max_area = area
            max_area_contour = contour

    if max_area_contour is not None:
        M = cv2.moments(max_area_contour)
        if M["m00"] != 0:
            center_x = int(M["m10"] / M["m00"])
            center_y = int(M["m01"] / M["m00"])

            # 노란색 물체의 크기에 따라 초록색 원 그리기
            radius = int(max_area ** 0.5 / 2)
            cv2.circle(frame, (center_x, center_y), radius, (0, 255, 0), 2)
            # 중심 좌표 표시
            cv2.circle(frame, (center_x, center_y), 2, (0, 0, 255), -1)

            # 중심 좌표가 초록색 원 안에 있는지 확인
            if center_x - radius >= 0 and center_x + radius < frame.shape[1] and center_y - radius >= 0 and center_y + radius < frame.shape[0]:
                # 노란색 물체의 중심이 초록색 원 안에 있을 때, 초록색 원을 그림
                cv2.circle(frame, (center_x, center_y), radius, (0, 255, 0), 2)
                
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)
    
        # 가장 큰 컨투어의 경계 상자 (x, y, 너비, 높이) 가져오기
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        # 프레임에 경계 상자 그리기
        #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
    '''
       
        

    # 초점 거리(f) 계산
    if w is not None:
        #f = (w * 30) / W 
        # 실제 거리(d) 계산
        d = (W * 270) / w
        #print("this is focal lenght:", f)
        print(f"홀컵까지의 거리 (미터): {d:.5f}")

    # 결과 화면 표시
    cv2.imshow('Original', frame)
    #cv2.imshow('Red Detected', red_detected)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# 작업 완료 후 리소스 해제
cap.release()
cv2.destroyAllWindows()