# -*- coding: utf-8 -*-

import time
from Vision.ImageProcessor import ImageProcessor
from Robo import Robo
from Motion.Motion import Motion
from Vision.Ball_middle import Ball


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

        if act == Act.TEESHOT:                  # 
            print("ACT: ", act)  # Debug
            
            ################# 처음 티샷 모션 
            robo._motion.teeshot("")
            
            act = Act.WALK_BALL
            
            #state = robo._image_processor.detect_ball()
        
        elif act == Act.WALK_BALL:               #
            check_ball = robo._image_processor.detect_ball()
            
            if check_ball == True:
                find_ball = Ball.middle_ball()
                
                while find_ball != "stop":
                    if find_ball == "stop":
                        act = Act.PUTTING_POS
                    elif find_ball == "go right":
                        robo._motion.head_right("") ################# 고개 오른쪽으로 돌리는 모션
                        
                        
                        
                    elif find_ball == "go left":
                        robo._motion.head_left("") ################# 고개 왼쪽으로 돌리는 모션
                    
                    elif find_ball == "go far":
                        act = Act.WALK_BALL
                        
            else:
                # 공이 화면에 안 보이는 경우
                # 패닝 틸팅? or 걷기?
                pass
        
