import cv2
import numpy as np

# 빨간 공의 크기 (미터 단위로)
W = 0.18  # 예시로 10cm로 가정합니다

# 빨간 공의 이미지에서의 가로 크기 (픽셀 단위로)
w = None  # 초점 거리 계산 후 설정합니다.

cap = cv2.VideoCapture('Distance/holecup_video/holecup60.avi')  

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
    
    cv2.drawContours(frame, [contours[0]], -1, (0, 255, 0), 2)
    
    #contours_min = np.argmin(contours[0], axis = 0)
    #contours_max = np.argmax(contours[0], axis = 0)
    
     
    
    

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
                    #print("diameter", diameter)

                # 제일 위쪽 점 계산
                up_point_yellow = [down_point_yellow[0], down_point_yellow[1] - diameter]
                
    
    
    #contours[0][contours_max[0][0]][0][0] = down_point_yellow[1]
    
    #cv2.drawContours(frame, [contours[0]], -1, (0, 255, 0), 2)


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
    
    print("ww",ww)
    cv2.imshow("res", result)
    
    
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        #print("-------------------",contours)
        x, y, w, h = cv2.boundingRect(largest_contour)
        #cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)
        
        print("this is w :", w)    


    #(left_point_yellow[0], up_point_yellow[1] ,ww, hh)   
    
    
   
       
        

    # 초점 거리(f) 계산
    if w is not None:
        #f = (w * 30) / W 
        # 실제 거리(d) 계산
        d = (W * 360) / w
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