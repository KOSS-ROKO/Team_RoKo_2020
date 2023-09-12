'''
#원본
import cv2
import numpy as np

video_capture = cv2.VideoCapture('Flag/flag_video/flag2.avi')

focal_length = 100  # 카메라 초점 거리 (예: 500 pixel)

# 실제 깃발의 너비 (예: 30 cm)
flag_width_cm = 18

# 프레임 번호 초기화
frame_number = 0

while True:
    # 프레임 읽기
    ret, frame = video_capture.read()

    image_copy = frame.copy()


    if not ret:
        break

    if frame_number % 13 == 1: # 특정 프레임에서만 거리 계산 출력
        # 복사본 생성
        
        # 프레임을 HSV 색 공간으로 변환
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 노란색 범위 설정 (HSV 색상 값)
        #31, 170, 97
        #24, 240, 73
        #32, 115, 131
        lower_yellow = np.array([0, 50, 100])
        upper_yellow = np.array([36, 250, 255])

        # 노란색 마스크 생성
        yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)

        # 노란색 객체 검출
        yellow_objects = cv2.bitwise_and(frame, frame, mask=yellow_mask)

        # 객체를 그레이 스케일로 변환
        gray_frame = cv2.cvtColor(yellow_objects, cv2.COLOR_BGR2GRAY)

        # 에지 검출 (Canny 사용)
        edges = cv2.Canny(gray_frame, 50, 150)

        # 객체 검출 (윤곽선 사용)
        contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        # 검출된 객체 중에서 깃대와 삼각형을 구별
        for contour in contours:
            epsilon = 0.01 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            if len(approx) == 3:
                # 삼각형으로 판단
                for i in range(len(approx)):
                    cv2.line(image_copy, tuple(approx[i][0]), tuple(approx[(i+1) % 3][0]), (0, 255, 0), 3)
            elif len(approx) > 3:
                # 깃대로 판단
                cv2.drawContours(image_copy, [contour], -1, (0, 0, 255), 3)

                # 깃발 중심 위치 계산
                flag_center_x = int(np.mean(approx[:, 0, 0]))

                # 화면 중앙과 깃발 중심 x 좌표의 거리 계산
                pixel_distance = abs(frame.shape[1] // 2 - flag_center_x)

                # 거리 계산하기 전에 예외 처리 추가
                if pixel_distance != 0:
                    # 픽셀 거리를 실제 거리로 변환 (단위: cm)
                    distance_cm = (flag_width_cm * focal_length) / (2 * pixel_distance)

                    # 콘솔에 거리 출력
                    print(f'Distance to Flag: {distance_cm:.2f} cm')
                else:
                    # pixel_distance가 0이면 거리를 계산할 수 없음을 출력
                    print('Distance calculation not possible (pixel_distance is 0)')

        # 결과 영상 출력
        cv2.imshow('Origin', frame)
        cv2.imshow('Result', yellow_mask)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # 다음 프레임 번호 증가
    frame_number += 1

# 영상 재생 종료 후 리소스 해제
video_capture.release()
cv2.destroyAllWindows()

'''




# 원본에 팽창 전처리 추가
import cv2
import numpy as np

video_capture = cv2.VideoCapture('Flag/flag_video/flag1.avi')

while True:
    ret, frame = video_capture.read()

    if not ret:
        break

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_yellow = np.array([0, 50, 100])
    upper_yellow = np.array([36, 250, 255])

    yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
    yellow_objects = cv2.bitwise_and(frame, frame, mask=yellow_mask)
    
    gauss = cv2.GaussianBlur(yellow_mask, (5,5), 0)
    kernel = np.ones((5,5),np.uint8)
    
    dilation = cv2.dilate(gauss, kernel, iterations = 1)
    closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)
     
    

    #gray_frame = cv2.cvtColor(yellow_objects, cv2.COLOR_BGR2GRAY)
    
    # 원 검출
    #circles = cv2.HoughCircles(yellow_mask, cv2.HOUGH_GRADIENT, 1, 10, param1=50, param2=20, minRadius=0, maxRadius=70)

    # 원 검출
    circles = cv2.HoughCircles(
        yellow_mask, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=30, minRadius=0, maxRadius=70)

    # 원 그리기
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center_x, center_y, radius = i
            cv2.circle(closing, (i[0], i[1]), i[2], (255, 255, 0), 2)
            # "circle" 텍스트 출력
            cv2.putText(closing, "circle", (center_x - 20, center_y - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

   
            

    cv2.imshow('Result', frame)
    cv2.imshow('1', yellow_mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()













