import cv2
import numpy as np

cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)
cap.set(5, 5)

while True:
    ret, frame = cap.read()

    if not ret:
        break
    '''
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_yellow = np.array([15, 100, 70])
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

            radius = int(max_area ** 0.5 / 2)
            cv2.circle(frame, (center_x, center_y), radius, (0, 255, 0), 2)
            cv2.circle(frame, (center_x, center_y), 2, (0, 0, 255), -1)

            if center_x - radius >= 0 and center_x + radius < frame.shape[1] and center_y - radius >= 0 and center_y + radius < frame.shape[0]:
                cv2.circle(frame, (center_x, center_y), radius, (0, 255, 0), 2)
    '''


    # 노란색 홀컵 검출
    yellow_lower = np.array([0, 71, 122])
    yellow_upper = np.array([36, 250, 250])
    
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    yellow_mask = cv2.inRange(hsv_frame, yellow_lower, yellow_upper)
    yellow_objects = cv2.bitwise_and(frame, frame, mask=yellow_mask)
    
    blurred_frame = cv2.GaussianBlur(yellow_objects, (5, 5), 0)
    gray_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2GRAY)
    
    _, binary_frame = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    # 이미지 전처리 - 침식, 팽창
    kernel = np.ones((5, 5), np.uint8)
    binary_frame = cv2.erode(binary_frame, kernel, iterations=1)
    binary_frame = cv2.dilate(binary_frame, kernel, iterations=1)
    
    cv2.imshow('Yellow Holecup Binary Image', binary_frame) # 이진화된 이미지 표시
    
    contours, _ = cv2.findContours(binary_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # 노란색 홀컵 윤곽선
    
    
    ##### 가장 왼쪽과 오른쪽, 위쪽 아래쪽 점 찾기
    
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
        
        
        
    #############여기서부터 빨간공
    
    
    # 빨간공 인식
    #imgThresh = self.detect_ball(frame)
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
    imgThreshLow = cv2.inRange(imgHSV, (0, 200, 155), (50, 255, 255))
    imgThreshHigh = cv2.inRange(imgHSV, (160, 155, 50), (179, 255, 255))
    
    imgThresh = cv2.add(imgThreshLow, imgThreshHigh)

    imgThresh = cv2.GaussianBlur(imgThresh, (3, 3), 2)
    imgThresh = cv2.erode(imgThresh, np.ones((5, 5), np.uint8))
    imgThresh = cv2.dilate(imgThresh, np.ones((5, 5), np.uint8))
    


    red_contours, _ = cv2.findContours(imgThresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if red_contours:
        red_max_contour = max(red_contours, key=cv2.contourArea)
        M = cv2.moments(red_max_contour)
        if M["m00"] != 0:
            red_center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])) 
            print(red_center)     
    else:
        print("none")

    cv2.imshow('Red Ball Binary Image', imgThresh) # 이진화된 이미지 표시
        
    contours, _ = cv2.findContours(imgThresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # 빨간색 골프 공 윤곽선
    
    
    ##### 가장 왼쪽과 오른쪽, 위쪽과 아래쪽 점 찾기

    left_point_red, right_point_red = None, None
    up_point_red, down_point_red = None, None
    
    if contours:
        for contour in contours:
            for point in contour:
                x_red = point[0][0]
                y_red = point[0][1]

                # 가장 왼쪽점 업데이트
                if left_point_red is None or x_red < left_point_red[0]:
                    left_point_red = [x_red, y_red]
                    #print(1)

                # 가장 오른쪽점 업데이트
                if right_point_red is None or x_red > right_point_red[0]:
                    right_point_red = [x_red, y_red]
                    #print(2)

                # 가장 위쪽점 업데이트
                if up_point_red is None or y_red < up_point_red[1]:
                    up_point_red = [x_red, y_red]
                    #print(3)

                # 가장 아래쪽점 업데이트
                if down_point_red is None or y_red > down_point_red[1]:
                    down_point_red = [x_red, y_red]
                    #print(4)


    if left_point_red is not None:
        cv2.circle(result, tuple(left_point_red), 5, (0, 255, 0), -1)
        print("red left", left_point_red)
    if right_point_red is not None:
        cv2.circle(result, tuple(right_point_red), 5, (0, 255, 0), -1)
        print("red right", right_point_red)
        
    if up_point_red is not None:
        cv2.circle(result, tuple(up_point_red), 5, (0, 255, 0), -1)
        print("red up", up_point_red)
    if down_point_red is not None:
        cv2.circle(result, tuple(down_point_red), 5, (0, 255, 0), -1)
        print("red down", down_point_red)



    ##### 홀인 여부 판단
    if left_point_yellow is not None and left_point_yellow is not None:
        A, A_prime = left_point_yellow[0], right_point_yellow[0]
        B, B_prime = left_point_red[0], right_point_red[0]

        C, C_prime = up_point_yellow[1], down_point_yellow[1]
        D, D_prime = up_point_red[1], down_point_red[1]
        
        #if A < B < A_prime and A < B_prime < A_prime and C < D < C_prime and C < D_prime < C_prime:
        if A < B < B_prime < A_prime and C < D < D_prime < C_prime:
            hole_result = True 
        else:
            hole_result = False
    else:
        hole_result = False
        
    print(hole_result)      



    cv2.imshow('Result', result)
    #cv2.imshow('masked', yellow_mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
