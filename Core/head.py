from Robo import Robo
from Vision.Ball_middle import Ball
from Controller import Controller


class Head:
    def __init__(self):
        pass
        
    robo = Robo()
    big_lr_angle = 0
    small_lr_angle = 0
    big_ud_angle = 0
    small_ud_angle = 0

    max_right_flag = 0
        
    def big_LR_head(self, detect_object, big_lr_angle):
        robo = self.robo
        
        check = False
        
        if detect_object == 'ball':
            check = robo._image_processor.detect_ball()
        elif detect_object == 'hole_cup':
            check = robo._image_processor.detect_holecup() ##############함수 바꿔야함 
        
        if check == True:
            # 공이 화면 안에 들어왔을 경우 big_lr_angle 만큼 몸 돌리기
            if Controller.big_lr_angle > 0:
                robo._motion.body("right")
            elif big_lr_angle < 0:
                robo._motion.body("left")

            return True, big_lr_angle
        
        else:   # 물체가 화면에 안 보이는 경우 detect : False
            # 패닝 틸팅? or 걷기?
            # 고개 각도 크게 돌리기, Find ball과 다름
            if max_right_flag == 0:
                robo._motion.head("right") ################# 3도보단 큰 각으로
                big_lr_angle += 10 # 10은 임의 값
                if big_lr_angle == max(): # <-max() 에러 안 나려고 적어 놓음, 바꾸삼 / 최대값이면 
                    max_right_flag = 1
                    big_lr_angle = 0
                    # 고개 정면(default)로 돌려놓기                        
            elif max_right_flag == 1:
                robo._motion.head("left") ################# 3도보단 큰 각으로
                big_lr_angle -= 10 # 10은 임의 값
            return check, big_lr_angle
                
    def small_LR_head(self, detect_object, small_lr_angle):
        robo = self.robo

        if detect_object == 'ball':
            check = robo._image_processor.middle_lr_ball()
        elif detect_object == 'hole_cup':
            check = robo._image_processor.middle_lr_holecup() ##함수 만들기 

        if check == "stop":
            # 공을 화면 중앙에 오도록 만드는 고개 각도 small_angle 만큼 몸 돌리기
            if small_lr_angle > 0:
                robo._motion.body("right")
            elif small_lr_angle < 0:
                robo._motion.body("left")
                            
            return True, small_lr_angle
            
        elif check == "go right":
            robo._motion.head("right") ################# 고개 오른쪽으로 돌리는 모션 / 3도 씩 움직이기
            small_lr_angle += 3    
            return False, small_lr_angle                
        elif check == "go left":
            robo._motion.head("left") ################# 고개 왼쪽으로 돌리는 모션
            small_lr_angle -= 3
            return False, small_lr_angle
        
        # elif check == "go far":
        #     return False, small_lr_angle 예외사항 

    def big_UD_head(self, detect_object, direction):
        robo = self.robo
        
        check = False
        
        if detect_object == 'ball':
            check = robo._image_processor.detect_ball()
        elif detect_object == 'hole_cup':
            check = robo._image_processor.detect_holecup() ##############함수 바꿔야함 
        
        if check == True:
            return True # small head 부르기
        
        else:   # 물체가 화면에 안 보이는 경우 detect : False
            # 패닝 틸팅? or 걷기?
            # 고개 각도 크게 돌리기, Find ball과 다름
            if max_down_flag == 0:
                robo._motion.head("down") ################# 3도보단 큰 각으로
                big_ud_angle += 10 # 10은 임의 값
                if big_ud_angle == max(): # <-max() 에러 안 나려고 적어 놓음, 바꾸삼 / 최대값이면 
                    max_down_flag = 1
                    big_ud_angle = 0
                    # 고개 정면(default)로 돌려놓기                        
            elif max_down_flag == 1:
                robo._motion.head("up") ################# 3도보단 큰 각으로
                big_ud_angle -= 10 # 10은 임의 값
                
                
    def small_UD_head(self, detect_object, small_ud_angle):
        robo = self.robo

        if detect_object == 'ball':
            direction = robo._image_processor.middle_ud_ball() ##함수 만들기
        elif detect_object == 'hole_cup':
            direction = robo._image_processor.middle_ud_holecup() ##함수 만들기
        if direction == "stop":
            
            return True, small_ud_angle
            
        elif direction == "up":
            robo._motion.head("up") ################# 고개 오른쪽으로 돌리는 모션 / 3도 씩 움직이기
            small_ud_angle += 3 
            return False, small_ud_angle          
        elif direction == "dowm":
            robo._motion.head("dowm") ################# 고개 왼쪽으로 돌리는 모션
            small_ud_angle -= 3
            return False, small_ud_angle
        # elif find_ball == "go far": ##예외사항 
        #     pass 
    