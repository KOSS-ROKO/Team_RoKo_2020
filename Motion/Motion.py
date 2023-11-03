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
        try:
            self.lock.acquire()
            self.serial_port.write(serial.to_bytes([one_byte]))  # python3
        finally:
            self.lock.release()
            time.sleep(0.02)

    def RX_data(self):
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
                elif RX == 200:
                    try:
                        self.lock.release()
                    except:
                        continue
                elif RX != 200:
                    self.distance = RX

    ############################################################
    # 기본자세 (100)
    def basic(self):
        self.TX_data_py2(100)

    # 걷기 (101~120)
    def walk(self, dir, loop=1, sleep=0.1, short=False):
        """ parameter :
        dir : {FORWARD, BACKWARD}
        """
        dir_list = {'FORWARD': 101, "BACKWARD": 111}
        if short:
            dir_list[dir] += 1

        for _ in range(loop):
            self.TX_data_py2(dir_list[dir])
            time.sleep(sleep)

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
            'DOWN': {
                3: 124, 6: 125, 9: 126, 30: 127
            },
            'UP' : {
                3: 129, 6: 130, 9: 131, 30: 132 # 포트번호 수정 
            },
            'LEFT': {
                3: 134, 6: 135, 30: 136,
            },
            'RIGHT': {
                3: 138, 6: 139, 30: 140
            },
            'DEFAULT':{
                1: 121, 2: 122 #121:상하, 122:좌우
            }
        }

        self.TX_data_py2(dir_list[dir][angle])
        time.sleep(0.3)

    # 돌기 (141~160)
    # 값 조절 필요
    def turn(self, dir, angle, loop=1, sleep=0.5, arm=False):
        """ parameter :
        dir : {LEFT, RIGHT}
        """
        dir_list = {
            "RIGHT": {
                5: 156, 10: 157, 20: 158, 45: 159, 60:160
            },
            "LEFT": {
                5: 151, 10: 152, 20: 153, 45: 154, 60:155
            }
        }

        for _ in range(loop):
            self.TX_data_py2(dir_list[dir][angle])
            time.sleep(sleep)


    # 옆으로 이동 (161~170)
    def walk_side(self, dir):
        """ parameter :
        dir : {LEFT, RIGHT}
        """
        dir_list = {"LEFT": 161, "RIGHT": 169}
        self.TX_data_py2(dir_list[dir])



    #퍼팅 위치에 서기 
    def pose(dir):
        #pose_list = {'A': 207, 'B': 208, 'C': 209, 'D': 210}
        if dir=="left":
            pass
        else:
            pass
        
    
    def putting(self, dir, power, sleep=1): 
        #power:1,2,3,4 // dir: LEFT/RIGHT
        dir_list = {
            "LEFT": {
                1: 175, 2: 176, 3: 177, 4: 178, 5:179
            },
            "RIGHT": {
                1: 170, 2: 171, 3: 172, 4: 173, 5:174
            }
        }
        self.TX_data_py2(dir_list[dir][power])

        time.sleep(sleep)
    
    
    def ceremony():
        pass

    
    
            

    ############################################################


if __name__ == '__main__':
    motion = Motion()
    motion.set_head("LEFTRIGHT_CENTER")
