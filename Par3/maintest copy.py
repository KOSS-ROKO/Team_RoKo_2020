# -*- coding: utf-8 -*-
import platform
import numpy as np
import argparse
import cv2
import serial
import time
import sys
from threading import Thread
import csv
import math
from Head import Head
from Motion import Motion
import Distance

X_255_point = 0
Y_255_point = 0
X_Size = 0
Y_Size = 0
Area = 0
Angle = 0
#-----------------------------------------------
Top_name = 'mini CTS5 setting'
hsv_Lower = 0
hsv_Upper = 0

hsv_Lower0 = 0
hsv_Upper0 = 0

hsv_Lower1 = 0
hsv_Upper1 = 0

#----------- 
color_num = [   0,  1,  2,  3,  4]
    
h_max =     [ 255, 65,196,111,110]
h_min =     [  55,  0,158, 59, 74]
    
s_max =     [ 162,200,223,110,255]
s_min =     [ 114,140,150, 51,133]
    
v_max =     [  77,151,239,156,255]
v_min =     [   0,95,104, 61,104]
    
min_area =  [  50, 50, 50, 10, 10]

now_color = 0
serial_use = 1

serial_port =  None
Temp_count = 0
Read_RX =  0

mx,my = 0,0

threading_Time = 5/1000.

Config_File_Name ='Cts5_v1.dat'

#----------------------------------------------------------
x0, y0, w0, h0, a0, b0, c0, d0 = 0,0,0,0,0,0,0,0
x1, y1, w1, h1, a1, b1, c1, d1 = 0,0,0,0,0,0,0,0
global red_ball
global is_red_ball
global red_ball_center
global red_Area
global yellow_object
global is_yellow_object
global yellow_object_center
global yellow_Area
global yellow_object_bottom

first_big_ud_angle = 0  # first_big_ud_angle 살향 여부 확인
big_ud_angle = 0
is_big_UD = 0

ACT = 0

n = 0   # 가로 세로 줄 수

#----------------------------------------------------------

def nothing(x):
    pass

#-----------------------------------------------
def create_blank(width, height, rgb_color=(0, 0, 0)):

    image = np.zeros((height, width, 3), np.uint8)
    color = tuple(reversed(rgb_color))
    image[:] = color

    return image
#-----------------------------------------------
def draw_str2(dst, target, s):
    x, y = target
    cv2.putText(dst, s, (x+1, y+1), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 0), thickness = 2, lineType=cv2.LINE_AA)
    cv2.putText(dst, s, (x, y), cv2.FONT_HERSHEY_PLAIN, 0.8, (255, 255, 255), lineType=cv2.LINE_AA)
#-----------------------------------------------
def draw_str3(dst, target, s):
    x, y = target
    cv2.putText(dst, s, (x+1, y+1), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 0), thickness = 2, lineType=cv2.LINE_AA)
    cv2.putText(dst, s, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), lineType=cv2.LINE_AA)
#-----------------------------------------------
def draw_str_height(dst, target, s, height):
    x, y = target
    cv2.putText(dst, s, (x+1, y+1), cv2.FONT_HERSHEY_PLAIN, height, (0, 0, 0), thickness = 2, lineType=cv2.LINE_AA)
    cv2.putText(dst, s, (x, y), cv2.FONT_HERSHEY_PLAIN, height, (255, 255, 255), lineType=cv2.LINE_AA)
#-----------------------------------------------
def clock():
    return cv2.getTickCount() / cv2.getTickFrequency()
#-----------------------------------------------
def Trackbar_change(now_color):
    global  hsv_Lower,  hsv_Upper
    hsv_Lower = (h_min[now_color], s_min[now_color], v_min[now_color])
    hsv_Upper = (h_max[now_color], s_max[now_color], v_max[now_color])
#-----------------------------------------------
def Hmax_change(a):
    
    h_max[now_color] = cv2.getTrackbarPos('Hmax', Top_name)
    Trackbar_change(now_color)
#-----------------------------------------------
def Hmin_change(a):
    
    h_min[now_color] = cv2.getTrackbarPos('Hmin', Top_name)
    Trackbar_change(now_color)
#-----------------------------------------------
def Smax_change(a):
    
    s_max[now_color] = cv2.getTrackbarPos('Smax', Top_name)
    Trackbar_change(now_color)
#-----------------------------------------------
def Smin_change(a):
    
    s_min[now_color] = cv2.getTrackbarPos('Smin', Top_name)
    Trackbar_change(now_color)
#-----------------------------------------------
def Vmax_change(a):
    
    v_max[now_color] = cv2.getTrackbarPos('Vmax', Top_name)
    Trackbar_change(now_color)
#-----------------------------------------------
def Vmin_change(a):
    
    v_min[now_color] = cv2.getTrackbarPos('Vmin', Top_name)
    Trackbar_change(now_color)
#-----------------------------------------------
def min_area_change(a):
   
    min_area[now_color] = cv2.getTrackbarPos('Min_Area', Top_name)
    if min_area[now_color] == 0:
        min_area[now_color] = 1
        cv2.setTrackbarPos('Min_Area', Top_name, min_area[now_color])
    Trackbar_change(now_color)
#-----------------------------------------------
def Color_num_change(a):
    global now_color, hsv_Lower,  hsv_Upper
    now_color = cv2.getTrackbarPos('Color_num', Top_name)
    cv2.setTrackbarPos('Hmax', Top_name, h_max[now_color])
    cv2.setTrackbarPos('Hmin', Top_name, h_min[now_color])
    cv2.setTrackbarPos('Smax', Top_name, s_max[now_color])
    cv2.setTrackbarPos('Smin', Top_name, s_min[now_color])
    cv2.setTrackbarPos('Vmax', Top_name, v_max[now_color])
    cv2.setTrackbarPos('Vmin', Top_name, v_min[now_color])
    cv2.setTrackbarPos('Min_Area', Top_name, min_area[now_color])

    hsv_Lower = (h_min[now_color], s_min[now_color], v_min[now_color])
    hsv_Upper = (h_max[now_color], s_max[now_color], v_max[now_color])
#----------------------------------------------- 
def TX_data(ser, one_byte):  # one_byte= 0~255
    #ser.write(chr(int(one_byte)))          #python2.7
    ser.write(serial.to_bytes([one_byte]))  #python3
#-----------------------------------------------
def RX_data(serial):
    global Temp_count
    try:
        if serial.inWaiting() > 0:
            result = serial.read(1)
            RX = ord(result)
            return RX
        else:
            return 0
    except:
        Temp_count = Temp_count  + 1
        print("Serial Not Open " + str(Temp_count))
        return 0
        pass
#-----------------------------------------------
# mouse callback function
def mouse_move(event,x,y,flags,param):
    global mx, my

    if event == cv2.EVENT_MOUSEMOVE:
        mx, my = x, y
# *************************
def RX_Receiving(ser):
    global receiving_exit,threading_Time

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
# *************************
def GetLengthTwoPoints(XY_Point1, XY_Point2):
    return math.sqrt( (XY_Point2[0] - XY_Point1[0])**2 + (XY_Point2[1] - XY_Point1[1])**2 )
# *************************
def FYtand(dec_val_v ,dec_val_h):
    return ( math.atan2(dec_val_v, dec_val_y) * (180.0 / math.pi))
#degree 값을 라디안 값으로 변환하는 함수
def FYrtd(rad_val ):
    return  (rad_val * (180.0 / math.pi))
# *************************
# 라디안값을 degree 값으로 변환하는 함수
def FYdtr(dec_val):
    return  (dec_val / 180.0 * math.pi)
# *************************
def GetAngleTwoPoints(XY_Point1, XY_Point2):
    xDiff = XY_Point2[0] - XY_Point1[0]
    yDiff = XY_Point2[1] - XY_Point1[1]
    cal = math.degrees(math.atan2(yDiff, xDiff)) + 90
    if cal > 90:
        cal =  cal - 180
    return  cal
# *************************
def hsv_setting_save():

    global Config_File_Name, color_num
    global color_num, h_max, h_min 
    global s_max, s_min, v_max, v_min, min_area
    
    try:
    #if 1:
        saveFile = open(Config_File_Name, 'w')
        i = 0
        color_cnt = len(color_num)
        while i < color_cnt:
            text = str(color_num[i]) + ","
            text = text + str(h_max[i]) + "," + str(h_min[i]) + ","
            text = text + str(s_max[i]) + "," + str(s_min[i]) + ","
            text = text + str(v_max[i]) + "," + str(v_min[i]) + ","
            text = text + str(min_area[i])  + "\n"
            saveFile.writelines(text)
            i = i + 1
        saveFile.close()
        print("hsv_setting_save OK")
        return 1
    except:
        print("hsv_setting_save Error~")
        return 0
#************************
def hsv_setting_read():
    global Config_File_Name
    global color_num, h_max, h_min 
    global s_max, s_min, v_max, v_min, min_area

    #try:
    if 1:
        with open(Config_File_Name) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            i = 0
            
            for row in readCSV:
                color_num[i] = int(row[0])
                h_max[i] = int(row[1])
                h_min[i] = int(row[2])
                s_max[i] = int(row[3])
                s_min[i] = int(row[4])
                v_max[i] = int(row[5])
                v_min[i] = int(row[6])
                min_area[i] = int(row[7])
                
                i = i + 1
              
        csvfile.close()
        print("hsv_setting_read OK")
        return 1
# **************************************************

if __name__ == '__main__':
    #-------------------------------------
    print ("-------------------------------------")
    print ("(2020-1-20) mini CTS5 Program.  MINIROBOT Corp.")
    print ("-------------------------------------")
    print ("")
    os_version = platform.platform()
    print (" ---> OS " + os_version)
    python_version = ".".join(map(str, sys.version_info[:3]))
    print (" ---> Python " + python_version)
    opencv_version = cv2.__version__
    print (" ---> OpenCV  " + opencv_version)
    #-------------------------------------
    #---- user Setting -------------------
    #-------------------------------------
    W_View_size =  640  #320  #640
    #H_View_size = int(W_View_size / 1.777)
    H_View_size = int(W_View_size / 1.333)

    BPS =  4800  # 4800,9600,14400, 19200,28800, 57600, 115200
    serial_use = 1
    now_color = 0
    View_select = 0
    #-------------------------------------
    print(" ---> Camera View: " + str(W_View_size) + " x " + str(H_View_size) )
    print ("-------------------------------------")
    #-------------------------------------
    try:
        hsv_setting_read()
    except:
        hsv_setting_save()
    #-------------------------------------------------------------------------
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video",
                    help="path to the (optional) video file")
    ap.add_argument("-b", "--buffer", type=int, default=64,
                    help="max buffer size")
    args = vars(ap.parse_args())

    img = create_blank(320, 100, rgb_color=(0, 0, 255))
    
    cv2.namedWindow(Top_name)
    cv2.moveWindow(Top_name,0,0)
    
    cv2.createTrackbar('Hmax', Top_name, h_max[now_color], 255, Hmax_change)
    cv2.createTrackbar('Hmin', Top_name, h_min[now_color], 255, Hmin_change)
    cv2.createTrackbar('Smax', Top_name, s_max[now_color], 255, Smax_change)
    cv2.createTrackbar('Smin', Top_name, s_min[now_color], 255, Smin_change)
    cv2.createTrackbar('Vmax', Top_name, v_max[now_color], 255, Vmax_change)
    cv2.createTrackbar('Vmin', Top_name, v_min[now_color], 255, Vmin_change)
    cv2.createTrackbar('Min_Area', Top_name, min_area[now_color], 255, min_area_change)
    cv2.createTrackbar('Color_num', Top_name,color_num[now_color], 4, Color_num_change)

    Trackbar_change(now_color)

    draw_str3(img, (15, 25), 'MINIROBOT Corp.')
    draw_str2(img, (15, 45), 'space: Fast <=> Video and Mask.')
    draw_str2(img, (15, 65), 's, S: Setting File Save')
    draw_str2(img, (15, 85), 'Esc: Program Exit')
    
    
    cv2.imshow(Top_name, img)
    
    #---------------------------
    if not args.get("video", False):
        camera = cv2.VideoCapture(0)
    else:
        camera = cv2.VideoCapture(args["video"])
    #---------------------------
    camera.set(3, W_View_size)
    camera.set(4, H_View_size) 
    camera.set(5, 30)
    time.sleep(0.5)
    #---------------------------
    (grabbed, frame) = camera.read()
    draw_str2(frame, (5, 15), 'X_Center x Y_Center =  Area' )
    draw_str2(frame, (5, H_View_size - 5), 'View: %.1d x %.1d.  Space: Fast <=> Video and Mask.'
                      % (W_View_size, H_View_size))
    draw_str_height(frame, (5, int(H_View_size/2)), 'Fast operation...', 3.0 )
    mask = frame.copy()
    cv2.imshow('mini CTS5 - Video', frame )
    cv2.imshow('mini CTS5 - Mask', mask)
    cv2.moveWindow('mini CTS5 - Mask',322 + W_View_size,36)
    cv2.moveWindow('mini CTS5 - Video',322,36)
    cv2.setMouseCallback('mini CTS5 - Video', mouse_move)

    #---------------------------
    if serial_use != 0:  # python3
    #if serial_use <> 0:  # python2.7
        BPS =  4800  # 4800,9600,14400, 19200,28800, 57600, 115200
        #---------local Serial Port : ttyS0 --------
        #---------USB Serial Port : ttyAMA0 --------
        serial_port = serial.Serial('/dev/ttyS0', BPS, timeout=0.01)
        serial_port.flush() # serial cls
        time.sleep(0.5)
    
        serial_t = Thread(target=RX_Receiving, args=(serial_port,))
        serial_t.daemon = True
        serial_t.start()
        
    # First -> Start Code Send 
    TX_data(serial_port, 250)
    TX_data(serial_port, 250)
    TX_data(serial_port, 250)
    
    old_time = clock()

    View_select = 0
    msg_one_view = 0
    
    #########################################################################
    ############################ 영상 처리 알고리즘 #############################
    #########################################################################
 
    head = Head()
    motion = Motion()
    
    ACT = "TEESHOT"




    def detect_ball(role="call_TF"):
        print("detect ball start")
        if(role=="call_TF"):  
            return is_red_ball
        elif(role=="call_video"):
            return a0, b0, c0, d0       #12,3,6,9   
        elif(role=="call_midpoint"):
            if is_red_ball: return red_ball_center
            else:           return None

    def detect_holecup(role="call_TF"): 
        if (role=="call_TF"):  
            return is_yellow_object
        elif (role=="call_video"): ## 홀컵의 w 크기 return
            return a1, b1, c1, d1
        elif (role=="call_midpoint"): ## 홀컵의 중앙 좌표 return
            return yellow_object_center
        elif (role == "bottom_point"):
            return c1
    
    def par4_direction(self):
        return yellow_object_center
    
    def middle_lr_ball(self):
        print("middle_lr_ball")
        if not detect_ball():
            return None
        x_center, y_center = red_ball_center
        cell_width = W_View_size // 11
        if (cell_width * 5 <= x_center <= cell_width * 6):
            print("stop")
            return "stop"
        elif x_center < cell_width * 5:
            print("right")
            return "right"
        elif x_center > cell_width * 6:
            print("left")
            return "left"
    
    def middle_ud_ball(self):
        print("middle_ud_ball")
        if not detect_ball():
            return None
        x_center, y_center = red_ball_center
        cell_height = H_View_size // 13
        # 빨간 공이 중앙 가로줄인 6번째 줄에서 검출되면 "stop" 출력
        if (cell_height * 5 <= y_center <= cell_height * 6):
            return "stop"
        # 1~5번째 줄에서 검출되면 "go up" 출력
        elif y_center < cell_height * 5:
            return "up"
        # 7~11번째 줄에서 검출되면 "go down" 출력
        elif y_center > cell_height * 6:
            return "down"    
    
    def middle_lr_holecup(self):
        print("middle_lr_holecup")
        if not detect_holecup():
            return None
        x_center, y_center = yellow_object_center
        cell_width = W_View_size // n
        if (cell_width * (n//2) <= x_center <= cell_width * (n//2+1)):
            print("stop")
            return "stop"
        elif x_center < cell_width * (n//2):
            print("right")
            return "right"
        elif x_center > cell_width * (n//2+1):
            print("left")
            return "left"  
        
    def middle_ud_holecup(self):
        print("middle_ud_holecup")
        if not detect_holecup():
            return None
        x_center, y_center = yellow_object_center
        cell_height = W_View_size // n
        
        # 빨간 공이 중앙 가로줄인 6번째 줄에서 검출되면 "stop" 출력
        if (cell_height * 6 <= y_center <= cell_height * 7):
            return "stop"
        # 1~5번째 줄에서 검출되면 "go up" 출력
        elif y_center < cell_height * 6:
            return "up"
        # 7~11번째 줄에서 검출되면 "go down" 출력
        elif y_center > cell_height * 7:
            return "down"
        # else:
        #     return "go far"              
        
    def big_UD_head(self, detect_object, big_ud_angle):
        check = False
        max_down_flag = 0
        print("big ud start !!")
        if detect_object == 'ball':
            check = is_red_ball
        elif detect_object == 'holecup':
            check = is_yellow_object
        if check == True:
            print("ball is detected")
            return True, big_ud_angle # small head 부르기
        
        else:   # 물체가 화면에 안 보이는 경우 detect : False
                # 고개 각도 크게 돌리기, Find ball과 다름
            if max_down_flag == 0:
                motion.head("DOWN", 30) ################# 3도보단 큰 각으로
                big_ud_angle -= 30 # 10은 임의 값
                if big_ud_angle == 10: # <-max() 에러 안 나려고 적어 놓음, 바꾸삼 / 최대값이면 
                    max_down_flag = 1
                    big_ud_angle = 64
                    time.sleep(1)
                    motion.head("UP", 30) # 고개 45도로 내리고 공 detect 시작 ! / 나중에 UP 45도 모션 추가할듯?
                    motion.head("UP", 9)
                    motion.head("UP", 6)
                    motion.head("UP", 9) ###
                    time.sleep(1)
            elif max_down_flag == 1:
                motion.head("UP", 30) ################# 3도보단 큰 각으로
                big_ud_angle += 30 # 30은 임의 값
            return False, big_ud_angle
    
    def ball_small_LR(object="ball"):   # ball은 small lr끝난뒤 몸 돌리고 고개 default함
            Distance.head_lr_angle = 100
            while True:
                print("---------start small lr head")
                is_vertical_middle, small_lr_temp = head.small_LR_head(object, Distance.head_lr_angle)
                if is_vertical_middle == True:
                    return "Success" #break
    
                elif is_vertical_middle == False:
                    Distance.head_lr_angle = small_lr_temp
                    continue
                else : # is_vertical_middle == Except_
                    return "Except"
    
    
    
    
    ###########
    def ball_pos(): ## 건웅 오빠
        
        motion.head("DEFAULT",63)

        time.sleep(1)
        print("++++++++++++++++++")
        print("ball pos")
        print("++++++++++++++++++")
        is_center = False
        rx,ry = reference_point = [380, 322]
        w = 20
        rectangle_coordinates = [rx-w, ry-w, rx+w, ry-w, rx+w, ry+w, rx-w, ry+w]
        while not is_center:
            motion.head("DEFAULT",63)
            time.sleep(2)
            x1, y1, x2, y2, x3, y3, x4, y4 = rectangle_coordinates
            print("현재 빨간공 중심: ", red_ball_center ,"목표 지점: ",reference_point)
            if(x1 <= red_ball_center[0] <= x2 and y1 <= red_ball_center[1] <= y4):    
                print("성공함요")
                break                              
            if(red_ball_center == None): 
                print("지금 화면안에 빨간 공 안보임")
                motion.walk("2JBACKWARD")
                time.sleep(2)
                continue
            dx = red_ball_center[0] - reference_point[0]
            dy = red_ball_center[1] - reference_point[1]
            
            print("중앙에서 떨어진 거리: ", dx, dy, abs(dx),abs(dy))
            print("dx//30: ",dx//30 ,"dy//30",dy//30)
            if(abs(dy)>=30):
                if (dy<0):
                    motion.walk("2JFORWARD")
                    print("1")
                else:
                    motion.walk("2JBACKWARD")
                    print("2")
            elif(abs(dx)>=30):
                if (dx<0):
                    motion.walk_side("LEFT10")
                    print("3")
                else:
                    motion.walk_side("RIGHT10")
                    print("4")
            else:
                is_center = True
    
    #########################################################################
    #########################################################################
    #########################################################################
    # -------- Main Loop Start --------
    while True:

        # grab the current frame
        (grabbed, frame) = camera.read()

        if args.get("video") and not grabbed:
            break
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)  # HSV => YUV
        mask = cv2.inRange(hsv, hsv_Lower, hsv_Upper)
        
        hsv_Lower = (h_min[now_color], s_min[now_color], v_min[now_color])
        hsv_Upper = (h_max[now_color], s_max[now_color], v_max[now_color])
        
        
        mask0 = cv2.inRange(hsv, (h_min[0], s_min[0], v_min[0]), (h_max[0], s_max[0], v_max[0]))
        mask1 = cv2.inRange(hsv, (h_min[1], s_min[1], v_min[1]), (h_max[1], s_max[1], v_max[1]))
        '''
        mask2 = cv2.inRange(hsv, (h_min[2], s_min[2], v_min[2]), (h_max[2], s_max[2], v_max[2]))
        mask3 = cv2.inRange(hsv, (h_min[3], s_min[3], v_min[3]), (h_max[3], s_max[3], v_max[3]))
        mask4 = cv2.inRange(hsv, (h_min[4], s_min[4], v_min[4]), (h_max[4], s_max[4], v_max[4]))
        '''
        
        mask = cv2.erode(mask, None, iterations=1)
        mask = cv2.dilate(mask, None, iterations=1)
        mask = cv2.GaussianBlur(mask, (3, 3), 2)  # softly
        
        mask0 = cv2.erode(mask0, None, iterations=1)
        mask0 = cv2.dilate(mask0, None, iterations=1)
        mask0 = cv2.GaussianBlur(mask0, (3, 3), 2)  # softly
        mask1 = cv2.erode(mask1, None, iterations=1)
        mask1 = cv2.dilate(mask1, None, iterations=1)
        mask1 = cv2.GaussianBlur(mask1, (3, 3), 2)  # softly
        
        #mask = cv2.erode(mask, None, iterations=1)
        #mask = cv2.dilate(mask, None, iterations=1)
        #mask = cv2.GaussianBlur(mask, (3, 3), 2)  # softly

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        cnts0 = cv2.findContours(mask0.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        cnts1 = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        
        '''
        cnts2 = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        cnts3 = cv2.findContours(mask3.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        cnts4 = cv2.findContours(mask4.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        '''
        center = None
        
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((X, Y), radius) = cv2.minEnclosingCircle(c)
            Area = cv2.contourArea(c) / min_area[now_color]
            if Area > 255:
                Area = 255
            if Area > min_area[now_color]:
                x4, y4, w4, h4 = cv2.boundingRect(c)
                cv2.rectangle(frame, (x4, y4), (x4 + w4, y4 + h4), (0, 255, 0), 2)
                #----------------------------------------
                X_Size = int((255.0 / W_View_size) * w4)
                Y_Size = int((255.0 / H_View_size) * h4)
                X_255_point = int((255.0 / W_View_size) * X)
                Y_255_point = int((255.0 / H_View_size) * Y)
        else:
            x = 0
            y = 0
            X_255_point = 0
            Y_255_point = 0
            X_Size = 0
            Y_Size = 0
            Area = 0
            Angle = 0

        if len(cnts0) > 0:
            c0 = max(cnts0, key=cv2.contourArea)
            ((X, Y), radius) = cv2.minEnclosingCircle(c0)
            Area = cv2.contourArea(c0) / min_area[now_color]
            if Area > 255:
                Area = 255
            if Area > min_area[now_color]:
                x4, y4, w4, h4 = cv2.boundingRect(c0)
                a0, b0, c0, d0 = (x4+w4/2,y4),(x4+w4,y4+h4/2),(x4+w4/2,y4+h4),(x4,y4+h4/2)
                is_red_ball, red_ball_center = True, (x4+w4/2,y4+h4/2)
                cv2.rectangle(frame, (x4, y4), (x4 + w4, y4 + h4), (0, 255, 0), 2)
                [cv2.circle(img, tuple(point), 5, (0, 0, 255), -1) for point in [a0, b0, c0, d0, red_ball_center]]
                red_Area = Area
                #----------------------------------------
                X_Size = int((255.0 / W_View_size) * w4)
                Y_Size = int((255.0 / H_View_size) * h4)
                X_255_point = int((255.0 / W_View_size) * X)
                Y_255_point = int((255.0 / H_View_size) * Y)
                #----------------------------------------
        else:
            x = 0
            y = 0
            X_255_point = 0
            Y_255_point = 0
            X_Size = 0
            Y_Size = 0
            Area = 0
            Angle = 0
            a0, b0, c0, d0, red_ball_center, red_Area= 0
            is_red_ball = False
        
        if len(cnts1) > 0:
            c1 = max(cnts1, key=cv2.contourArea)
            ((X, Y), radius) = cv2.minEnclosingCircle(c1)
            Area = cv2.contourArea(c1) / min_area[now_color]
            if Area > 255:
                Area = 255
            if Area > min_area[now_color]:
                x4, y4, w4, h4 = cv2.boundingRect(c1)
                a1, b1, c1, d1 = (x4+w4/2,y4),(x4+w4,y4+h4/2),(x4+w4/2,y4+h4),(x4,y4+h4/2)
                is_yellow_object, yello_object_center = True, (x4+w4/2,y4+h4/2)
                cv2.rectangle(frame, (x4, y4), (x4 + w4, y4 + h4), (0, 255, 0), 2)
                [cv2.circle(img, point, 5, (255, 0, 0), -1) for point in [a1, b1, c1, d1, yello_object_center]]
                yello_Area = Area
                #----------------------------------------
                X_Size = int((255.0 / W_View_size) * w4)
                Y_Size = int((255.0 / H_View_size) * h4)
                X_255_point = int((255.0 / W_View_size) * X)
                Y_255_point = int((255.0 / H_View_size) * Y)
                #----------------------------------------
        else:
            x = 0
            y = 0
            X_255_point = 0
            Y_255_point = 0
            X_Size = 0
            Y_Size = 0
            Area = 0
            Angle = 0
            a1, b1, c1, d1, yellow_ball_center, yellow_Area= 0
            is_yellow_object = False
        Frame_time = (clock() - old_time) * 1000.
        old_time = clock()
        
        #######################################################################
        #########################################################################
        #########################################################################
        #변수 선언
        
        if ACT == "TEESHOT":
            print("ACT: ", ACT, "Teeshot A") # Debug
            is_ball = is_red_ball
            ### False면, big UD LR 해라
            if not is_ball:
                if first_big_ud_angle == 0:   # 최초  big_ud_angle 실행 판단 
                    big_ud_angle = 100
                    first_big_ud_angle = 1
                if first_big_ud_angle and not is_big_UD and big_ud_angle: #while
                    is_object_in_frame, Distance.Head_ud_angle = big_UD_head(object, big_ud_angle) 
                    if is_object_in_frame == True:
                        first_big_ud_angle = 0
                        big_ud_angle = 100
                        is_big_UD = "Success"
                    elif is_object_in_frame == False:
                        big_ud_angle = Distance.Head_ud_angle
                        if Distance.Head_ud_angle == 64: 
                            first_big_ud_angle = 0
                            big_ud_angle = 100
                            is_big_UD =  "Except"
                        else: 
                            continue                        
                #if go_to == "big_lr" :
                
                if is_big_UD == "Except" :  # big UD 검출안됨 -> big LR 로 넘어감
                    print("is_big_UD: ", is_big_UD)
                    """
                    big_LR("ball")  # big은 알아서 고개 디폴트 함 
                
                is_small_LR = ball_small_LR("ball")
                
                if is_small_LR == "Except" :
                    motion.head("DEFAULT", 2) # small_LR 한 후 고개 디폴트
                    # big 알고리즘으로 넘어감
                    # is_big_LR = big_LR("ball") 하러 처음으로 올라감 
                    big_LR("ball") # 이거 한번만 실행하면 무조건 찾을 거라고 생각해서 while로 안 돌아감.
                else:
                    break   
            else:
                ball_small_LR("ball") # small lr 함으로써 중앙 맞춰짐  
                     
            """
            print("제발 여기까지만 오자 시팔")
                      
        #########################################################################
        #########################################################################
        #########################################################################
           
        ################## 카메라 실행 ################## 
        if View_select == 0: # Fast operation 
            #print(" " + str(W_View_size) + " x " + str(H_View_size) + " =  %.1f ms" % (Frame_time ))
            #temp = Read_RX
            pass
        elif View_select == 1: # Debug
            cv2.imshow('mini CTS5 - Video', frame )
            cv2.imshow('mini CTS5 - Mask', mask)

        key = 0xFF & cv2.waitKey(1)
        
        if key == 27:  # ESC  Key
            break
        elif key == ord(' '):  # spacebar Key
            if View_select == 0:
                View_select = 1
            else:
                View_select = 0
        elif key == ord('s') or key == ord('S'):  # s or S Key:  Setting valus Save
            hsv_setting_save()
            msg_one_view = 1

    # cleanup the camera and close any open windows
    receiving_exit = 0
    time.sleep(0.5)
    
    camera.release()
    cv2.destroyAllWindows()
