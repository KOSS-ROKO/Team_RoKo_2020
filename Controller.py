# -*- coding: utf-8 -*-

import time
from Def.ImageProcessor import ImageProcessor
from Robo import Robo
from Motion import Motion
from enum import Enum

class Act(Enum):
    FIND_BALL = 1

class Controller:
    robo = Robo()
    act  = Act.FIND_BALL

    @classmethod
    def start(cls):
        # 정해진 파워로 한번 퍼팅.
        act = cls.act
        robo = cls.robo

        if act == Act.FIND_BALL:
            print("ACT: ", act)  # Debug
            state = robo._image_processor.detect_ball()

            if state:
                robo._motion.walk("FORWARD")
            
        
        