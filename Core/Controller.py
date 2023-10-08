# -*- coding: utf-8 -*-

import time
from Vision.ImageProcessor import ImageProcessor
from Robo import Robo
from Motion.Motion import Motion


class Act:
    
    TEESHOT = 1          # 2. 맨 처음 티샷  
    WALK_BALL = 2        # 3. 공까지 걸어가기 (걸음수)
    PUTTING_POS = 3      # 4. 퍼팅 위치에 서기
    PUTTING = 4          # 5. 퍼팅
    OLEIN = 5            # 6. 홀인

class Controller:

    def __init__(self):
        pass
    
    robo = Robo()
    act  = Act.TEESHOT

    @classmethod
    def start(self):
        # 정해진 파워로 한번 퍼팅.
        act = self.act
        robo = self.robo

        if act == Act.TEESHOT:
            print("ACT: ", act)  # Debug
            state = robo._image_processor.detect_ball()

            if state:
                robo._motion.walk("FORWARD")
            
        
        