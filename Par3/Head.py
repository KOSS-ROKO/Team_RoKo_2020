# -*- coding: utf-8 -*-

from Robo import Robo
import time


class Head:
    def __init__(self):
        pass
        
    robo = Robo()

        
    def big_LR_head(self, detect_object, big_lr_angle, max_right_flag):
        print("big lr head start")
        robo = self.robo
        
        check = False
        
        if detect_object == 'ball':
            check = robo._image_processor.detect_ball()

            if check == True:
            # 공이 화면 안에 들어왔을 경우 big_lr_angle 만큼 몸 돌리기
                if big_lr_angle > 100:
                    print("turn right")
                    robo._motion.turn("RIGHT", abs(big_lr_angle - 100))
                    time.sleep(2)
                    robo._motion.turn("RIGHT", 10)
                    time.sleep(1)

                elif big_lr_angle < 100:
                    robo._motion.turn("LEFT", abs(big_lr_angle - 100))
                    time.sleep(2)
                    robo._motion.turn("LEFT", 10)
                    time.sleep(1)
            
                robo._motion.head("DEFAULT", 2)
                time.sleep(1)
                return True, big_lr_angle, max_right_flag
        
            else:   # 물체가 화면에 안 보이는 경우 detect : False
                # 패닝 틸팅? or 걷기?
                # 고개 각도 크게 돌리기, Find ball과 다름
                if max_right_flag == 0:                                                                 
                    robo._motion.head("RIGHT", 30) ################# 3도보단 큰 각으로
                    time.sleep(0.5)
                    big_lr_angle += 30 # 10은 임의 값
                    if big_lr_angle == 190: # <-max() 에러 안 나려고 적어 놓음, 바꾸삼 / 최대값이면 
                        max_right_flag = 1
                        big_lr_angle = 100
                        robo._motion.head("DEFAULT", 2)  # 고개 정면(default)로 돌려놓기 
                        time.sleep(1)

                elif max_right_flag == 1:
                    robo._motion.head("LEFT", 30) ################# 3도보단 큰 각으로
                    time.sleep(0.5)
                    big_lr_angle -= 30 # 10은 임의 값
                    if big_lr_angle == 10: # <-max() 에러 안 나려고 적어 놓음, 바꾸삼 / 최대값이면 
                        max_right_flag = 0
                        big_lr_angle = 100
                        robo._motion.head("DEFAULT", 2)  # 고개 정면(default)로 돌려놓기 
                return check, big_lr_angle, max_right_flag
        
        elif detect_object == 'ball2': # 턴하지 않음
            check = robo._image_processor.detect_ball()
        
            if check == False:
             # 물체가 화면에 안 보이는 경우 detect : False
                # 패닝 틸팅? or 걷기?
                # 고개 각도 크게 돌리기, Find ball과 다름
                if max_right_flag == 0:
                    print("head LEFT")
                    robo._motion.head("LEFT", 30) ################# 3도보단 큰 각으로
                    time.sleep(0.2)
                    big_lr_angle -= 30 # 10은 임의 값
                    if big_lr_angle == 10: # <-max() 에러 안 나려고 적어 놓음, 바꾸삼 / 최대값이면 
                        max_right_flag = 1
                        big_lr_angle = 100
                        robo._motion.head("DEFAULT", 2)  # 고개 정면(default)로 돌려놓기  
                        time.sleep(1)
                                            
                elif max_right_flag == 1:
                    print("head RIGHT")
                    robo._motion.head("RIGHT", 30) ################# 3도보단 큰 각으로
                    time.sleep(0.2)
                    big_lr_angle += 30 # 10은 임의 값
                    if big_lr_angle == 190: # <-max() 에러 안 나려고 적어 놓음, 바꾸삼 / 최대값이면 
                        max_right_flag = 0
                        big_lr_angle = 100 
                        robo._motion.head("DEFAULT", 2)  # 고개 정면(default)로 돌려놓기 
                        time.sleep(1) 

                        
                return check, big_lr_angle, max_right_flag
            else:
                return True, big_lr_angle, max_right_flag
            
        elif detect_object == 'holecup': # 턴하지 않음
            check = robo._image_processor.detect_holecup()
        
            if check == False:
             # 물체가 화면에 안 보이는 경우 detect : False
                # 패닝 틸팅? or 걷기?
                # 고개 각도 크게 돌리기, Find ball과 다름
                if max_right_flag == 0:
                    print("head LEFT")
                    robo._motion.head("LEFT", 30) ################# 3도보단 큰 각으로
                    time.sleep(0.2)
                    big_lr_angle -= 30 # 10은 임의 값
                    if big_lr_angle == 10: # <-max() 에러 안 나려고 적어 놓음, 바꾸삼 / 최대값이면 
                        max_right_flag = 1
                        big_lr_angle = 100
                        robo._motion.head("DEFAULT", 2)  # 고개 정면(default)로 돌려놓기  
                                            
                elif max_right_flag == 1:
                    print("head RIGHT")
                    robo._motion.head("RIGHT", 30) ################# 3도보단 큰 각으로
                    time.sleep(0.2)
                    big_lr_angle += 30 # 10은 임의 값
                    if big_lr_angle == 190: # <-max() 에러 안 나려고 적어 놓음, 바꾸삼 / 최대값이면 
                        max_right_flag = 0
                        big_lr_angle = 100 
                        robo._motion.head("DEFAULT", 2)  # 고개 정면(default)로 돌려놓기  

                        
                return check, big_lr_angle, max_right_flag

            else:
                return True, big_lr_angle, max_right_flag

                
    def small_LR_head(self, detect_object, small_lr_angle):
        robo = self.robo

        if detect_object == 'ball':
            check = robo._image_processor.middle_lr_ball()

            if check == "stop":
            # 공을 화면 중앙에 오도록 만드는 고개 각도 small_angle 만큼 몸 돌리기
                if small_lr_angle > 100:
                    robo._motion.turn("RIGHT", abs(small_lr_angle - 100))
                    #robo._motion.turn("RIGHT", 10)
                elif small_lr_angle < 100:
                    robo._motion.turn("LEFT", abs(small_lr_angle - 100))
                    #robo._motion.turn("LEFT", 10)
                                
                return True, small_lr_angle
            
            elif check == "right":
                robo._motion.head("LEFT", 3) ################# 고개 오른쪽으로 돌리는 모션 / 3도 씩 움직이기
                small_lr_angle -= 3    
                return False, small_lr_angle                
            elif check == "left":
                robo._motion.head("RIGHT", 3) ################# 고개 왼쪽으로 돌리는 모션
                small_lr_angle += 3
                return False, small_lr_angle
            else:
                return 0, small_lr_angle # 예외사항 
        
        elif detect_object == 'ball2':
            check = robo._image_processor.middle_lr_ball()

            if check == "stop":
                # small_angle 만큼 몸 돌리지않기 !                             
                return True, small_lr_angle
                
            elif check == "right":
                robo._motion.head("LEFT", 3) ################# 고개 오른쪽으로 돌리는 모션 / 3도 씩 움직이기
                small_lr_angle -= 3    
                return False, small_lr_angle                
            elif check == "left":
                robo._motion.head("RIGHT", 3) ################# 고개 왼쪽으로 돌리는 모션
                small_lr_angle += 3
                return False, small_lr_angle
            else:
                return 0, small_lr_angle # 예외사항 
        
        elif detect_object == 'holecup':
            check = robo._image_processor.middle_lr_holecup()

            if check == "stop":
                # small_angle 만큼 몸 돌리지않기 !                             
                return True, small_lr_angle
                
            elif check == "right":
                robo._motion.head("LEFT", 3) ################# 고개 오른쪽으로 돌리는 모션 / 3도 씩 움직이기
                small_lr_angle -= 3    
                return False, small_lr_angle                
            elif check == "left":
                robo._motion.head("RIGHT", 3) ################# 고개 왼쪽으로 돌리는 모션
                small_lr_angle += 3
                return False, small_lr_angle
            else:
                return 0, small_lr_angle # 예외사항 

    def big_UD_head(self, detect_object, big_ud_angle):
        robo = self.robo
        
        check = False
        
        max_down_flag = 0
        print("big ud start !!")
        if detect_object == 'ball':
            check = robo._image_processor.detect_ball()
            
        elif detect_object == 'holecup':
            check = robo._image_processor.detect_holecup()
        
        if check == True:
            print("ball is detected")
            return True, big_ud_angle # small head 부르기
        
        else:   # 물체가 화면에 안 보이는 경우 detect : False
            # 패닝 틸팅? or 걷기?
            # 고개 각도 크게 돌리기, Find ball과 다름
            if max_down_flag == 0:
                robo._motion.head("DOWN", 30) ################# 3도보단 큰 각으로
                big_ud_angle -= 30 # 10은 임의 값
                if big_ud_angle == 10: # <-max() 에러 안 나려고 적어 놓음, 바꾸삼 / 최대값이면 
                    max_down_flag = 1
                    big_ud_angle = 64
                    time.sleep(2)
                    robo._motion.head("UP", 30) # 고개 45도로 내리고 공 detect 시작 ! / 나중에 UP 45도 모션 추가할듯?
                    robo._motion.head("UP", 9)
                    robo._motion.head("UP", 6)
                    #robo._motion.head("UP", 9) ###
                    time.sleep(1)
            elif max_down_flag == 1:
                robo._motion.head("UP", 30) ################# 3도보단 큰 각으로
                big_ud_angle += 30 # 30은 임의 값
            return False, big_ud_angle
                
    def small_UD_head(self, detect_object, small_ud_angle):
        robo = self.robo

        if detect_object == 'ball':
            direction = robo._image_processor.middle_ud_ball() ##함수 만들기
        elif detect_object == 'holecup':
            direction = robo._image_processor.middle_ud_holecup() ##함수 만들기
            
        if direction == "stop":
            return True, small_ud_angle
            
        elif direction == "up":
            robo._motion.head("UP", 3) ################# 고개 오른쪽으로 돌리는 모션 / 3도 씩 움직이기
            small_ud_angle += 3 
            return False, small_ud_angle          
        elif direction == "down":
            robo._motion.head("DOWN", 3) ################# 고개 왼쪽으로 돌리는 모션
            small_ud_angle -= 3
            return False, small_ud_angle
        # elif find_ball == "go far": ##예외사항 
        #     pass 
        
        
        
        
        
    def head_for_dist(self, detect_object, small_ud_angle):
        robo = self.robo
        print("head_for_dist")

        if detect_object == 'ball':
            direction = robo._image_processor.middle_ud_ball() ##함수 만들기
            
            if direction == "stop":
                return True, small_ud_angle
            elif direction == "up":
                robo._motion.head("UP", 3) ################# 고개 오른쪽으로 돌리는 모션 / 3도 씩 움직이기
                small_ud_angle += 3 
                return False, small_ud_angle          
            else:
                robo._motion.head("DOWN", 3) ################# 고개 왼쪽으로 돌리는 모션
                small_ud_angle -= 3
                return False, small_ud_angle
        #-----------------
        elif detect_object == 'holecup':
            direction = robo._image_processor.middle_ud_holecup() ##함수 만들기
            
            if direction == "stop":
                return True, small_ud_angle
            elif direction == "down":
                robo._motion.head("DOWN", 3) ################# 고개 오른쪽으로 돌리는 모션 / 3도 씩 움직이기
                small_ud_angle -= 3 
                return False, small_ud_angle          
            else:
                robo._motion.head("UP", 3) ################# 고개 왼쪽으로 돌리는 모션
                small_ud_angle += 3
                return False, small_ud_angle
        # elif find_ball == "go far": ##예외사항 
        #     pass 
    
    
        '''   
    def straight(self):
        robo = self.robo
        check = robo._image_processor.ball_hole_straight()

        if check == "middle":                            
            return True
        elif check == "left":   ###홀컵이 왼쪽에 있음. 오른쪽으로 원그리며 이동
            robo._motion.walk_side("RIGHT10")
            time.sleep(1)
            robo._motion.turn("LEFT", 20)    # 값 조절 필요
            return False               
        elif check == "right":    ## 똑같이 왼쪽으로 이동
            robo._motion.walk_side("LEFT10")
            time.sleep(1)
            robo._motion.turn("RIGHT", 25)    # 값 조절 필요
            return False
        else: # check == "none"
            return "Except"
        
        '''
        
    def straight(self):
        robo = self.robo
        check = robo._image_processor.ball_hole_straight()

        if check == "middle":                            
            return True
        elif check == "right":   ### 찌그째그 걸음으로 오른쪽으로 원그리며 이동
            robo._motion.walk_side("RIGHT10")
            time.sleep(0.5)
            robo._motion.turn("LEFT", 15)    # 값 조절 필요
            time.sleep(1)
            return False               
        elif check == "left":    ## 똑같이 왼쪽으로 이동
            robo._motion.walk_side("LEFT10")
            time.sleep(0.5)
            robo._motion.turn("RIGHT", 15)    # 값 조절 필요
            time.sleep(1)
            return False
        else: # check == "none"
            return "Except"