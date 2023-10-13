# -*- coding: utf-8 -*-

import time
from Robo import Robo
from Vision.Ball_middle import Ball
from head import Head

class Act:
    
    TEESHOT = 1          # 1. 맨 처음 티샷  
    WALK_BALL = 2        # 2. 공까지 걸어가기 (걸음수)
    PUTTING_POS = 3      # 3. 퍼팅 위치에 서기
    PUTTING = 4          # 4. 퍼팅
    HOLEIN = 5           # 5. 홀인

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
        first_detect_ball_flag = 0
        max_right_flag = 0 ##위치 수정 필요 
        is_object_in_frame = False
        object_vertical_middle = False



        if act == Act.TEESHOT:                 ##### 1. 시작 및 티샷
            print("ACT: ", act)  # Debug
            
            ################# 처음 티샷 모션 
            robo._motion.teeshot("")
            
            # turn body left, 몸을 왼쪽으로 90도 돌림. / 고개는 이미 정면을 바라보고 있음.(바꿀 필요 없단 뜻)
            robo._motion.body_left("")
            
            act = Act.WALK_BALL
        
        
        elif act == Act.WALK_BALL: 
            big_lr_angle = 0            ##### 2. 공을 향해 걸어간다
            max_right_flag = 0
            small_lr_angle = 0
            small_ud_angle = 0
            #big lr head
            while True:
                is_object_in_frame, big_lr_temp = Head.big_LR_head("ball", big_lr_angle)
                if is_object_in_frame == True:
                    break
                elif is_object_in_frame == False:
                    big_lr_angle = big_lr_temp
                    continue
                #if big_lr_angle == -90: #왼쪽 max까지 갔는데 공 못찾으면 
                    #Head.big_UD_head()
                    # 예외처리 : big up down 코드
            #고개 정면 코드 추가하기

            #small lr head
            while True:
                is_vertical_middle, small_lr_temp = Head.small_LR_head("ball", small_lr_angle)
                if is_vertical_middle == True:
                    break
                elif is_vertical_middle == False:
                    small_lr_angle = small_lr_temp
                    continue

            #small ud head
            while True:
                is_horizontal_middle, small_ud_temp = Head.small_LR_head("ball", small_ud_angle)
                if is_horizontal_middle == True: #최종 중앙 맞춰짐 
                    act = Act.PUTTING_POS 
                    break
                elif is_horizontal_middle == False:
                    small_ud_angle = small_ud_temp
                    continue

            """
            # if is_object_in_frame == False :
            #     is_object_in_frame = Head.big_LR_head("big-left/right")
            # elif is_object_in_frame == True : 
            #     object_vertical_middle = Head.small_LR_head("small-left/right")
            #     if object_vertical_middle == True:
            #         Head.small_UD_head("small-up/down")
            #     else : #left right로 공이 검출안될경우 상하
            #         Head.big_UD_head("big-up/down")

            
                    """
            
            """
            ### def big_head에서 화면상에 물체 검출 True 후에 몸까지 고개각도로 돌린 상태임
            is_object_in_frame = Head.big_head() #true 아님 false
            
            if Head.small_head("ball"):
                act = Act.PUTTING_POS
            
            
            if first_detect_ball_flag == 0: # 맨 처음만 실행
                check_ball = robo._image_processor.detect_ball()
                small_angle = 0
            else:
                big_angle = 0
                            
            if check_ball == True:
                # 공이 화면 안에 들어왔을 경우 big_angle 만큼 몸 돌리기
                if big_angle > 0:
                    robo._motion.body_right("")
                elif big_angle < 0:
                    robo._motion.body_left("")
                

                first_detect_ball_flag = 1 # 공 검출 완료
                find_ball = Ball.middle_ball()
                
                
                if find_ball == "stop":
                    # 공을 화면 중앙에 오도록 만드는 고개 각도 small_angle 만큼 몸 돌리기
                    if small_angle > 0:
                        robo._motion.body_right("")
                    elif small_angle < 0:
                        robo._motion.body_left("")
                        
                    act = Act.PUTTING_POS
                    
                elif find_ball == "go right":
                    robo._motion.head_right("") ################# 고개 오른쪽으로 돌리는 모션 / 3도 씩 움직이기
                    small_angle += 3                    
                elif find_ball == "go left":
                    robo._motion.head_left("") ################# 고개 왼쪽으로 돌리는 모션
                    small_angle -= 3
                    
                
                elif find_ball == "go far":
                    act = Act.WALK_BALL
                        
            else: # check_ball == False
                # 공이 화면에 안 보이는 경우
                # 패닝 틸팅? or 걷기?
                # 고개 각도 크게 돌리기, Find ball과 다름
                if max_right_flag == 0:
                    robo._motion.head_right("") ################# 3도보단 큰 각으로
                    big_angle += 10 # 10은 임의 값
                    if big_angle == max(): # <-max() 에러 안 나려고 적어 놓음, 바꾸삼 / 최대값이면 
                        max_right_flag = 1
                        big_angle = 0
                        # 고개 정면(default)로 돌려놓기                        
                elif max_right_flag == 1:
                    robo._motion.head_left("") ################# 3도보단 큰 각으로
                    big_angle -= 10 # 10은 임의 값
                    """

            # 거리 측정 후 걷기
            robo._motion.walk("FORWARD", 5, 0.1)
            # 걷는 횟수 = (d - 15) / 한발자국 걷는 센치(5cm)
            # 걷는 횟수를 loop인자로 넘겨주면 됨.
                
            
        elif act == Act.PUTTING_POS:             ##### 3. 퍼팅 위치에 서기
            
            #1. 홀컵 : ------------------------------------------------------------
            # 홀컵 중앙에 오도록 고개 돌리기 & 고개 각도 저장
            if first_detect_holecup_flag == 0: # 맨 처음만 실행
                check_holecup = robo._image_processor.detect_holecup()
                small_angle = 0
            else:
                big_angle = 0
                            
            if check_holecup == True:
                # 공이 화면 안에 들어왔을 경우 big_angle 만큼 몸 돌리기
                if big_angle > 0:
                    robo._motion.body_right("")
                elif big_angle < 0:
                    robo._motion.body_left("")
                

                first_detect_holecup_flag = 1 # 공 검출 완료
                find_holecup = Ball.middle_ball()##########################################333?
                
                
                if find_holecup == "stop":
                    # 공을 화면 중앙에 오도록 만드는 고개 각도 small_angle 만큼 몸 돌리기
                    if small_angle > 0:
                        robo._motion.body_right("")
                    elif small_angle < 0:
                        robo._motion.body_left("")
                        
                    act = Act.PUTTING_POS
                    
                elif find_holecup == "go right":
                    robo._motion.head_right("") ################# 고개 오른쪽으로 돌리는 모션 / 3도 씩 움직이기
                    small_angle += 3                    
                elif find_holecup == "go left":
                    robo._motion.head_left("") ################# 고개 왼쪽으로 돌리는 모션
                    small_angle -= 3
                
                elif find_holecup == "go far":
                    act = Act.WALK_BALL
                        
            else: # check_ball == False
                # 공이 화면에 안 보이는 경우
                # 패닝 틸팅? or 걷기?
                # 고개 각도 크게 돌리기, Find ball과 다름
                if max_right_flag == 0:
                    robo._motion.head_right("") ################# 3도보단 큰 각으로
                    big_angle += 10 # 10은 임의 값
                    if big_angle == max(): # <-max() 에러 안 나려고 적어 놓음, 바꾸삼 / 최대값이면 
                        max_right_flag = 1
                        big_angle = 0
                        # 고개 정면(default)로 돌려놓기                        
                elif max_right_flag == 1:
                    robo._motion.head_left("") ################# 3도보단 큰 각으로
                    big_angle -= 10 # 10은 임의 값
        # 홀컵 거리 측정 
            #만약 홀컵 거리가 15cm 이 하면 원프레임 호출
            
        # 2. 공 : -----------------------------------------------------------------
        # #공이 중앙에 오도록 고개 돌리기 & 고개 각도 저장
        # 공 거리 측정 
        
        # 공과 홀컵의 각도 계산후 걸음 이동
        
        
        elif act == Act.PUTTING:             ##### 4. 퍼팅
            ##################### 2.의 중간 맞추는 코드 가져옴
            ######## 홀컵 거리 재기 위해
            big_lr_angle = 0           
            max_right_flag = 0
            small_lr_angle = 0
            small_ud_angle = 0
            #big lr head
            while True:
                is_object_in_frame, big_lr_temp = Head.big_LR_head("holecup", big_lr_angle)
                if is_object_in_frame == True:
                    break
                elif is_object_in_frame == False:
                    big_lr_angle = big_lr_temp
                    continue
                #if big_lr_angle == -90: #왼쪽 max까지 갔는데 공 못찾으면 
                    #Head.big_UD_head()
                    # 예외처리 : big up down 코드
            #고개 정면 코드 추가하기

            #small lr head
            while True:
                is_vertical_middle, small_lr_temp = Head.small_LR_head("holecup", small_lr_angle)
                if is_vertical_middle == True:
                    break
                elif is_vertical_middle == False:
                    small_lr_angle = small_lr_temp
                    continue

            #small ud head
            while True:
                is_horizontal_middle, small_ud_temp = Head.small_LR_head("holecup", small_ud_angle)
                if is_horizontal_middle == True: #최종 중앙 맞춰짐 
                    #### 홀컵 까지의 거리 재기 
                    

                    break
                elif is_horizontal_middle == False:
                    small_ud_angle = small_ud_temp
                    continue
            ##########################################






        
        elif act == Act.HOLEIN:             ##### 5. 홀인
            oneframe = robo._image_processor.ball_hole_oneframe()
            
            if oneframe == True:
                check_holein = robo._image_processor.detect_hole_in()
                if check_holein == True:
                    # 세레모니
                    robo._motion.ceremony("")
                else:
                    # 몰라. 3번을 더 간단히?
                    pass

            else:   
                # 퍼팅준비로 돌아감
                act = Act.PUTTING_POS
            
            
        
