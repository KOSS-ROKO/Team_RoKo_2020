# -*- coding: utf-8 -*-
import time

from Motion import Motion
import Distance


class Act:
    TEESHOT1 = 1          # 1. 맨 처음 티샷  
    

class Controller:

    def __init__(self):
        #act = Act.TEESHOT
        pass
    
    act  = Act.TEESHOT1
    #robo = Robo()


    @classmethod  
    def start(self):

        act = self.act
        #robo = self.robo
        

        motion = Motion()
        
       
        #=======================================================#
        #                      1. Teeshot                       #         
        #=======================================================#
        
        if act == Act.TEESHOT1:                 ##### 1. 시작 및 티샷 #################
            print("ACT: ", act) # Debug
            time.sleep(2)
            print("controller")
            motion.walk_side('LEFT10')
            time.sleep(1)
            #receiving_exit = 0
            return True

       