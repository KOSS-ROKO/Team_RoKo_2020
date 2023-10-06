from enum import Enum, auto

import time

class Act(Enum):
    

    START = auto()  # 시작   
    TEESHOT = auto()  # 맨 처음 티샷  

    FIND_BALL = auto() # 공이 중앙에 오도록 고개를 (left, right)
    DISTANCE = auto() # 거리 측정 (거리)
    WALK_BALL = auto()  # 공까지 걸어가기 (걸음수)

    LEFT_RIGHT = auto() # 홀컵이 중앙에 오도록 고개를 ( left&right )  (변수에 좌우 angle 값 저장) 
    UP_DOWN = auto() # 홀컵 중앙 맞춘 고개 각도 값 저장 (up&down) (변수에 상하 angle 값 저장) 

    ANGLE_CAL= auto() # 각도, 오왼 계산 / 이동 (오, 왼 얼만큼 둥그렇게 게걸음으로 이동할지)
    PUTTING = auto() # 퍼팅 강도 설정, 퍼팅 하기


    ONEFRAME = auto() # 홀컵-공 한 화면 안에 들어오는지 (True, False)
    HOLEIN  = auto() #홀인여부 판단 (True, False)
    CEREMONY = auto() #세레머니




class Controller:
    
    act: Act = Act.START
    
    @classmethod
    def teeshot(self):
        # 정해진 파워로 한번 퍼팅.
        act = self.act

        if act == act.START:
            print("ACT: ", act)  # Debug
