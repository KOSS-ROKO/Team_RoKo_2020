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
        self.lock = Lock()
        #self.lock = False
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

    def TX_data(self, one_byte):
        self.serial_port.write(serial.to_bytes([one_byte]))  # python3
        time.sleep(0.02)

        # try:
        #     self.lock.acquire()
        #     self.serial_port.write(serial.to_bytes([one_byte]))  # python3
        # finally:
        #     self.lock.release()
        #     time.sleep(0.02)


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


    ############################################################
    # 기본자세 (99)
    def basic(self):
        self.TX_data(99)
        time.sleep(1.5)

    # 걷기 (101~120)
    def walk(self, dir, dist=0, loop=1):
        """ parameter :
        dir : {'JFORWARD', 'JBACKWARD', FORWARD, BACKWARD}
        """
        # Jforward = 전진종종걸음 Jbackward = 후진종종걸음
        # 2Jforward = 2센치 종종걸음
        dir_list = {'JFORWARD': 100, "JBACKWARD": 101, "FORWARD":102, "BACKWARD": 103, 
        "FORWARD10": 104, "FORWARD12": 107, "FORWARD13":149, "FORWARD14": 108, "FORWARD15": 109,
                    '2JFORWARD': 105, "2JBACKWARD": 106, "FORWARD2": 118, "FORWARD3": 119, "FORWARD5":165 ,"FORWARD6": 123} 



        print("Motion.py walk funct")
        
        if (dir == "FORWARD") or (dir == "JFORWARD") or (dir == "FORWARD3") or (dir == "FORWARD2"): # forward6 일단은 그리디에서 뺐는데 나중에 시간 부족할 거 같으면 다시 넣기
            if dist == 0 :  
                print(dir)
                self.TX_data(dir_list[dir])
                time.sleep(6)
            while dist > 0:    
                if dist >= 40:
                    self.TX_data(dir_list["FORWARD3"])
                    time.sleep(12)
                    dist -= 40
                elif dist >= 24:
                    self.TX_data(dir_list["FORWARD3"])
                    time.sleep(8)
                    dist -= 24
                elif dist >= 16:
                    self.TX_data(dir_list["FORWARD2"])
                    time.sleep(8)
                    dist -= 16
                elif dist >= 8:
                    self.TX_data(dir_list["FORWARD"])
                    time.sleep(4)
                    dist -= 8
                elif 3 <= dist < 8:
                    self.TX_data(dir_list["JFORWARD"])
                    time.sleep(4)
                    dist -= 4
                elif 3 > dist:  
                    print("FORWARD too small to WALK further.", dist)
                    break
        elif (dir == "BACKWARD") or (dir == "JBACKWARD"):
            if dist == 0 :  
                print(dir)
                self.TX_data(dir_list[dir])
                time.sleep(6)
            while dist < 0:            
                if dist <= -8:
                    print("BACKWARD", dir, " by a degrees.", dist)
                    self.TX_data(dir_list["BACKWARD"])
                    time.sleep(6)
                    dist += 8
                elif -8 < dist <= -3:
                    print("Rotating", dir, " by a degrees.", dist)
                    self.TX_data(dir_list["JBACKWARD"])
                    time.sleep(4)
                    dist += 4
                elif dist > -3:  
                    print("Angle too small to rotate further.", dist)
                    break
        elif dir == "2JFORWARD":
            self.TX_data(dir_list["2JFORWARD"])
            time.sleep(2)
            dist -= 1
        elif dir == "2JBACKWARD":
            print("Rotating", dir, " by a degrees.", dist)
            self.TX_data(dir_list["2JBACKWARD"])
            time.sleep(2)
            dist += 2
        elif dir == "FORWARD6":
            self.TX_data(dir_list["FORWARD6"])
            time.sleep(7)
            dist -= 48
        else:
            print("else walk")
            self.TX_data(dir_list[dir])
            time.sleep(3)
            
            

    def arms_off(self):
        self.TX_data(181)    
        time.sleep(1)         

    # 머리 각도 (121~140)
    def head(self, dir, angle=0):
        dir_list = {
            'DOWN': { 3: 124, 6: 125, 9: 126, 30: 127, 45: 141, 60:150 },
            'UP' : { 3: 129, 6: 130, 9: 131, 30: 132, 45: 142 },
            'LEFT': { 3: 134, 6: 135, 30: 136, 90:164 },
            'RIGHT': { 3: 138, 6: 139, 30: 140, 90:144 },
            'DEFAULT': { 0:120, 1: 121, 2: 122, 63: 143 }
        }
        self.TX_data(dir_list[dir][angle])
        time.sleep(0.2)

    # 돌기 (141~160)
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
                    self.TX_data(dir_list[dir][a])
                    time.sleep(sleep)
                    angle -= a
                    break
            if angle<5 and angle>2.5:
                print("Rotating", dir, " by a degrees.", angle)
                self.TX_data(dir_list[dir][a])
                time.sleep(sleep)
                angle -= 5
            if angle<2.5:  
                print("Angle too small to rotate further.", angle)
                break


    # 옆으로 이동 (161~170)
    def walk_side(self, dir):
        dir_list = {"LEFT10": 113, "RIGHT10": 112,"LEFT20": 115, "RIGHT20": 114, "LEFT70": 117, "RIGHT70": 116,
        "RIGHT20cm": 163,"LEFT120cm": 128, "RIGHT120cm": 137}

        self.TX_data(dir_list[dir])
        if dir != "RIGHT20cm":  time.sleep(1)
        else: time.sleep(7)




    #퍼팅 위치에 서기 
    def pose(self, dir, TB=False):
        if not TB:
            if dir=="RIGHT":
                self.TX_data(111)
                time.sleep(9.5)
            elif dir=="LEFT":
                self.TX_data(110)
                time.sleep(9.5)   
            else:  
                self.TX_data(110)
                time.sleep(9.5) 
        else: # TB= True
            if dir=="RIGHT":
                self.TX_data(148)
                time.sleep(9.5)
            elif dir=="LEFT":
                self.TX_data(147)
                time.sleep(9.5)  
            else:  
                self.TX_data(147)
                time.sleep(9.5)
        
    
    def putting(self, dir, power, sleep=1): 
        print("Motion putting")
        # power:1,2,3,4 // dir: LEFT/RIGHT
        dir_list = {
            "LEFT": {1: 175, 2: 176, 3: 177, 4: 178, 5:179},
            "RIGHT": {1: 170, 2: 171, 3: 172, 4: 173, 5:174},
            "PAR4": { 1:161, 2:162 }
        }
        self.TX_data(dir_list[dir][power])
        time.sleep(sleep)
    
    def ceremony(self):
        self.TX_data(180)
        time.sleep(2)

    def Rarm(self, dir): #오른쪽 팔
        dir_list = {'DOWN':145 ,'RESET':146}

        self.TX_data(dir_list[dir])
        time.sleep(2)

    def holecup_turn(self, dir, angle):
        dir_list = {'LEFT':{5:166, 10:167, 20 : 182, 45:184}, 'RIGHT':{5:168, 10:169, 20:183, 45:185}}
    
        self.TX_data(dir_list[dir][angle])
        time.sleep(1)

    ############################################################


if __name__ == '__main__':
    motion = Motion()
    motion.head("DEFAULT",1)
    time.sleep(1)
    motion.head("DEFAULT",2)
    time.sleep(1)