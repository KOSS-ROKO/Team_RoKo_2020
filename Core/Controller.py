# -*- coding: utf-8 -*-

import time
from Robo import Robo
from Vision.Ball_middle import Ball

class Act:
    
    TEESHOT = 1          # 1. 맨 처음 티샷  
    WALK_BALL = 2        # 2. 공까지 걸어가기 (걸음수)
    PUTTING_POS = 3      # 3. 퍼팅 위치에 서기
    PUTTING = 4          # 4. 퍼팅
    HOLEIN = 5            # 5. 홀인

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
        flag = 0

        if act == Act.TEESHOT:                 ##### 1. 시작 및 티샷
            print("ACT: ", act)  # Debug
            
            ################# 처음 티샷 모션 
            robo._motion.teeshot("")
            
            # turn body left, 몸을 왼쪽으로 90도 돌림. / 고개는 이미 정면을 바라보고 있음.(바꿀 필요 없단 뜻)
            robo._motion.body_left("")
            
            act = Act.WALK_BALL
        
        
        elif act == Act.WALK_BALL:             ##### 2. 공을 향해 걸어간다
            if flag == 0: # 맨 처음만 실행
                check_ball = robo._image_processor.detect_ball()
            
            if check_ball == True:
                flag = 1 # 공 검출 완료
                find_ball = Ball.middle_ball()
                
                
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
                # 고개 각도 크게 돌리기, Find ball과 다름
                flag = 0
                pass
            
        elif act == Act.PUTTING_POS:             ##### 3. 퍼팅 위치에 서기
            pass
        
        elif act == Act.PUTTING:             ##### 4. 퍼팅
            pass
        
        elif act == Act.HOLEIN:             ##### 5. 홀인
            pass
            
        
