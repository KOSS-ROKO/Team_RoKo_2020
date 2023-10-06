import cv2
import numpy as np

class Field:
    
    def __init__(self):
        pass

    def detect_field(frame):

        # HSV 색상 공간으로 변환합니다.
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 경기장 초록색만 검출하기 위한 색상 범위
        # 경기장 색깔 범위 HSV : 색조, 채도, 명도
        lower_green = np.array([30, 70, 40])  # 초록색 최소값
        upper_green = np.array([85, 255, 255])  # 초록색 최대값

        # 초록색 영역을 마스킹합니다.
        mask = cv2.inRange(hsv, lower_green, upper_green)

        # 경계를 찾습니다.
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 경계를 그립니다.
        cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

        # 결과 프레임을 표시합니다.
        cv2.imshow('Edge Detection', frame)
