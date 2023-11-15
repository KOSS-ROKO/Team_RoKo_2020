# -*- coding: utf-8 -*-

#### 전역 변수 담을 파일 ####

global _Head_UD_Middle_Value
global _Head_Length_list
global Head_UD_Middle_Value_Measures
Head_UD_Middle_Value_Measures = 100
global Head_ud_angle
global Length_Weight
global Length_ServoAngle
global Length_ServoAngle_dict

global holecup_dist
global field
field = "left"
global small_lr_angle
small_lr_angle = 100

_Head_UD_Middle_Value = 113
_Head_ServoAngle_list = [i*3+11 for i in range(30)]
#_Head_Length_list = [0.8, 1.9, 3.5, 4.4, 6.4, 7.9, 9.5, 11.2, 12.9, 14.8, 16.5, 18.1, 21.5, 24.1, 26.5, 29.8, 32.6,35,38,42,46,50,58,63,66,70,77,82,87,93]
_Head_Length_list = [0.8, 1.9, 3.5, 4.4, 6.4, 7.9, 9.5, 11.2, 12.9, 14.8, 16.5, 18.1, 21.5, 24.1, 26.5, 29.8, 32.6, 36.4, 38.3, 42.1, 46.1, 51.7, 57.6, 63.8, 71, 81, 94.3, 112, 128, 180]

Head_ud_angle = Head_UD_Middle_Value_Measures


Length_Weight = _Head_UD_Middle_Value - Head_UD_Middle_Value_Measures
Head_ServoAngle_Measures_list = [i*3+20-Length_Weight for i in range(30)]


Length_ServoAngle = list(zip(Head_ServoAngle_Measures_list, _Head_Length_list))
Length_ServoAngle_dict = dict(Length_ServoAngle)