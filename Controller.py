from enum import Enum, auto

import time

from Motion import Motion
from Def.ImageProcessor import ImageProcessor
from Robo import Robo

from Def.Detection import Detection


class Act(Enum):
    # 0,1은 없음
    TEESHOT = auto()  # 2. 맨 처음 티샷  
    WALK_BALL = auto()  # 3. 공까지 걸어가기 (걸음수)
    PUTTING_POS = auto()  # 4. 퍼팅 위치에 서기
    PUTTING = auto()  # 5. 퍼팅
    HOLEIN = auto() # 6. 홀인
    


class Controller:
    robo: Robo = Robo()
    act: Act = Act.TEESHOT
    
    @classmethod
    def start(self):
        # 정해진 파워로 한번 퍼팅.
        act = self.act
        robo: Robo = Robo()
        

        if act == act.TEESHOT:
            print("ACT: ", act)  # Debug
            
            self._motion = Motion()  # Motion
            # self._motion.set_head("DOWN", 30) # 티샷######################################
            # time.sleep(0.5)
            self.act = act.WALK_BALL
        
        
        elif act == act.WALK_BALL:
                        
            state = Detection.detect_ball()
            # state = self.robo._image_processor
        
            # findball 함수 호출
            pass

        elif act == act.PUTTING_POS:
            pass
        elif act == act.PUTTING:
            pass
        
        elif act == act.HOLEIN:
            pass
        
            
        
        