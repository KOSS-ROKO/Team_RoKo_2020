import cv2
import numpy as np

# 비디오 캡처 객체 생성
cap = cv2.VideoCapture('video.mp4')

# HSV 색상 범위를 정의 (예를 들어, 빨간색 범위)
lower_red = np.array([0, 100, 100])
upper_red = np.array([16, 255, 255])

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break

    # BGR 색상 공간에서 HSV 색상 공간으로 변환
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # HSV 이미지에서 빨간색 범위를 마스킹
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # 마스킹을 적용하여 결과 이미지 생성
    result = cv2.bitwise_and(frame, frame, mask=mask)
    gauss = cv2.GaussianBlur(mask, (5,5), 0)

    # 커널 정의
    kernel = np.ones((5,5),np.uint8)

    # 팽창 연산
    dilation = cv2.dilate(gauss, kernel, iterations = 1)
    # 닫힘 연산
    closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)

    # 원 검출
    circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 1, 10, param1=50, param2=20, minRadius=0, maxRadius=70)

    # 원 그리기
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            cv2.circle(closing, (i[0], i[1]), i[2], (255, 255, 0), 2)

        cv2.imshow('HoughCircle', closing)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    
    # 결과 이미지 표시
    #cv2.imshow('frame', result)
    cv2.imshow('mask', mask)
    cv2.imshow('d', dilation)
    cv2.imshow('closing', closing)

    # 'q' 키를 누르면 종료q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
