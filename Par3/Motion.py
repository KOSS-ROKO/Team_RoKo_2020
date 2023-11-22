# -*- coding: utf-8 -*-
# Motion code
import platform
import argparse
import cv2
import sys
import serial
import time
from threading import Thread, Lock


# -----------------------------------------------
class Motion:
    def __init__(self, sleep_time=0):
        self.serial_use = 1
        self.serial_port = None
        self.Read_RX = 0
        self.receiving_exit = 1
        self.threading_Time = 0.01
        self.sleep_time = sleep_time
        #self.lock = Lock()
        self.lock = False
        self.distance = 0
        BPS = 4800  # 4800,9600,14400, 19200,28800, 57600, 115200
        # ---------local Serial Port : ttyS0 --------
        # ---------USB Serial Port : ttyAMA0 --------
        self.serial_port = serial.Serial('/dev/ttyS0', BPS, timeout=0.01)
        self.serial_port.flush()  # serial cls
        self.serial_t = Thread(target=self.Receiving, args=(self.serial_port,))
        self.serial_t.daemon = True
        self.serial_t.start()
        time.sleep(0.1)

    # DELAY DECORATOR
    def sleep(self, func):
        def decorated():
            func()
            time.sleep(self.sleep_time)

        return decorated

    def TX_data_py2(self, one_byte):  # one_byte= 0~255
        self.lock = True
        self.serial_port.write(serial.to_bytes([one_byte]))  # python3
        time.sleep(0.1)
        '''
        try:
            self.lock.acquire()
            self.serial_port.write(serial.to_bytes([one_byte]))  # python3
        finally:
            self.lock.release()
            time.sleep(0.02)
        '''

    def RX_data(self):
        print('rxdata')
        time.sleep(0.02)
        if self.serial_port.inWaiting() > 0:
            result = self.serial_port.read(1)
            RX = ord(result)
            return RX
        else:
            return 0

    def Receiving(self, ser):
        self.receiving_exit = 1
        while True:
            time.sleep(self.threading_Time)
            # 수신받은 데이터의 수가 0보다 크면 데이터를 읽고 출력
            while ser.inWaiting() > 0:
                # Rx, 수신
                result = ser.read(1) # 시리얼 포트에서 한 바이트(문자)를 읽어와 result 변수에 저장
                RX = ord(result)
                if RX == 38:
                    self.lock = False
                # print("RX=" + str(RX))
                else:
                    self.distance = RX
                # -----  remocon 16 Code  Exit ------
                
            if self.receiving_exit == 0:
                break
        '''
        self.receiving_exit = 1
        while True:
            if self.receiving_exit == 0:
                break
            time.sleep(self.threading_Time)
            time.sleep(0.08)

            while ser.inWaiting() > 0:
                time.sleep(0.5)
                result = ser.read(1)
                RX = ord(result)
                # -----  remocon 16 Code  Exit ------
                if RX == 16:
                    self.receiving_exit = 0
                    break
                elif RX == 38:
                    try:
                        self.lock.release()
                    except:
                        continue
                elif RX != 200:
                    self.distance = RX
        '''

    ############################################################
    # 기본자세 (99)
    def basic(self):
        self.TX_data_py2(99)
        time.sleep(1.5)

    # 걷기 (101~120)
    def walk(self, dir, dist=0, loop=1):
        """ parameter :
        dir : {'JFORWARD', 'JBACKWARD', FORWARD, BACKWARD}
        """
        # Jforward = 전진종종걸음 Jbackward = 후진종종걸음
        # 2Jforward = 2센치 종종걸음
        dir_list = {'JFORWARD': 100, "JBACKWARD": 101, "FORWARD":102, "BACKWARD": 103, "FORWARD10": 104, "FORWARD12": 107, "FORWARD14": 108, "FORWARD15": 109,
                    '2JFORWARD': 105, "2JBACKWARD": 106}


        print("motion.py dist - 18or26: ", dist)
               
        ############
        if dir=="FORWARD" or "2JFORWARD":
            while dist > 0:            
                if dist >= 8:
                    print(dir, dist)
                    self.TX_data_py2(dir_list["FORWARD"])
                    time.sleep(3)
                    dist -= 8
                elif dist < 8 and dist >= 5:
                    print(dir, dist)
                    self.TX_data_py2(dir_list["JFORWARD"])
                    time.sleep(3)
                    dist -= 5
                elif 2 <= dist < 5 :  
                    print(dir, dist)
                    self.TX_data_py2(dir_list["2JFORWARD"])
                    time.sleep(3)
                    dist -= 2
                    continue
                elif 2 > dist:  
                    print("FORWARD too small to WALK further.", dist)
                    break
        elif dir=="BACKWARD" or "2JBACKWARD":
            while dist < 0:            
                if dist <= -8:
                    print("BACKWARD", dir, " by a degrees.", dist)
                    self.TX_data_py2(dir_list["BACKWARD"])
                    time.sleep(3)
                    dist += 8
                elif -8 < dist <= -5:
                    print("Rotating", dir, " by a degrees.", dist)
                    self.TX_data_py2(dir_list["JBACKWARD"])
                    time.sleep(3)
                    dist += 5
                elif -5 < dist <= -2:
                    print("Rotating", dir, " by a degrees.", dist)
                    self.TX_data_py2(dir_list["2JBACKWARD"])
                    time.sleep(3)
                    dist += 2
                elif dist > -2:  
                    print("Angle too small to rotate further.", dist)
                    break
        else:
            print("else walk")
            self.TX_data_py2(dir_list[dir])
            time.sleep(3)

                    

    # 머리 각도 (121~140)
    def head(self, dir, angle=0):
        """ parameter :
        dir : {DOWN, LEFT, RIGHT, UPDOWN_CENTER, LEFTRIGHT_CENTER}
        angle: {DOWN:{20,30,40,45,60,70,80,90,100,110},
        LEFT:{30,45,60,90},
        RIGHT:{30,45,60,90}
        }
        """
        dir_list = {
            'DOWN': { 3: 124, 6: 125, 9: 126, 30: 127, 45: 141 },
            'UP' : { 3: 129, 6: 130, 9: 131, 30: 132, 45: 142 },
            'LEFT': { 3: 134, 6: 135, 30: 136 },
            'RIGHT': { 3: 138, 6: 139, 30: 140 },
            'DEFAULT': { 1: 121, 2: 122, 63: 143 }
        }
        self.TX_data_py2(dir_list[dir][angle])
        time.sleep(0.2)

    # 돌기 (141~160)
    # 값 조절 필요
    def turn(self, dir, angle=0, loop=1, sleep=1, arm=False):
        """ parameter :
        dir : {LEFT, RIGHT}
        """
        dir_list = {
            "LEFT": {60: 160, 45: 159, 20: 158, 10: 157, 5: 156},
            "RIGHT": {60: 155, 45: 154, 20: 153, 10: 152, 5: 151}
        }

        while angle > 0:
            angles = list(dir_list[dir].keys())
            angles.sort(reverse=True)
            for a in angles:
                if angle >= a:
                    print("Rotating", dir, " by a degrees.", angle)
                    self.TX_data_py2(dir_list[dir][a])
                    time.sleep(sleep)
                    angle -= a
                    break
            if angle<5 and angle>2.5:
                print("Rotating", dir, " by a degrees.", angle)
                self.TX_data_py2(dir_list[dir][a])
                time.sleep(sleep)
                angle -= 5
            if angle<2.5:  
                print("Angle too small to rotate further.", angle)
                break


    # 옆으로 이동 (161~170)
    def walk_side(self, dir):
        """ parameter :
        dir : {LEFT, RIGHT}
        """
        # dir_list = {"LEFT": 119, "RIGHT": 118}
        dir_list = {"LEFT10": 113, "RIGHT10": 112,"LEFT20": 115, "RIGHT20": 114, "LEFT70": 117, "RIGHT70": 116}
        self.TX_data_py2(dir_list[dir])
        time.sleep(1)



    #퍼팅 위치에 서기 
    def pose(self,dir, TB=False):
        # dir = ["left", "right"]
        if TB:
            if dir=="RIGHT":
                self.TX_data_py2(111)
                time.sleep(7)
            elif dir=="LEFT":
                self.TX_data_py2(110)
                time.sleep(7)  
            else:  
                self.TX_data_py2(110)
                time.sleep(7) 
        else: # TB= True
            if dir=="RIGHT":
                self.TX_data_py2(148)
                time.sleep(7)
            elif dir=="LEFT":
                self.TX_data_py2(147)
                time.sleep(7)  
            else:  
                self.TX_data_py2(147)
                time.sleep(7)
        
    
    def putting(self, dir, power, sleep=1): 
        print("Motion putting")
        # power:1,2,3,4 // dir: LEFT/RIGHT
        dir_list = {
            "left": {1: 175, 2: 176, 3: 177, 4: 178, 5:179},
            "right": {1: 170, 2: 171, 3: 172, 4: 173, 5:174}
        }
        self.TX_data_py2(dir_list[dir][power])
        time.sleep(sleep)
    
    def ceremony(self):
        self.TX_data_py2(180)
        time.sleep(2)

    def Rarm(self, dir): #오른쪽 팔
        dir_list = {'DOWN':145 ,'RESET':146}

        self.TX_data_py2(dir_list[dir])
        time.sleep(2)

            

    ############################################################


if __name__ == '__main__':
    motion = Motion()
    motion.set_head("LEFTRIGHT_CENTER")