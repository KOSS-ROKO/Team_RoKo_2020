from Robo import Robo
from Vision.Ball_middle import Ball

class Head:
    def __init__(self):
        pass
        
    robo = Robo()
    act  = Act.TEESHOT
        
    def big_head(self, detect_object):
        robo = self.robo
        
        check = False
        
        if detect_object == 'ball':
            check = robo._image_processor.detect_ball()
        elif detect_object == 'hole_cup':
            check = robo._image_processor.detect_holecup()
        
        if check == True:
            # 공이 화면 안에 들어왔을 경우 big_angle 만큼 몸 돌리기
            if big_angle > 0:
                robo._motion.body_right("")
            elif big_angle < 0:
                robo._motion.body_left("")

            return True # small head 부르기
        
        else:   # 물체가 화면에 안 보이는 경우 detect : False
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
                
                
    def small_head(self, detect_object):
        robo = self.robo
        
        find_ball = Ball.middle_ball()
        if find_ball == "stop":
            # 공을 화면 중앙에 오도록 만드는 고개 각도 small_angle 만큼 몸 돌리기
            if small_angle > 0:
                robo._motion.body_right("")
            elif small_angle < 0:
                robo._motion.body_left("")
                
            act = Act.PUTTING_POS ## 뭐하기로했었는데 뭐였지?
            return 
            
        elif find_ball == "go right":
            robo._motion.head_right("") ################# 고개 오른쪽으로 돌리는 모션 / 3도 씩 움직이기
            small_angle += 3                    
        elif find_ball == "go left":
            robo._motion.head_left("") ################# 고개 왼쪽으로 돌리는 모션
            small_angle -= 3
        
        elif find_ball == "go far":
            act = Act.WALK_BALL