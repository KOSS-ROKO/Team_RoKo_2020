# -*- coding: utf-8 -*-
import time
from Robo import Robo
from Head import Head
from Motion import Motion
import Distance


class Act:
    TEESHOT = 1          # 1. 맨 처음 티샷  
    WALK_BALL = 2        # 2. 공까지 걸어가기 (걸음수)
    PUTTING_POS = 3      # 3. 퍼팅 위치에 서기
    PUTTING = 4          # 4. 퍼팅
    HOLEIN = 5           # 5. 홀인

class Controller:

    def __init__(self):
        #act = Act.TEESHOT
        pass
    
    act  = Act.TEESHOT
    robo = Robo()


    @classmethod  
    def start(self):

        act = self.act
        robo = self.robo
        
        head = Head()
        motion = Motion()
        
        
        #=======================================================#
        #                        Head def                       #         
        #=======================================================#
        def big_UD(object="ball"):
            big_ud_angle = 100
            # big UD head
            while True:
                is_object_in_frame, Distance.Head_ud_angle = head.big_UD_head(object, big_ud_angle)
                if is_object_in_frame == True:
                    return "Success"
                elif is_object_in_frame == False:
                    big_ud_angle = Distance.Head_ud_angle
                
                    if Distance.Head_ud_angle == 55: # Distance.Head_UD_Middle_Value_Measures - 100 + 10 + 45:  # big ud 한 사이클이 끝남. / 9는 바뀔 수 있는 값
                        Distance.Head_ud_angle = Distance.Head_UD_Middle_Value_Measures # 고개값을 다시 정면100으로 
                        #go_to = "big_lr"  # LR로 갈지 구분
                        return "Except"
                    else: 
                        continue
                        
                        
        def big_LR(object="ball"):
            big_lr_angle = 100
            max_right_flag = 0
            print("THis is ", object)
            # big LR head
            while True:
                is_object_in_frame, big_lr_temp, max_right_flag = head.big_LR_head(object, big_lr_angle, max_right_flag)
                if is_object_in_frame == True:
                    break
                elif is_object_in_frame == False:
                    big_lr_angle = big_lr_temp
                    print("big_lr_angle : ", big_lr_angle)
                    continue
                #if big_lr_angle == -90: #왼쪽 max까지 갔는데 공 못찾으면 
                    #head.big_UD_head()
                    # 예외처리 : big up down 코드
            #고개 정면 코드 추가하기

        def small_LR(object="ball"):
            Distance.small_lr_angle = 100
            while True:
                print("---------start small lr head")
                is_vertical_middle, small_lr_temp = head.small_LR_head(object, Distance.small_lr_angle)
                if is_vertical_middle == True:
                    return "Success" #break
    
                elif is_vertical_middle == False:
                    Distance.small_lr_angle = small_lr_temp
                    continue
                else : # is_vertical_middle == Except_
                    return "Except"
                         

        def UD_for_dist(object="ball"): # small ud head 변형
            small_ud_angle = Distance.Head_UD_Middle_Value_Measures
            # 거리를 위한 고개 각도 내리기 
            while True:
                print("---------start ud for dist")
                is_horizontal_middle, small_ud_temp = head.head_for_dist(object, small_ud_angle)
                if is_horizontal_middle == True: #최종 중앙 맞춰짐 
                    #act = Act.PUTTING_POS 
                    #variable.Head_ud_angle = 
                    Distance.Head_ud_angle = small_ud_temp
                    print(Distance.Head_ud_angle)
                    break
                elif is_horizontal_middle == False:
                    small_ud_angle = small_ud_temp
                    Distance.Head_ud_angle = small_ud_temp
                    continue

        def holecup_UD_for_dist(): # small ud head 변형
            small_ud_angle = 10
            
            # 거리를 위한 고개 각도 올리기 
            while True:
                print("---------start HOlECUP ud for dist")
                is_horizontal_middle, small_ud_temp = head.head_for_dist("holecup", small_ud_angle)
                if is_horizontal_middle == True: #최종 중앙 맞춰짐 
                    #act = Act.PUTTING_POS 
                    #variable.Head_ud_angle = 
                    Distance.Head_ud_angle = small_ud_temp
                    print("holecup ud angle : ",Distance.Head_ud_angle)
                    break
                elif is_horizontal_middle == False:
                    if small_ud_angle > small_ud_temp : # 홀컵중점 바껴서 갇히는 현상 해결
                        Distance.Head_ud_angle = small_ud_temp  #(상관없) 더 최근 고개값 = 더 먼 거리값
                        break
                    small_ud_angle = small_ud_temp
                    Distance.Head_ud_angle = small_ud_temp

                    continue
            
            
        def is_point_inside_rectangle(point, rectangle):
            x, y = point
            x1, y1, x2, y2, x3, y3, x4, y4 = rectangle
            return x1 <= x <= x2 and y1 <= y <= y4

        # 좌표가 사각형 밖에 있다면 기준 좌표로부터 얼마나 떨어져 있는지 계산하는 함수 정의
        def calculate_distance_from_reference(center, reference):
            cx, cy = center
            rx, ry = reference
            dx = cx - rx
            dy = cy - ry
            return dx, dy    
        #=======================================================#
        #                      1. Teeshot                       #         
        #=======================================================#
        
        if act == Act.TEESHOT:                 ##### 1. 시작 및 티샷 #################
            print("ACT: ", act) # Debug

            is_ball = robo._image_processor.detect_ball()

            ### False면, big UD LR 해라
            if is_ball == False:                
                while True:
                    # big UD head
                    is_big_UD = big_UD("ball")

                    #if go_to == "big_lr" :
                    if is_big_UD == "Except" :  # big UD 검출안됨 -> big LR 로 넘어감
                        big_LR("ball")  # big은 알아서 고개 디폴트 함 
                    
                    is_small_LR = small_LR("ball")
                    
                    if is_small_LR == "Except" :
                        motion.head("DEFAULT", 2) # small_LR 한 후 고개 디폴트
                        # big 알고리즘으로 넘어감
                        # is_big_LR = big_LR("ball") 하러 처음으로 올라감 
                        big_LR("ball") # 이거 한번만 실행하면 무조건 찾을 거라고 생각해서 while로 안 돌아감.
                    else:
                        break
                    
            else:
                small_LR("ball") # small lr 함으로써 중앙 맞춰짐

            # ud_for_dist 하기전에 고개 세팅
            motion.head("DEFAULT", 2) # 고개 디폴트
            Distance.Head_ud_angle = Distance.Head_UD_Middle_Value_Measures
            motion.head("DEFAULT", 1) # 고개 디폴트
            
            UD_for_dist("ball")
            motion.head("DEFAULT", 1) # ud for dist 이후 고개 상하 디폴트
            time.sleep(2)
            

            # length = 거리 
            ball_dist = Distance.Length_ServoAngle_dict.get(Distance.Head_ud_angle)
            print(Distance.Length_ServoAngle_dict)
            print("==========================================")
            print("ball dist: ", ball_dist , "===========","head angle: ", Distance.Head_ud_angle)
            print("==========================================")



            if ball_dist > 18:
                motion.walk("FORWARD", ball_dist - 18)
                    
            elif ball_dist == 18:
                print("correct!")
            else :      # 최소 거리 18보다 더 가까이 있을 경우: 뒷걸음질
                motion.walk("BACKWARD", ball_dist - 18)

            # PUTTING
            time.sleep(3)
            motion.putting("left", 3, 2)
            print("putting")
            time.sleep(5)


            # turn body left, 몸을 왼쪽으로 90도 돌림.
            motion.turn("LEFT", 60)
            time.sleep(7)
            motion.turn("LEFT", 60)
            time.sleep(2)
            print("turn LEFT")

            self.act = Act.WALK_BALL
            
            motion.walk("FORWARD10", 1)
            time.sleep(15)
            
            # return True
        
        #=======================================================#
        #                        2. Walk                        #         
        #=======================================================#
        
        elif act == Act.WALK_BALL: 
        ##### 2. 공을 향해 걸어간다 #################

            print("^^^^222222")
            print("^^^^222222")
            print("^^^^222222")
            print("^^^^222222")
            
            #motion.head("DEFAULT", 1)
            #motion.head("DOWN", 45) # 고개 45도로 내리고 공 detect 시작 !
            #time.sleep(5)
        
            
            is_ball = robo._image_processor.detect_ball()

            ### False면, big UD LR 해라
            if is_ball == False:                
                while True:
                    # big UD head
                    is_big_UD = big_UD("ball")
                    print("controller === big ud ")

                    #if go_to == "big_lr" :
                    if is_big_UD == "Except" :  # big UD 검출안됨 -> big LR 로 넘어감
                        motion.head("UP", 9) # after Teeshot 고개 60
                        motion.head("UP", 6)
                        big_LR("ball")  # big은 알아서 고개 디폴트 함 
                    
                    is_small_LR = small_LR("ball")
                    
                    if is_small_LR == "Except" :
                        motion.head("DEFAULT", 2) # small_LR 한 후 고개 디폴트
                        big_LR("ball") # 이거 한번만 실행하면 무조건 찾을 거라고 생각해서 while로 안 돌아감.
                    else:
                        break
            else:
                small_LR("ball") # small lr 함으로써 중앙 맞춰짐
            
            # ud_for_dist 하기전에 고개 세팅
            motion.head("DEFAULT", 2) # 고개 디폴트
            Distance.Head_ud_angle = Distance.Head_UD_Middle_Value_Measures
            motion.head("DEFAULT", 1) # 고개 디폴트
            time.sleep(1)
            
            print("ball detected")
            UD_for_dist("ball")
            motion.head("DEFAULT", 1) # ud for dist 이후 고개 상하 디폴트
            time.sleep(2)

            # length = 거리 
            ball_dist = Distance.Length_ServoAngle_dict.get(Distance.Head_ud_angle)
            print("ball distance :", ball_dist)
            
        
            # 무지성 10번 걸은 후, 남은 거리 측정 후 걷기
            if ball_dist > 26:  # 18+8 (화면에 여유있게 들어오도록)
                motion.walk("FORWARD", ball_dist - 26)
                    
            elif ball_dist == 26:
                print("correct!")
            else :      # 최소 거리 18보다 더 가까이 있을 경우: 뒷걸음질
                motion.walk("BACKWARD", ball_dist - 26)            
            
            
            self.act = Act.PUTTING_POS
            
            #return True
            
        #=======================================================#
        #                     3. Putting Pos                    #         
        #=======================================================#
            
        elif act == Act.PUTTING_POS:             ##### 3. 퍼팅 위치에 서기 #################
            ###### 홀컵 중앙 맞추기 #######################
            
            print("^^^^333333")
            print("^^^^333333")
            print("^^^^333333")
            print("^^^^333333")

            motion.head("DOWN", 45) # 고개 45도로 내리고 공 detect 시작 !
            time.sleep(1)
            Distance.Head_UD_Angle = 55
            
            
            is_holecup_in_frame = robo._image_processor.detect_holecup()
            
            motion.head("DEFAULT", 1) # 고개 상하 디폴트
            
            if is_holecup_in_frame == False:    
                print("holecup NONONONONONO")
                # big UD head
                while True:
                    is_big_UD = big_UD("holecup")
                    if is_big_UD == "Except" :  # big UD 검출안됨 -> big LR 로 넘어감
                        print("holecup big UD except")
                        big_LR("holecup")
                        
                    is_small_LR = small_LR("holecup")
                    print("small lr finished")

                    if is_small_LR == "Except" :
                        motion.head("DEFAULT", 2) # small_LR 한 후 고개 디폴트
                        
                        big_LR("holecup") # 이거 한번만 실행하면 무조건 찾을 거라고 생각해서 while로 안 돌아감.
                    else:
                        break

               
                #====== holecup 고개 방향만큼 꽃게 걸음 ======#
                side_walk = int(abs(100-Distance.Head_lr_angle)//10) # 식은 시행착오거치면서 변경예정

                print("**꽃게 걸음 시작**")
                # side walk 방향 설정 
                if  Distance.small_lr_angle < 100:
                    # 고개가 왼쪽L이면 오른쪽R으로 side walk해라
                    print("꽃게 걸음 오른쪽")
                    side_lr = "RIGHT"
                elif Distance.small_lr_angle > 100 : 
                    # 고개가 오른쪽R이면 왼쪽L으로 side walk해라
                    print("꽃게 걸음 왼쪽")
                    side_lr = "LEFT"

                print("side walk -------", side_walk)
                # motion.py에 walk_side for문이 없어서 임시로 여기다 넣음
                for _ in range(side_walk):
                    motion.walk_side(side_lr)
                
            motion.head("DEFAULT", 2) # LR 한 후 고개 디폴트
                    
            print("holecup YES")
            ###### 홀컵 찾음, 중앙 맞췄음. 일직선 맞추고, 이제 거리 재야됨

            
            '''
            while True:
                # 공 홀컵 일직선 맞추기 => 홀컵만으로 판별
                print("!!call straight ")
                check_straight = head.straight()
                if check_straight == True: # 거리 알고리즘으로 넘어감
                    print("straight true!!")
                    break
                elif check_straight == "Except":
                    print("straight except")
                    while True:
                        # straight의 Except 처리
                        # 홀컵이 안보이는 경우이므로, 홀컵을 찾는 과정
                        # 문제점 : 홀컵 UD는 몸을 움직이지 않음. 근데 몸 움직여야함ㅠ

                        motion.head("DEFAULT", 1)
                        is_big_UD = big_UD("holecup")
                        
                        if is_big_UD == "Except":
                            big_LR("holecup")
                        is_small_LR = small_LR("holecup")
                        
                        if is_small_LR == "Except" :
                            motion.head("DEFAULT", 2) # small_LR 한 후 고개 디폴트
                            # big 알고리즘으로 넘어감

                            big_LR("holecup") # 이거 한번만 실행하면 무조건 찾을 거라고 생각해서 while로 안 돌아감.
                        else:
                            break
                else:
                    continue   
            '''   

            
            while True:
                # 공 홀컵 일직선 맞추기
                print("!!call straight ")
                check_straight = head.straight()
                if check_straight == True: # 거리 알고리즘으로 넘어감
                    print("straight true!!")
                    break
                elif check_straight == "Except":
                    print("straight except")
                    while True:
                        motion.head("DEFAULT", 1)
                        is_big_UD = big_UD("ball")
                        
                        if is_big_UD == "Except":
                            big_LR("ball")
                        is_small_LR = small_LR("ball")
                        
                        if is_small_LR == "Except" :
                            motion.head("DEFAULT", 2) # small_LR 한 후 고개 디폴트
                            # big 알고리즘으로 넘어감
                            # is_big_LR = big_LR("ball") 하러 처음으로 올라감 
                            big_LR("ball") # 이거 한번만 실행하면 무조건 찾을 거라고 생각해서 while로 안 돌아감.
                        else:
                            break
                else:
                    continue
                     
                    
                
            ##### straight 알고리즘하다가 중앙이 흐트려졌을 거라 판단하여 -> 중앙 맞추기 시작
            
            ### field 블랙 판별 => 좌우 퍼팅 결정   
            Distance.field = robo._image_processor.field() #return left, right
            Distance.field = "left" ##temp
            #몸 퍼팅 위치에 서기
            if Distance.field == "left" :
                print("field left!!")
                motion.pose("LEFT")
            elif Distance.field == "right" :
                print("field right!!")
                motion.pose("RIGHT")

            
            ''' 홀컵 찾기, 홀컵 거리 재기 안 할 거라 일단 주석처리했음
            
            # 거리 알고리즘    
            # ud_for_dist 하기전에 고개 세팅
            motion.head("DEFAULT", 2) # 고개 디폴트
            Distance.Head_ud_angle = Distance.Head_UD_Middle_Value_Measures
            motion.head("DEFAULT", 1) # 고개 디폴트
            
            motion.head("DOWN", 45)
            time.sleep(2)
            
            # ud_for_dist 하기전에 holecup 찾기
            # holecup찾기 (고개 O, 몸 X)
            while True:
                big_LR("holecup")
                is_small_LR = small_LR("holecup")

                if is_small_LR == "Except" :
                    print("holecup small lr except")
                    motion.head("DEFAULT", 2) # small_LR 한 후 고개 디폴트
                    
                    big_LR("holecup") # 이거 한번만 실행하면 무조건 찾을 거라고 생각해서 while로 안 돌아감.
                else:
                    break
            
            
            motion.head("DOWN", 45)
            Distance.Head_UD_Angle = 10
            holecup_UD_for_dist() # 홀컵 거리 재기
            motion.head("DEFAULT", 1) # ud for dist 이후 고개 상하 디폴트
            time.sleep(2)
                            
            # 홀컵 거리 재기
            Distance.holecup_dist = Distance.Length_ServoAngle_dict.get(Distance.Head_ud_angle)
            
            print("holecup dist : ", Distance.holecup_dist)
            # 이 length를 퍼팅 파워로 바꿔주는 코드 필요 -> 직접해보면서 조절
            '''

            self.act = Act.PUTTING

            # 공 거리는 Act 4(PUTTING)에서 재기

            #return True

        
        
        
        #=======================================================#
        #                      4. Putting                       #         
        #=======================================================#
        
        elif act == Act.PUTTING:             ##### 4. 퍼팅 #################
            
            print("^^^^444444")
            print("^^^^444444")
            print("^^^^444444")
            print("^^^^444444")


            motion.head("DOWN", 45) # 고개 45도로 내리고 공 detect 시작 !
            # motion.head("DOWN", 30) # 고개 45도로 내리고 공 detect 시작 !
            # motion.head("DOWN", 9) # 고개 45도로 내리고 공 detect 시작 !
            # motion.head("DOWN", 6) # 고개 45도로 내리고 공 detect 시작 !
            time.sleep(1)

            Distance.Head_UD_Angle = 55
            
    

            # ud_for_dist 하기전에 고개 세팅
            motion.head("DEFAULT", 2) # 고개 디폴트
            Distance.Head_ud_angle = Distance.Head_UD_Middle_Value_Measures
            motion.head("DEFAULT", 1) # 고개 디폴트

            UD_for_dist("ball") # 공 거리 재기
            motion.head("DEFAULT", 1) # ud for dist 이후 고개 상하 디폴트
            time.sleep(2)

            # length = 거리 
            ball_dist = Distance.Length_ServoAngle_dict.get(Distance.Head_ud_angle)
            print(Distance.Length_ServoAngle_dict)
            print("=====================================")
            print("balL dist:" , ball_dist , " head ud angle:", Distance.Head_ud_angle)
            print("=====================================")
            
            while True:
                print("ball dist :", ball_dist)
                if 15 <= ball_dist <= 21: # 거리 값 조정 필요!
                    break
                elif ball_dist < 15:
                    motion.walk("JBACKWARD")
                    ball_dist += 3
                elif ball_dist > 21:
                    motion.walk("JFORWARD")
                    ball_dist -= 3

            time.sleep(3)
            
            ### 건웅 오빠 필독!
            
            motion.head("DEFAULT",63)
            red_center = robo._image_processor.detect_ball("call_midpoint")
            print("++++++++++++++++++")
            print(red_center)
            print("++++++++++++++++++")
            is_center = False
            while not is_center:
                rectangle_coordinates = [388, 140, 422, 140, 422, 180, 388, 180]
                if is_point_inside_rectangle(red_center, rectangle_coordinates):
                    is_center = True
                else:
                    reference_point = [400, 160]
                    dx, dy = calculate_distance_from_reference(red_center, reference_point) # 15에 1cm
                    x,y = dx/2, dy
                    if(abs(dx)>=25):
                        if (dx<0):
                            while(abs(dx)//30):
                                robo._motion.walk_side("LEFT10")
                        else:
                            while(abs(dx)//30):
                                robo._motion.walk_side("Right10")
                    if(abs(dy)>=25):
                        if (dy<0):
                            while(abs(dy)//30):
                                robo._motion.walk_side("2JBACKWARD")
                        else:
                            while(abs(dy)//30):
                                robo._motion.walk_side("2JFORWARD")
                        
                    
            ### 퍼팅 직전 공의 위치 정확히 두는 코드 여기 들어가야함! 꽃게걸음으로 좌우 조절 
                
                
            ### 진짜 퍼팅
            motion.putting(Distance.field, 1, 2)
            time.sleep(5)
                
                
            self.act = Act.HOLEIN

            motion.turn("LEFT", 45)
            time.sleep(5)
            motion.turn("LEFT", 45)
            time.sleep(3)

            #return True

        
        elif act == Act.HOLEIN:             ##### 5. 홀인 #################
            
            print("^^^^^^^^5555555")
            print("^^^^^^^^5555555")
            print("^^^^^^^^5555555")
            print("^^^^^^^^5555555")
            
            ###### Find ball for HOLEIN ######
            is_ball = robo._image_processor.detect_ball()

            ### False면, big UD LR 해라
            if is_ball == False:          
                while True:
                    print("FAIL ball detect 555")   
                    # big UD head
                    is_big_UD = big_UD("ball")
                    print(" === big ud === for holeIN")

                    #if go_to == "big_lr" :
                    if is_big_UD == "Except" :  # big UD 검출안됨 -> big LR 로 넘어감
                        print("big ud except 555")
                        # big LR 시행하기전에 UD 45도로
                        motion.head("DOWN", 45)
                        
                        big_LR("ball")  # big은 알아서 고개 디폴트 함 
                    
                    is_small_LR = small_LR("ball")
                    
                    if is_small_LR == "Except" :
                        print("small lr except 555")
                        motion.head("DEFAULT", 2) # small_LR 한 후 고개 디폴트
                        # big 알고리즘으로 넘어감
                        # is_big_LR = big_LR("ball") 하러 처음으로 올라감 
                        big_LR("ball") # 이거 한번만 실행하면 무조건 찾을 거라고 생각해서 while로 안 돌아감.
                    else:
                        break
            else:
                print("ball detect 555 => small lr할 거야")
                small_LR("ball") # small lr 함으로써 중앙 맞춰짐

            
            oneframe = robo._image_processor.ball_hole_oneframe()
            if oneframe == True:
                print("is oneframe? yesss")
                check_holein = robo._image_processor.detect_hole_in()
                if check_holein == True:
                    print("ceremony hehehehehe")
                    # 세레모니
                    motion.ceremony()
                    return True
                else:
                    print("holein fail")
                    # 몰라. 3번을 더 간단히?
                    self.act = Act.WALK_BALL
                    
                    motion.head("DEFAULT", 1)
                    time.sleep(1)
                    motion.head("DOWN", 45)
                    time.sleep(1)

            else:   
                print('go putting pos')
                # 원프레임이 아니라서 다시 WALK BALL로
                self.act = Act.WALK_BALL
            
            
            #return True
