# -*- coding: utf-8 -*-
import platform
import numpy as np
import argparse
import cv2
import serial
import time
import sys
from threading import Thread

### ---------전역 변수 설정--------------
# 빨간색 범위
lower_red = np.array([170, 100, 45])
upper_red = np.array([177, 255, 255])

# 카메라 경로 설정
# cap = cv2.VideoCapture(0)
images = ['1.jpg', '2.jpg', '3.jpg', '4.jpg']

# 전체 화면 결과 창 크기 설정
cv2.namedWindow('Full Frame', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Full Frame', 800, 600)  # 적절한 크기로 조정

# 빨간 공만 보이는 창 생성
cv2.namedWindow('Red Objects', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Red Objects', 400, 300)

# Serial 변수
serial_use = 1
serial_port =  None
Read_RX =  0
receiving_exit = 1
threading_Time = 0.01
# ------------------------------------

### ----- CV 함수 ------
def extract_red_objects(frame): # 영상에서 빨간색만 추출하는 함수
    # BGR에서 HSV로 변환
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # 빨간색 범위로 이진화
    mask = cv2.inRange(hsv, lower_red, upper_red)
    
    # 이진화된 이미지에서 빨간색 객체만 추출
    red_objects = cv2.bitwise_and(frame, frame, mask=mask)
    
    return red_objects

def divide_screen(frame): # 화면을 11x11 그리드로 나누는 함수
    height, width = frame.shape[:2]
    cell_height = height // 11
    cell_width = width // 11
    
    # 그리드 라인 그리기
    for i in range(1, 11):
        cv2.line(frame, (0, i * cell_height), (width, i * cell_height), (0, 255, 0), 2)  # 녹색
        cv2.line(frame, (i * cell_width, 0), (i * cell_width, height), (0, 255, 0), 2)
    
    return frame

def process_images(image_list): # 이미지 cv 처리 함수

    for img in images:
        frame = cv2.imread(img)
        if frame is None:
            print(f"Failed to read image: {img}")
            continue   

        red_objects = extract_red_objects(frame) # 빨간색 객체 추출
        divided_frame = divide_screen(frame) # 화면을 11x11 그리드로 나누고 그리드 라인 그리기
        
        # 빨간색 객체 검출 및 위치 계산
        non_zero_pixels = np.transpose(np.nonzero(red_objects))
        
        if non_zero_pixels.size > 0:
            x_center = non_zero_pixels[:, 1].mean()
            y_center = non_zero_pixels[:, 0].mean()
            
            cell_width = divided_frame.shape[1] // 11

            # 빨간 공이 중앙 세로줄인 6번째 줄에서 검출되면 "stop" 출력
            if (cell_width * 5 <= x_center <= cell_width * 6): print("stop")
            elif x_center < cell_width * 5: # 1~5번째 줄에서 검출되면 "go right" 출력
                print("go right")
                TX_data_py2(serial_port, 30)
                time.sleep(1)
            elif x_center > cell_width * 6: # 7~11번째 줄에서 검출되면 "go left" 출력
                print("go left")
                TX_data_py2(serial_port, 28)
                time.sleep(1)

        else: print("go far")


        # 빨간 공만 보이는 창에 이미지 표시
        cv2.imshow('Red Objects', red_objects)
        
        # 전체 화면에 영상 출력
        cv2.imshow('Full Frame', frame)

        cv2.waitKey(10000) #10초 대기 후 다음 이미지

# ----------------------

### ----- Serial 함수 -----
def TX_data_py2(ser, one_byte):  # one_byte= 0~255

    ser.write(serial.to_bytes([one_byte])) 

def RX_data(ser):

    if ser.inWaiting() > 0:
        result = ser.read(1)
        RX = ord(result)
        return RX
    else:
        return 0
    
def Receiving(ser):
    global receiving_exit

    global X_255_point
    global Y_255_point
    global X_Size
    global Y_Size
    global Area, Angle


    receiving_exit = 1
    while True:
        if receiving_exit == 0:
            break
        time.sleep(threading_Time)
        while ser.inWaiting() > 0:
            result = ser.read(1)
            RX = ord(result)
            print ("RX=" + str(RX))
            
            # -----  remocon 16 Code  Exit ------
            if RX == 16:
                receiving_exit = 0
                break
# -------------------------


if __name__ == "__main__":

    # ---------- serial 통신 ------------
    BPS =  4800
    serial_port = serial.Serial('/dev/ttyS0', BPS, timeout=0.01)
    serial_port.flush()

    process_images(images)


    cv2.destroyAllWindows()
