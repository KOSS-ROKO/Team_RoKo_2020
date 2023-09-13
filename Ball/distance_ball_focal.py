'''
# 이 파일 원본 코드

import cv2
import numpy as np

# Define the known width of the object (in this case, the diameter of the ball in meters)
known_width = 3.0  # Adjust this value according to the actual size of the red ball

# Define the focal length of the camera (you need to calibrate your camera for this)
focal_length = 50  # Adjust this value based on your camera calibration

cap = cv2.VideoCapture('Ball/ball_video/ball3.avi')

# Calculate distance function
def calculate_distance(known_diameter, known_width, focal_length):
    return (known_diameter * focal_length) / (known_width * 2)

while True:
    # Read a frame
    ret, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper range for red color in HSV
    lower_red = np.array([170, 100, 45])
    upper_red = np.array([177, 255, 255])

    # Create a mask for the red color
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Apply the mask to the original frame
    red_detected = cv2.bitwise_and(frame, frame, mask=mask)

    # Find contours in the red mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Calculate the radius of the detected circle
        (x, y), radius = cv2.minEnclosingCircle(contour)

        # Check if the detected contour is big enough to be considered the ball
        if radius > 1:  # Adjust this threshold based on your needs
            # Calculate the distance to the red ball
            distance = calculate_distance(2 * radius, known_width, focal_length)
            # Draw the distance on the frame
            text = f"Distance: {distance:.2f} cm"
            cv2.putText(frame, text, (int(x) - 50, int(y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            print(text)

    # Display the original frame with distance information
    cv2.imshow('Original', frame)

    # 'q' key to quit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()


'''




import cv2
import numpy as np

# 빨간 공의 크기 (미터 단위로)
W = 0.1  # 예시로 10cm로 가정합니다.

# 빨간 공의 이미지에서의 가로 크기 (픽셀 단위로)
w = None  # 초점 거리 계산 후 설정합니다.

cap = cv2.VideoCapture('Ball/ball_video/ball4.avi')  

while True:
    # 프레임 읽기
    ret, frame = cap.read()
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # 빨간색 범위를 정의
    lower_red = np.array([150, 90, 40])
    upper_red = np.array([190, 255, 255])
     
    # HSV 이미지에서 빨간색 마스크 생성
    mask = cv2.inRange(hsv, lower_red, upper_red)
    
    # 원본 이미지에서 마스크로 빨간색 부분 추출
    red_detected = cv2.bitwise_and(frame, frame, mask=mask)
    
    # 빨간 공의 가로 크기를 측정 (w)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        print("this is w : ", w)
    
    # 초점 거리(f) 계산
    if w is not None:
        #f = (w * 30) / W  
        # 실제 거리(d) 계산
        d = (W * 230) / w
        #print("this is focal lenght:", f)
        print("빨간 공까지의 거리 (미터):", d)
    
    # 결과 화면 표시
    cv2.imshow('Original', frame)
    cv2.imshow('Red Detected', red_detected)
    
    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 작업 완료 후 리소스 해제
cap.release()
cv2.destroyAllWindows()
