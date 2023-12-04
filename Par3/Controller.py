# -*- coding: utf-8 -*-
import time
from Robo import Robo
from Head import Head
from Motion import Motion
import Distance


class Act:
    TEESHOTA = 1          # 1. 맨 처음 티샷  
    TEESHOTB = 2
    WALK_BALL = 3        # 2. 공까지 걸어가기 (걸음수)
    PUTTING_POS = 4      # 3. 퍼팅 위치에 서기
    PUTTING = 5          # 4. 퍼팅
    HOLEIN = 6           # 5. 홀인

class Controller:

    def __init__(self):
        #act = Act.TEESHOT
        pass
    
    act  = Act.PUTTING
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
                    big_ud_angle = Distance.Head_ud_angle
                    return "Success"
                elif is_object_in_frame == False:
                    big_ud_angle = Distance.Head_ud_angle
                
                    if Distance.Head_ud_angle == 55: # Distance.Head_UD_Middle_Value_Measures - 100 + 10 + 45:  # big ud 한 사이클이 끝남. / 9는 바뀔 수 있는 값
                        #Distance.Head_ud_angle = Distance.Head_UD_Middle_Value_Measures # 고개값을 다시 정면100으로 
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
            cnt = 0
            while True:
                cnt += 1
                print(cnt)
                print("---------start small lr head")
                is_vertical_middle, small_lr_temp = head.small_LR_head(object, Distance.head_lr_angle)
                if cnt > 40:
                    print("small lr,,, cnt > 40,,, except")
                    return "Except"
                
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
            small_ud_angle = Distance.Head_ud_angle
            time.sleep(0.5)
            # 거리를 위한 고개 각도 내리기 
            while True:
                print("---------start ud for dist")
                is_horizontal_middle, small_ud_temp = head.head_for_dist(object, small_ud_angle)
                if is_horizontal_middle == True: #최종 중앙 맞춰짐 
                    Distance.Head_ud_angle = small_ud_temp
                    if Distance.Head_ud_angle >= 90:
                        time.sleep(3)
                        continue
                    print("head UD angle : ", Distance.Head_ud_angle)
                    break
                elif is_horizontal_middle == False:
                    small_ud_angle = small_ud_temp
                    Distance.Head_ud_angle = small_ud_temp
                    continue

        # def holecup_UD_for_dist(): # small ud head 변형
        #     small_ud_angle = 10
            
        #     # 거리를 위한 고개 각도 올리기 
        #     while True:
        #         print("---------start HOlECUP ud for dist")
        #         is_horizontal_middle, small_ud_temp = head.head_for_dist("holecup", small_ud_angle)
        #         if is_horizontal_middle == True: #최종 중앙 맞춰짐 
        #             #act = Act.PUTTING_POS 
        #             #variable.Head_ud_angle = 
        #             Distance.Head_ud_angle = small_ud_temp
        #             print("holecup ud angle : ",Distance.Head_ud_angle)
        #             break
        #         elif is_horizontal_middle == False:
        #             if small_ud_angle > small_ud_temp : # 홀컵중점 바껴서 갇히는 현상 해결
        #                 Distance.Head_ud_angle = small_ud_temp  #(상관없) 더 최근 고개값 = 더 먼 거리값
        #                 break
        #             small_ud_angle = small_ud_temp
        #             Distance.Head_ud_angle = small_ud_temp

        #             continue
            
        ###########
        def ball_pos():
            time.sleep(0.2)
            motion.head("DEFAULT", 63)
            time.sleep(1)
            print("++++++++++++++++++")
            print("ball pos")
            print("++++++++++++++++++")
            is_center = False
            x,y = reference_point = [392, 298]
            v = 5
            w = 10
            rectangle_coordinates = [x-v, y-w, x+w, y-w, x+w, y+v, x-v, y+v]
            while not is_center:
                red_center = robo._image_processor.detect_ball('call_midpoint')
                x1, y1, x2, y2, x3, y3, x4, y4 = rectangle_coordinates
                print("현재 빨간공 중심: ", red_center ,"목표 지점: ",reference_point)
                if(red_center == None): 
                    print("지금 화면안에 빨간 공 안보임")
                    motion.walk("BACKWARD")
                    time.sleep(3)
                    continue
                else:
                    if(x1 <= red_center[0] <= x2 and y1 <= red_center[1] <= y4):    
                        print("성공함요")
                        break
                dx = red_center[0] - reference_point[0]
                dy = red_center[1] - reference_point[1]
                
                print("중앙에서 떨어진 거리: ", dx, dy, abs(dx),abs(dy))
                print("dx//30: ",dx//30 ,"dy//30",dy//30)
                if(abs(dx)>=30):
                    if (dx<0):
                        motion.walk_side("LEFT10")
                        print("3")
                    else:
                        motion.walk_side("RIGHT10")
                        print("4")
                elif(abs(dy)>=30):
                    if (dy<0):
                        motion.walk("2JFORWARD")
                        print("1")
                    else:
                        motion.walk("2JBACKWARD")
                        print("2")
                else:
                    is_center = True
                Distance.Head_ud_angle = 63
        
        def Set_holecup_right():
            time.sleep(0.1)
            motion.head("DEFAULT", 0) # 고개 디폴트
            time.sleep(0.1)
            is_left = False
            motion.Rarm("DOWN")
            time.sleep(1)
            for i in range(0,5):
                time.sleep(0.4)
                print("왼쪽에 있는지 확인")
                is_holecup = robo._image_processor.detect_holecup()
                print("CHECK HOLCUP : ", is_holecup)
                if is_holecup:
                    print("왼편에 있음")
                    is_left = True
                    break
                time.sleep(0.1)
                motion.head("RIGHT",20)
                time.sleep(0.5)
            print("is_left: ", is_left)
            motion.head("RIGHT",90)    # 머리 오른쪽 90도
            time.sleep(1)
            print("팔 내리고 머리 90으로 돌림")
            if is_left:
                while True:
                    is_holecup =  robo._image_processor.detect_holecup()
                    print("홀컵 있는지 확인", is_holecup)
                    if is_holecup:
                        print("찾음")
                        break
                    time.sleep(0.1)
                    robo._motion.holecup_turn('LEFT', 20)
                    print("완쪽으로 몸 돌리기")
                    time.sleep(1)
            else:
                while True:
                    time.sleep(0.1)
                    robo._motion.holecup_turn('RIGHT', 10)
                    print("오른쪽으로 몸 돌리기")
                    time.sleep(1)
                    is_holecup =  robo._image_processor.detect_holecup()
                    print("홀컵있는지 확인", is_holecup)
                    if is_holecup:
                        print("찾음")
                        is_left = True
                        break
             
            while True:
                time.sleep(0.2)
                mid = 340
                min = mid - 8
                max = mid + 8
                holecup_midpoint = robo._image_processor.detect_holecup("call_toppoint")
                print("홀컵 중앙은", holecup_midpoint, "목푤는 : ", min, max)
                if is_left and holecup_midpoint == (0,0):
                    robo._motion.holecup_turn('LEFT', 10)
                if min<=holecup_midpoint[0] <= max:
                    print("범위안에 들어옴 종료 성공")
                    robo._motion.Rarm('RESET')
                    time.sleep(0.5)
                    motion.head("DEFAULT", 0) # 고개 디폴트
                    time.sleep(0.5)
                    break
                elif holecup_midpoint[0] >= max:
                    if holecup_midpoint[0] > max + 150:
                        print("RIGHT 회전하고 쉬기")
                        time.sleep(0.1)
                        robo._motion.holecup_turn('RIGHT', 20)
                        time.sleep(0.1)
                    else:
                        print("RIGHT 회전하고 쉬기")
                        time.sleep(0.1)
                        robo._motion.holecup_turn('RIGHT', 5)
                        time.sleep(0.1)
                elif min>=holecup_midpoint[0]:
                    if min-150>=holecup_midpoint[0]:
                        print("왼쪽 회전하고 쉬기")
                        time.sleep(0.1)
                        robo._motion.holecup_turn('LEFT', 20)
                        time.sleep(0.1)
                    else:
                        print("왼쪽 회전하고 쉬기")
                        time.sleep(0.2)
                        robo._motion.holecup_turn('LEFT', 5)
                        time.sleep(0.1)
       
        def Set_holecup_left():
            time.sleep(0.5)
            motion.head("DEFAULT", 0) # 고개 디폴트
            ### 고개 내리는 거  
            #motion.head("DOWN", 60) # 고개 디폴트
            
            time.sleep(1)
            is_right = False
            #print("is_left: ", is_right)
            
            for i in range(0,3):
                time.sleep(0.1)
                is_holecup = robo._image_processor.detect_holecup()
                print(i,"HOLCUP은: ", is_holecup)
                if is_holecup:
                    print("right편에 있음")
                    is_right = True
                    break
                time.sleep(0.1)
                motion.head("LEFT",30)
                time.sleep(1)
            print("is_left: ", is_right)
            motion.head("LEFT",90)    # 머리 오른쪽 90도
            time.sleep(0.2)
            print("머리 90으로 돌림")
            if is_right:
                while True:
                    is_holecup =  robo._image_processor.detect_holecup()
                    print("홀컵 있는지 확인", is_holecup)
                    if is_holecup:
                        print("찾음")
                        break
                    time.sleep(0.1)
                    robo._motion.turn('RIGHT', 20)
                    print("오른쪽으로 몸 돌리기")
                    time.sleep(0.1)
            else:
                while True:
                    time.sleep(0.1)
                    is_holecup =  robo._image_processor.detect_holecup()
                    print("홀컵있는지 확인", is_holecup)
                    if is_holecup:
                        print("찾음")
                        is_right = True
                        break
                    robo._motion.turn('LEFT', 45)
                    print("왼쪽으로 몸 돌리기")
                    time.sleep(0.1)



            while True:
                time.sleep(0.2)
                holecup_midpoint = robo._image_processor.detect_holecup("call_toppoint")
                mid = 445               ###### if body left ++, if body right --
                min = mid - 10
                max = mid + 10
                
                print("홀컵 중앙은", holecup_midpoint, "목푤는 : ", min, max)
                if holecup_midpoint == (0,0):
                    robo._motion.turn('RIGHT', 20)
                    time.sleep(0.5)
                if min<=holecup_midpoint[0] <= max:
                    print("범위안에 들어옴 종료 성공")  
                    motion.head("DEFAULT", 0) # 고개 디폴트
                    time.sleep(1)
                    break
                elif holecup_midpoint[0] > max:
                        print("오른쪽 5 회전하고 쉬기")
                        robo._motion.holecup_turn('RIGHT', 5)
                        time.sleep(0.1)
                elif min>holecup_midpoint[0]:
                    if holecup_midpoint[0] < min-150:
                        print("왼쪽 10 회전하고 쉬기")
                        robo._motion.holecup_turn('LEFT', 10)
                        time.sleep(0.1)
                    else:
                        print("왼쪽 5 회전하고 쉬기")
                        robo._motion.holecup_turn('LEFT', 5)
                        time.sleep(0.1)
        
        
        #=======================================================#
        #                      1. Teeshot A                     #         
        #=======================================================#
        
        if act == Act.TEESHOTA:                 ##### 1. 시작 및 티샷 #################
            print("ACT: ", act, "Teeshot A") # Debug
            '''
            time.sleep(3)
            is_ball = robo._image_processor.detect_ball()

            ### False면, big UD LR 해라
            if is_ball == False:                
                while True:
                    # big UD head
                    is_big_UD = big_UD("ball")

                    if is_big_UD == "Except" :  # big UD 검출안됨 -> big LR 로 넘어감
                        big_LR("ball")  # big은 알아서 고개 디폴트 함 
                    
                    is_small_LR = ball_small_LR("ball")
                    
                    if is_small_LR == "Except" :
                        time.sleep(1)
                        motion.head("DEFAULT", 0)
                        Distance.Head_ud_angle = Distance.Head_UD_Middle_Value_Measures
                        time.sleep(1)
                        continue
                    else:
                        break
                    
            else:
                ball_small_LR("ball") # small lr 함으로써 중앙 맞춰짐

            # ud_for_dist 하기전에 고개 세팅
            motion.head("DEFAULT", 0)
            Distance.Head_ud_angle = Distance.Head_UD_Middle_Value_Measures
            time.sleep(2)
            '''

            UD_for_dist("ball")
    
            # length = 거리 
            ball_dist = Distance.Length_ServoAngle_dict.get(Distance.Head_ud_angle)
            print(Distance.Length_ServoAngle_dict)
            print("==========================================")
            print("ball dist: ", ball_dist , "===========","head angle: ", Distance.Head_ud_angle)
            print("==========================================")

            motion.head("DEFAULT", 1) # ud for dist 이후 고개 상하 디폴트
            Distance.Head_ud_angle = Distance.Head_UD_Middle_Value_Measures
            time.sleep(2)

            '''
            if ball_dist > 18:
                motion.walk("FORWARD", ball_dist - 18)
            elif ball_dist == 18:
                print("correct!")
            else :      # 최소 거리 18보다 더 가까이 있을 경우: 뒷걸음질
                motion.walk("BACKWARD", ball_dist - 18)
            '''
                
                
                
            point = 0   # 점 1, 2, 3 할당

            if ball_dist < 26:      # 점 1
                point = 1
            elif ball_dist < 46:    # 점 2
                point = 2
                motion.walk("FORWARD", ball_dist - 18)
            else :   
                point = 3               # 점 3
                motion.walk("FORWARD", ball_dist - 18)
                
                
            ball_pos()
            time.sleep(1)
            
            
            if point==1:
                motion.turn("RIGHT", 10)
                time.sleep(1)
            elif point==2:
                pass
            elif point==3:
                motion.turn("LEFT", 10)
                time.sleep(1)
                
                
            #Set_holecup_right()
            
            #ball_pos()
            #time.sleep(1)
            

            # PUTTING
            time.sleep(3)
            motion.putting("LEFT", 3, 2)
            print("putting")
            time.sleep(5)
            
            motion.walk_side("LEFT120cm")
            time.sleep(15)


            # turn body left, 몸을 왼쪽으로 90도 돌림.           
            motion.turn("LEFT", 90)
            time.sleep(4)
            motion.turn("LEFT", 10)
            time.sleep(0.5)

            self.act = Act.WALK_BALL
            
            # return True
            
            
        #=======================================================#
        #                      2. Teeshot B                     #         
        #=======================================================#
        
        
        elif act == Act.TEESHOTB:                 ##### 1. 시작 및 티샷 #################
            print("ACT: ", act, "Teeshot B") # Debug


            time.sleep(3)
            is_ball = False
            is_ball = robo._image_processor.detect_ball()
            
            ### False면, big UD LR 해라
            if is_ball == False:                
                while True:
                    # big UD head
                    is_big_UD = big_UD("ball")
                    motion.head("DOWN", 9)
                    motion.head("DOWN", 6)
                    Distance.Head_ud_angle -= 15

                    if is_big_UD == "Except" :  # big UD 검출안됨 -> big LR 로 넘어감
                        big_LR("ball2")  # big은 알아서 고개 디폴트 함 
                    
                    is_small_LR = small_LR("ball2")
                    
                    if is_small_LR == "Except" :
                        time.sleep(1)
                        motion.head("DEFAULT", 0)
                        Distance.Head_ud_angle = Distance.Head_UD_Middle_Value_Measures
                        time.sleep(1)
                        continue
                    else:
                        break
                    
            else:
                small_LR("ball2") # small lr 함으로써 중앙 맞춰짐
                
            point = 0
            if Distance.head_lr_angle <= 85:
                motion.walk_side("LEFT70") # loop문 추가 / 수정 필수
                time.sleep(0.2)
                motion.walk_side("LEFT70")
                time.sleep(0.2)
                motion.walk_side("LEFT70")
                time.sleep(0.2)
                motion.walk_side("LEFT70")
                time.sleep(0.2)
                motion.pose("RIGHT", True)
                time.sleep(2)
                motion.turn("RIGHT", 20)
                print("1번 점에서 확인")
                point = 1
            elif Distance.head_lr_angle >= 115:
                motion.walk_side("RIGHT70") # loop문 추가
                time.sleep(0.2)
                motion.walk_side("RIGHT70")
                time.sleep(0.2)
                motion.walk_side("RIGHT70")
                time.sleep(0.2)
                motion.walk_side("RIGHT70")
                time.sleep(0.2)
                motion.pose("LEFT", True)
                time.sleep(2)
                motion.turn("LEFT", 10)
                print("3번 점에서 확인")
                point = 3
            else:
                print("2번 점에서 확인")
                motion.pose("LEFT", True)
                time.sleep(2)
                point = 2
            
            #-----------------------------------------------------------------------------------------------------

            # ud_for_dist 하기전에 고개 세팅
            motion.head("DEFAULT", 0)
            Distance.Head_ud_angle = Distance.Head_UD_Middle_Value_Measures
            time.sleep(2)

            # UD_for_dist("ball")
            # motion.head("DEFAULT", 1) # ud for dist 이후 고개 상하 디폴트
            # time.sleep(1)

            # # length = 거리 
            # ball_dist = Distance.Length_ServoAngle_dict.get(Distance.Head_ud_angle)
            # print(Distance.Length_ServoAngle_dict)
            # print("==========================================")
            # print("ball dist: ", ball_dist , "===========","head angle: ", Distance.Head_ud_angle)
            # print("==========================================")

            # if ball_dist > 18:
            #     motion.walk("FORWARD", ball_dist - 18)
            #     time.sleep(1)
            # elif ball_dist == 18:
            #     print("correct!")
            # else :      # 최소 거리 18보다 더 가까이 있을 경우: 뒷걸음질
            #     motion.walk("BACKWARD", ball_dist - 18)
            #     time.sleep(1)
                
                

            ball_pos()
            time.sleep(1)
            
            if point == 1:
                time.sleep(1)
                motion.putting("RIGHT", 3)
                time.sleep(5)
                
                motion.turn("RIGHT", 45)
                time.sleep(2)
                motion.turn("RIGHT", 45)
                time.sleep(2)
            elif point == 2:
                time.sleep(1)
                motion.putting("LEFT", 3)
                time.sleep(5)
                motion.turn("LEFT", 45)
                time.sleep(2)
                motion.turn("LEFT", 45)
                time.sleep(2)
                # motion.turn("LEFT", 10)
                # time.sleep(3)
            elif point == 3:
                time.sleep(1)
                motion.putting("LEFT", 3)
                time.sleep(5)
                motion.turn("LEFT", 45)
                time.sleep(2)
                motion.turn("LEFT", 45)
                time.sleep(2)
                # motion.turn("LEFT", 10)
                # time.sleep(2)
                 
            self.act = Act.WALK_BALL
            time.sleep(3)
            motion.turn("LEFT", 10)
            time.sleep(2)
            print("start forward 12")
            motion.walk("FORWARD13")
            time.sleep(22)

            
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

            
            motion.head("UP", 9)
            time.sleep(1)
            motion.head("UP", 9)
            # 지금 각도 45도임
        
            
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

                    if is_big_UD == "Except" :  # big UD 검출안됨 -> big LR 로 넘어감
                        motion.head("UP", 6)
                        big_LR("ball")  # big은 알아서 고개 디폴트 함 
                    
                    is_small_LR = ball_small_LR("ball")
                    
                    if is_small_LR == "Except" :
                        time.sleep(1)
                        motion.head("DEFAULT", 0)
                        Distance.Head_ud_angle = Distance.Head_UD_Middle_Value_Measures
                        time.sleep(1)
                        continue
                    else:
                        break
            else:
                ball_small_LR("ball") # small lr 함으로써 중앙 맞춰짐
            
            # ud_for_dist 하기전에 고개 세팅
            motion.head("DEFAULT", 0)
            Distance.Head_ud_angle = Distance.Head_UD_Middle_Value_Measures
            time.sleep(2)
            
            print("ball detected")
            UD_for_dist("ball")
            motion.head("DEFAULT", 1) # ud for dist 이후 고개 상하 디폴트
            time.sleep(1)

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

            time.sleep(2)
            
            #---------------------ball dist one more time     
            
            '''
            motion.head("DOWN", 45) # 고개 45도로 내리고 공 detect 시작 !
            time.sleep(2)

            is_ball = robo._image_processor.detect_ball()

            ### False면, big UD LR 해라
            if is_ball == False:  
                motion.head("DEFAULT", 1)
                time.sleep(1)                  
                while True:
                    # big UD head
                    is_big_UD = big_UD("ball")
                    print("controller === big ud ")

                    if is_big_UD == "Except" :  # big UD 검출안됨 -> big LR 로 넘어감
                        # motion.head("UP", 9) # after Teeshot 고개 60
                        # motion.head("UP", 6)
                        big_LR("ball")  # big은 알아서 고개 디폴트 함 
                    
                    is_small_LR = ball_small_LR("ball")
                    
                    if is_small_LR == "Except" :
                        time.sleep(1)
                        motion.head("DEFAULT", 0)
                        time.sleep(1)
                        continue
                    else:
                        break
            else:
                ball_small_LR("ball") # small lr 함으로써 중앙 맞춰짐

            # ud_for_dist 하기전에 고개 세팅
            motion.head("DEFAULT", 0)
            Distance.Head_ud_angle = Distance.Head_UD_Middle_Value_Measures
            time.sleep(3)
            
            UD_for_dist("ball")
            motion.head("DEFAULT", 1) # ud for dist 이후 고개 상하 디폴트
            time.sleep(2)

            # length = 거리 
            ball_dist = Distance.Length_ServoAngle_dict.get(Distance.Head_ud_angle)
            print("ball distance :", ball_dist)  


            if ball_dist > 26:  # 18+8 (화면에 여유있게 들어오도록)
                motion.walk("FORWARD", ball_dist - 26)
                    
            elif ball_dist == 26:
                print("correct!")
            else :      # 최소 거리 18보다 더 가까이 있을 경우: 뒷걸음질
                motion.walk("BACKWARD", ball_dist - 26)    
            '''
            
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

            time.sleep(1)
            motion.head("DOWN", 45) # 고개 45도로 내리고 공 detect 시작 !
            time.sleep(1)
            Distance.Head_UD_Angle = 55
            
            
            is_holecup_in_frame = robo._image_processor.detect_holecup()
            
            
            
            if is_holecup_in_frame == False:  
                motion.head("DEFAULT", 1) # 고개 상하 디폴트  
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
                        time.sleep(1)
                        motion.head("DEFAULT", 0)
                        Distance.Head_ud_angle = Distance.Head_UD_Middle_Value_Measures
                        time.sleep(1)
                        continue 
                    else:
                        break
            motion.head("DEFAULT", 2) # after small lr, occur error, so add default 2

            '''
                #====== holecup 고개 방향만큼 꽃게 걸음 ======#
                side_walk = int(abs(100-Distance.head_lr_angle)//10) # 식은 시행착오거치면서 변경예정

                print("**꽃게 걸음 시작**")
                # side walk 방향 설정 
                if  Distance.head_lr_angle < 100:
                    # 고개가 왼쪽L이면 오른쪽R으로 side walk해라
                    print("꽃게 걸음 오른쪽")
                    side_lr = "RIGHT"
                elif Distance.head_lr_angle > 100 : 
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
                        Distance.Head_ud_angle = 100
                        # 매번 고개 디폴트했다가 54도로 갔다가 하는 거
                        is_big_UD = big_UD("ball")
                        
                        if is_big_UD == "Except":
                            robo._motion.head("UP", 9)
                            big_LR("ball")
                        is_small_LR = ball_small_LR("ball")
                        
                        if is_small_LR == "Except" :
                            time.sleep(1)
                            motion.head("DEFAULT", 0)
                            Distance.Head_ud_angle = Distance.Head_UD_Middle_Value_Measures
                            time.sleep(1)
                            continue
                        else:
                            break
                else:
                    continue
                
                     
            motion.pose("LEFT")
            time.sleep(3)

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

            '''
            # ud_for_dist 하기전에 고개 세팅
            motion.head("DEFAULT", 2) # 고개 디폴트
            time.sleep(1)
            Distance.Head_ud_angle = Distance.Head_UD_Middle_Value_Measures
            motion.head("DEFAULT", 1) # 고개 디폴트
            time.sleep(1)

            UD_for_dist("ball") # 공 거리 재기
            motion.head("DEFAULT", 1) # ud for dist 이후 고개 상하 디폴트
            time.sleep(2)

            # length = 거리 
            ball_dist = Distance.Length_ServoAngle_dict.get(Distance.Head_ud_angle)
            print(Distance.Length_ServoAngle_dict)
            print("=====================================")
            print("balL dist:" , ball_dist , " head ud angle:", Distance.Head_ud_angle)
            print("=====================================")

                 
                    
            if ball_dist > 18:  # 18+8 (화면에 여유있게 들어오도록)
                motion.walk("FORWARD", ball_dist - 18)
            elif ball_dist == 18:
                print("correct!")
            else :      # 최소 거리 18보다 더 가까이 있을 경우: 뒷걸음질
                motion.walk("BACKWARD", ball_dist - 18)    
            '''
         
            ball_pos() 
            Set_holecup_left()
            ball_pos() 
                
                
            ### 진짜 퍼팅
            motion.putting("LEFT", 4, 2)
            time.sleep(5)
                
                
            self.act = Act.HOLEIN

            motion.turn("LEFT", 45)
            time.sleep(1)
            motion.turn("LEFT", 20)
            time.sleep(1)

            #return True

        
        elif act == Act.HOLEIN:             ##### 5. 홀인 #################
            
            print("^^^^^^^^5555555")
            print("^^^^^^^^5555555")
            print("^^^^^^^^5555555")
            print("^^^^^^^^5555555")

            motion.head("UP", 9)
            time.sleep(1)
            motion.head("UP", 9)
            # 지금 각도 45도임
            
            ###### Find ball for HOLEIN ######
            is_ball = robo._image_processor.detect_ball()

            ### False면, big UD LR 해라
            if is_ball == False: 
                motion.head("DEFAULT", 1)
                time.sleep(1)         
                while True:
                    print("FAIL ball detect 555")   
                    # big UD head
                    is_big_UD = big_UD("ball")
                    print(" === big ud === for holeIN")

                    if is_big_UD == "Except" :  # big UD 검출안됨 -> big LR 로 넘어감
                        print("big ud except 555")
                        # big LR 시행하기전에 UD 45도로
                        #motion.head("DOWN", 45)
                        
                        big_LR("ball")  # big은 알아서 고개 디폴트 함 
                        
                    elif is_big_UD == "Success" : # big ud에서 너무 아래쪽에 공이 검출될까봐 조금만 더 내려줌
                        motion.head("DOWN", 3)
                    
                    
                    is_small_LR = ball_small_LR("ball")
                    
                    if is_small_LR == "Except" :
                        time.sleep(1)
                        motion.head("DEFAULT", 0)
                        Distance.Head_ud_angle = Distance.Head_UD_Middle_Value_Measures
                        time.sleep(1)
                        continue
                    else:
                        break
            else:
                print("ball detect 555 => small lr할 거야")
                ball_small_LR("ball") # small lr 함으로써 중앙 맞춰짐

            time.sleep(0.5)
            motion.head("DEFAULT", 2)
            time.sleep(1)

            oneframe = robo._image_processor.ball_hole_oneframe()
            if oneframe == True:
                print("is oneframe? YESsss")
                check_holein = robo._image_processor.detect_hole_in()
                if check_holein == True:
                    print("ceremony hehehehehe")
                    # 세레모니
                    motion.ceremony()
                    return True
                else:
                    print("------홀인 실패------")
                    self.act = Act.WALK_BALL
            else:   
                print('원프레임이 아니라서 WALK BALL로')
                # 원프레임이 아니라서 다시 WALK BALL로
                self.act = Act.WALK_BALL
            
            
            #return True