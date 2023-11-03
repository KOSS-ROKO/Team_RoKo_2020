# -*- coding: utf-8 -*-

import time
from Robo import Robo
from head import Head
from Vision.Distance import Distance
from Motion.Motion import Motion
import variable

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
     ## 거리 측정
    def distance(object):
        f = 450
        while True:
            is_horizontal_middle, small_ud_temp = Head.small_LR_head(object, small_ud_angle)
            if is_horizontal_middle == True: #최종 중앙 맞춰짐 
                if object == "holecup":
                    #### 홀컵 까지의 대략적인 거리 재기 
                    fake_dist = Distance.holecup_dist(f)
                    break
                elif object == "ball":
                    #### 공 까지의 대략적인 거리 재기
                    fake_dist = Distance.ball_dist(f)
                    break

            elif is_horizontal_middle == False:
                small_ud_angle = small_ud_temp
                continue
 
        # 홀컵 거리 인식에서 f값 결정
        # 가까운지 먼지
        if fake_dist >= 50:
            f = 450
        else : 
            f = 270
        # 홀컵 거리
        if object == "holecup":
            holecup_dist = Distance.holecup_dist(f)
            return holecup_dist
        else : # object == "ball"
            ball_dist = Distance.ball_dist(f)
            return ball_dist
    

    def start(self):
        # 정해진 파워로 한번 퍼팅.
        act = self.act
        robo = self.robo
        first_detect_ball_flag = 0
        max_right_flag = 0 ##위치 수정 필요 
        is_object_in_frame = False
        object_vertical_middle = False



        if act == Act.TEESHOT:                 ##### 1. 시작 및 티샷 #################
            print("ACT: ", act)  # Debug
            
            ######## 처음 티샷하기위해 #########
            
            ######## act == Act.WALK_BALL에 Big UD 추가 ########
            big_ud_angle = 100                   # 2. 공을 향해 걸어간다
            big_lr_angle = 100            
            small_lr_angle = 0
            small_ud_angle = 0
            go_to = "small"

            ### big UD & LR 할까말까 결정 T / F
            is_ball = robo._image_processor.detect_ball()

            ### False면, big UD LR 해라
            if is_ball == False:

                # big UD head
                while True:
                    is_object_in_frame, variable.Head_ud_angle = Head.big_UD_head("ball", big_ud_angle)
                    if is_object_in_frame == True:
                        break
                    elif is_object_in_frame == False:
                        big_ud_angle = variable.Head_ud_angle
            
                        continue
                    if big_ud_temp == 10:  # 한 사이클이 다 끝남
                        variable.Head_ud_angle = Head_UD_Middle_Value_Measures # 고개값을 다시 정면100으로 
                        robo._motion.head("DEFAULT",1) # 고개 정면(default)로 돌려놓기 
                        go_to = "big_lr"  # LR로 갈지 구분

                if go_to == "big_lr" :
                    # big LR head
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

            ### True이거나 Big을 끝냈으면 small로 넘어가라  
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
                is_horizontal_middle, variable.Head_ud_angle = Head.small_LR_head("ball", small_ud_angle)
                if is_horizontal_middle == True: #최종 중앙 맞춰짐 
                    act = Act.PUTTING_POS 
                    break
                elif is_horizontal_middle == False:
                    small_ud_angle = variable.Head_ud_angle
                    continue


            # 거리 측정 후 걷기
            robo._motion.walk("FORWARD", 5, 0.1)
            # 걷는 횟수 = (d - 15) / 한발자국 걷는 센치(5cm)
            # 걷는 횟수를 loop인자로 넘겨주면 됨.

            ######### 퍼팅 위치에 서고 ########
            ###### act == Act.PUTTING_POS
            ###### 원래라면 퍼팅 포즈로 가서 << 원프레임, 스트레이트, 거리 재기 >> 해야하는데
            ######------------------> 이거 지금 테스트 용으로 바로 퍼팅함
            ######### 퍼팅한다 ########
            robo._motion.putting("LEFT", 4)
            

            # 이 바로 아래모션 좌퍼팅기준으로 썼네..
            # turn body left, 몸을 왼쪽으로 90도 돌림. / 고개는 이미 정면을 바라보고 있음.(바꿀 필요 없단 뜻)
            robo._motion.turn("LEFT", 60)   # <--고쳐야함. 몸 90도 돌려야하는데 지금 90없어서 60으로함 
            
            act = Act.WALK_BALL
        
        
        elif act == Act.WALK_BALL: 
            big_lr_angle = 0            ##### 2. 공을 향해 걸어간다 #################
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

            # length = 거리 
            # 인자 값으로 서보모터 값 들어가야함 (원래 값 + 변한 값)
            length = variable.Length_ServoAngle_dict.get(variable.Head_ud_angle +  small_ud_angle)
            #length = variable.Length_ServoAngle_dict.get(variable.Head_ud_angle +  small_ud_angle)
            
            # 걷는 횟수 = (d - 15) / 한발자국 걷는 센치(5cm)
            # 걷는 횟수를 loop인자로 넘겨주면 됨.
            walk_loop = (length -15) / 5

            # 거리 측정 후 걷기
            robo._motion.walk("FORWARD", walk_loop, 0.1)
            
                
            
        elif act == Act.PUTTING_POS:             ##### 3. 퍼팅 위치에 서기 #################
            ###### 홀컵 중앙 맞추기 #######################
            big_lr_angle = 0           
            small_lr_angle = 0
            small_ud_angle = 0
            
            #big_ud_head
            is_ball_hole_oneframe = robo._image_processor.ball_hole_oneframe()
    
            if is_ball_hole_oneframe == False:
                # big ud head를 수행해라 아래 코드 고쳐야함
                while True:
                    ## 원래 공, 홀컵 둘다 검출해야함
                    # 근데 공 앞이니까 홀컵만 해도 원프레임이지않을까????
                    is_object_one_frame, big_ud_temp = Head.big_UD_head("holecup", big_ud_angle)
                    if is_object_one_frame == True:
                        break
                    elif is_object_one_frame == False:
                        big_ud_angle = big_ud_temp
                        continue
                    #if big_lr_angle == -90: #왼쪽 max까지 갔는데 공 못찾으면 
                        #Head.big_UD_head()
                        # 예외처리 : big up down 코드
                #고개 정면 코드 추가하기
            elif is_ball_hole_oneframe == True:
                while True:
                    # 공 홀컵 일직선 맞추기
                    check_straight = Head.straight()
                    # check_straight = robo._image_processor.straight()
                    if check_straight ==True:
                        # 거리 알고리즘 (홀 컵 거리재기)
                                     
                        # 인자 값으로 서보모터 값 들어가야함 (원래 값 + 변한 값)
                        length = variable.Length_ServoAngle_dict.get(variable.Head_ud_angle +  small_ud_angle)
                        
                        # 걷는 횟수 = (d - 15) / 한발자국 걷는 센치(5cm)
                        # 걷는 횟수를 loop인자로 넘겨주면 됨.
                        walk_loop = (length -15) / 5

                        # 거리 측정 후 걷기
                        robo._motion.walk("FORWARD", walk_loop, 0.1)
                        break
                    else :
                        continue
                    
            ### field 블랙 판별 => 좌우 퍼팅 결정   
            field = robo._image_processor.field() #return left, right
            #몸 퍼팅 위치에 서기
            if field == "left" :
                robo._motion.pose("left")
            elif field == "right" :
                robo._motion.pose("right")
            ### 거리 알고리즘
            # 홀컵 middle 맞추기
            # 홀컵 거리 재기
               
            # 공 middle 맞추기
            # 공 거리 재기 => 15cm 거리 미세조정
        
            
        
        
        elif act == Act.PUTTING:             ##### 4. 퍼팅 #################
            ##################### 2.의 중간 맞추는 코드 가져옴
            ### 거리 알고리즘
            # 홀컵 middle 맞추기
            # 홀컵 거리 재기
            ######## 홀컵 거리 재기 위해
            big_lr_angle = 0           
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

            # small ud head 
            #        +
            ##### distance
            holecup_dist = Controller.distance("holecup")
            
            
            
            ###### 홀 컵 거리가 10이하이면 홀인 알고리즘 / 아니면 공 거리 재기
            if 0 < holecup_dist <= 10:
                act = Act.HOLEIN
            else:   
                ############################ 공 거리 재기 시작 ########################
                big_lr_angle = 0           
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

                #small ud head + distance
                
                while True:
                    ball_dist = Controller.distance("ball")
                    
                    if 13 <= ball_dist <= 17: # 거리 값 조정 필요!
                        break
                    elif ball_dist < 13:
                        robo._motion.walk("BACKWARD")
                    elif ball_dist > 17:
                        robo._motion.walk("FORWARD")

                ### 진짜 퍼팅
                ###### 홀 컵 거리에 따라 퍼팅 강도 조절하기
                if 0 < holecup_dist <= 10:
                    # Motion.putting() # 나중에 robo의 motion변수를 없애고 아래 코드가 아닌 이 코드로 변경할 예정
                    robo._motion.putting(field, 1) # def putting 짜야함 + 방향과 강도를 넘겨줌
                elif 10 < holecup_dist <= 20:
                    # Motion.putting() 
                    robo._motion.putting(field, 2) 

            

        
        elif act == Act.HOLEIN:             ##### 5. 홀인 #################
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
            
            
            
            
           