# -*- coding: utf-8 -*-
import time
from Robo import Robo
from Head import Head
from Motion import Motion
import Distance

# Par 4

class Act:
    TEESHOTA = 1          # 1. 맨 처음 티샷  
    TEESHOTB = 2
    SECSHOT = 3
    WALK_BALL = 4       # 2. 공까지 걸어가기 (걸음수)
    PUTTING_POS = 5      # 3. 퍼팅 위치에 서기
    PUTTING = 6         # 4. 퍼팅
    HOLEIN = 7           # 5. 홀인

class Controller:

    def __init__(self):
        #act = Act.TEESHOT
        pass
    
    act  = Act.TEESHOTB
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
                
                    if Distance.Head_ud_angle == 64: # Distance.Head_UD_Middle_Value_Measures - 100 + 10 + 45:  # big ud 한 사이클이 끝남. / 9는 바뀔 수 있는 값
                        #Distance.Head_ud_angle = Distance.Head_UD_Middle_Value_Measures # 고개값을 다시 정면100으로 
                        #go_to = "big_lr"  # LR로 갈지 구분
                        return "Except"
                    else: 
                        continue
                        
                        
        def big_LR(object="ball"):
            Distance.head_lr_angle = 100
            max_right_flag = 0
            print("THis is ", object)
            # big LR head
            while True:
                is_object_in_frame, small_lr_temp, max_right_flag = head.big_LR_head(object, Distance.head_lr_angle, max_right_flag)
                if is_object_in_frame == True:
                    break
                elif is_object_in_frame == False:
                    Distance.head_lr_angle = small_lr_temp
                    print("head_lr_angle : ", Distance.head_lr_angle)
                    continue
                #if big_lr_angle == -90: #왼쪽 max까지 갔는데 공 못찾으면 
                    #head.big_UD_head()
                    # 예외처리 : big up down 코드
            #고개 정면 코드 추가하기

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
                
        def small_LR(object="ball2"):    # ball은 small lr끝난뒤 몸, 고개 그대로, 끝.
            #Distance.head_lr_angle = 100
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
            
        ###########
        def ball_pos(): ## 건웅 오빠
            
            motion.head("DEFAULT",63)

            time.sleep(1)
            print("++++++++++++++++++")
            print("ball pos")
            print("++++++++++++++++++")
            is_center = False
            x,y = reference_point = [374, 316]
            w = 20
            rectangle_coordinates = [x-w, y-w, x+w, y-w, x+w, y+w, x-w, y+w]
            while not is_center:
                motion.head("DEFAULT",63)
                time.sleep(2)
                red_center = robo._image_processor.detect_ball('call_midpoint')
                x1, y1, x2, y2, x3, y3, x4, y4 = rectangle_coordinates
                print("현재 빨간공 중심: ", red_center ,"목표 지점: ",reference_point)
                if(x1 <= red_center[0] <= x2 and y1 <= red_center[1] <= y4):    
                    print("성공함요")
                    break                              
                if(red_center == None): 
                    print("지금 화면안에 빨간 공 안보임")
                    motion.walk("2JBACKWARD")
                    time.sleep(2)
                    continue
                dx = red_center[0] - reference_point[0]
                dy = red_center[1] - reference_point[1]
                
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
        ##########
        
        
        
        #=======================================================#
        #                      1. Teeshot A                     #         
        #=======================================================#
        
        if act == Act.TEESHOTA:                 ##### 1. 시작 및 티샷 #################
            print("ACT: ", act) # Debug

            print("^^첫번째 티샷 111^^")
            is_ball = robo._image_processor.detect_ball()

            ### False면, big UD LR 해라
            if is_ball == False:                
                while True:
                    # big UD head
                    is_big_UD = big_UD("ball")

                    #if go_to == "big_lr" :
                    if is_big_UD == "Except" :  # big UD 검출안됨 -> big LR 로 넘어감
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
                
                
            time.sleep(1)
            ball_pos() ## 건웅 오빠
        
              

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

            self.act = Act.SECSHOT

        #=======================================================#
        #                      2. Teeshot B                     #         
        #=======================================================#
        
        if act == Act.TEESHOTB:                 ##### 1. 시작 및 티샷 #################
            print("ACT: ", act, "Teeshot B") # Debug


            print("^^첫번째 티샷  222^^")
            is_ball = robo._image_processor.detect_ball()

            ### False면, big UD LR 해라
            if is_ball == False:                
                while True:
                    # big UD head
                    is_big_UD = big_UD("ball")
                    motion.head("DOWN", 9)
                    motion.head("DOWN", 6)
                    Distance.Head_ud_angle -= 15


                    #if go_to == "big_lr" :
                    if is_big_UD == "Except" :  # big UD 검출안됨 -> big LR 로 넘어감
                        big_LR("ball2")  # big은 알아서 고개 디폴트 함 
                    
                    is_small_LR = small_LR("ball2")
                    
                    if is_small_LR == "Except" :
                        motion.head("DEFAULT", 2) # small_LR 한 후 고개 디폴트
                        # big 알고리즘으로 넘어감
                        # is_big_LR = big_LR("ball") 하러 처음으로 올라감 
                        big_LR("ball2") # 이거 한번만 실행하면 무조건 찾을 거라고 생각해서 while로 안 돌아감.
                    else:
                        break
                    
            else:
                small_LR("ball2") # small lr 함으로써 중앙 맞춰짐

            point = 0
            # 점 3개 중에 결정
            if Distance.head_lr_angle <= 80:
                motion.walk_side("LEFT70") # loop문 추가 / 수정 필수
                time.sleep(1)
                motion.walk_side("LEFT70")
                time.sleep(1)
                motion.walk_side("LEFT70")
                time.sleep(1)
                motion.walk_side("LEFT70")
                time.sleep(1)
                motion.pose("RIGHT", True)
                time.sleep(1)
                motion.turn("RIGHT", 15)
                print("1번 점에서 확인")
                point = 1
            elif Distance.head_lr_angle >= 120:
                motion.walk_side("RIGHT70") # loop문 추가
                time.sleep(1)
                motion.walk_side("RIGHT70")
                time.sleep(1)
                motion.walk_side("RIGHT70")
                time.sleep(1)
                motion.walk_side("RIGHT70")
                time.sleep(1)
                motion.pose("LEFT")
                time.sleep(1)
                motion.turn("LEFT", 15)
                print("3번 점에서 확인")
                point = 3
            else:
                print("2번 점에서 확인")
                motion.pose("LEFT", True)
                time.sleep(1)
                point = 2
            
            #-----------------------------------------------------------------------------------------------------


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



            ball_pos() ## 건웅 오빠
            
            time.sleep(1)
            motion.head("DEFAULT", 1)
            time.sleep(1)


            
            if point == 1:
                time.sleep(1)
                motion.putting("right", 3)
                time.sleep(5)
                
                motion.turn("RIGHT", 60)
                time.sleep(6)
                motion.turn("RIGHT", 45)
                time.sleep(2)
            elif point == 2:
                time.sleep(1)
                motion.putting("left", 3)
                time.sleep(5)
                
                motion.turn("LEFT", 60)
                time.sleep(6)
                motion.turn("LEFT", 60)
                time.sleep(2)
            elif point == 3:
                time.sleep(1)
                motion.putting("left", 3)
                time.sleep(5)
                
                motion.turn("LEFT", 60)
                time.sleep(5)
                motion.turn("LEFT", 60)
                time.sleep(2)
                motion.turn("LEFT", 10)
                time.sleep(2)
                 
            self.act = Act.WALK_BALL
            time.sleep(1)
            motion.walk("FORWARD14", 1)
            time.sleep(25)

            self.act = Act.SECSHOT


        #=======================================================#
        #                      3. SECSHOT (두번째 티샷)           #         
        #=======================================================#

        elif act == Act.SECSHOT:                 ##### 1. 시작 및 티샷 #################
            print("ACT: ", act) # Debug

            print("^^두번째 티샷^^")

            motion.turn("RIGHT", 45)
            time.sleep(2)
            motion.turn("RIGHT", 45)
            time.sleep(2)
            
            
            motion.head("DOWN", 45) # 고개 45도로 내리고 공 detect 시작 !
            time.sleep(2)
            

            # 공 찾고 중앙 맞추기
            is_ball = robo._image_processor.detect_ball()
            
            ### False면, big UD LR 해라
            if is_ball == False:  
                motion.head("DEFAULT", 1)   
                time.sleep(1)           
                while True:
                    # big UD head
                    is_big_UD = big_UD("ball")
                    time.sleep(0.5)
                    print("controller === big ud ")

                    #if go_to == "big_lr" :
                    if is_big_UD == "Except" :  # big UD 검출안됨 -> big LR 로 넘어감
                        big_LR("ball")  # big은 알아서 고개 디폴트 함 
                    
                    is_small_LR = ball_small_LR("ball")
                    
                    if is_small_LR == "Except" :
                        motion.head("DEFAULT", 2) # small_LR 한 후 고개 디폴트
                        big_LR("ball") # 이거 한번만 실행하면 무조건 찾을 거라고 생각해서 while로 안 돌아감.
                    else:
                        break
            else:
                ball_small_LR("ball") # small lr 함으로써 중앙 맞춰짐
            

            ## 이제 남은 거리만큼 공까지 걷기
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
            
        
            # 남은 거리 만큼 걷기
            if ball_dist > 18:  # 18+8 (화면에 여유있게 들어오도록)
                motion.walk("FORWARD", ball_dist - 18) 
            elif ball_dist == 18:
                print("correct!")
            else :      # 최소 거리 18보다 더 가까이 있을 경우: 뒷걸음질
                motion.walk("BACKWARD", ball_dist - 18)   

            #================================#
            #        퍼팅 포즈처럼 돌기          #
            #================================#

            # 좌퍼팅 준비자세처럼 서야 Straight가능
            motion.pose("LEFT", True) # 18cm 용 포즈
            
            #================================#
            #      두번째 티샷의 Act.3          #
            #================================# 
            # straight 안 하고 하드코딩.

            #================================#
            #           두번째 티샷            #
            #================================#

            ball_pos() ## 건웅 오빠
            
            motion.head("DEFAULT", 1)
            time.sleep(1)


            ### 진짜 두번째 TEESHOT
            motion.putting("LEFT", 3)
            time.sleep(5)
                
                
            self.act = Act.WALK_BALL

            motion.turn("LEFT", 45)
            time.sleep(2)
            motion.turn("LEFT", 45)
            time.sleep(2)


            # return True
        
        #=======================================================#
        #                        2. Walk                        #         
        #=======================================================#
        
        
        
        #-----------------------------------#
        # 민주, 희 필독!!                    #
        # 파3 2번 walk부터 쭈우우욱 복붙 하기.#
        #-----------------------------------#