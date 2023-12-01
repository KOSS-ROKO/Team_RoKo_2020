# -*- coding: utf-8 -*-

import cv2, sys
import numpy as np
import platform
import os
import time

def draw_str(dst, target, s):
    x, y = target
    cv2.putText(dst, s, (x+1, y+1), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0), thickness=1, lineType=cv2.LINE_AA)
    cv2.putText(dst, s, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)

def clock():
    return cv2.getTickCount() / cv2.getTickFrequency()

print("-------------------------------------")
print("(2020-1-15) Camera Frame check")
print("")

os_version = platform.platform()
print(" ---> OS " + os_version)

python_version = ".".join(map(str, sys.version_info[:3]))
print(" ---> Python " + python_version)

opencv_version = cv2.__version__
print(" ---> OpenCV  " + opencv_version)

W_View_size = 640
H_View_size = 480
FPS = 5

print(" ---> View Size: " + str(W_View_size) + " x " + str(H_View_size))
print(" ---> FPS: " + str(FPS))
print("-------------------------------------")  

if not os.path.exists("VIDEO"):
    os.makedirs("VIDEO")

# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# video_filename = "VIDEO/" + time.strftime('%Y-%m-%d_%H-%M-%S') + ".avi"
# out = cv2.VideoWriter(video_filename, fourcc, FPS, (W_View_size, H_View_size))

cap = cv2.VideoCapture(0)
cap.set(3, W_View_size)
cap.set(4, H_View_size)
cap.set(5, FPS)

recording = False
frame_count = 0

old_time = clock()
View_select = 1

while True:
    ret, img = cap.read()
    if not ret:
        break

    Frame_time = 1000 / ((clock() - old_time) * 1000.)
    old_time = clock()

    if View_select == 1:
        center_x = W_View_size // 2
        center_y = H_View_size // 2
        
        # Draw a crosshair at the center
        cv2.line(img, (0, center_y), (480, center_y), (0, 255, 0), 2)
        cv2.line(img, (center_x, 0), (center_x, 640), (0, 255, 0), 2)
        
        draw_str(img, (5, 20), str(W_View_size) + " x " + str(H_View_size) + ' = FPS %.1f ' % (Frame_time))
        cv2.imshow('Video Test', img)
    else:
        print(" " + str(W_View_size) + " x " + str(H_View_size) + " = FPS %.1f " % (Frame_time))

    key = 0xFF & cv2.waitKey(1)
    if key == 27:
        break
    elif key == ord(' '):
        if not recording:
            recording = True
            frame_count = 0
            # video_filename = "VIDEO/" + time.strftime('%Y-%m-%d_%H-%M-%S') + ".avi"
            # out = cv2.VideoWriter(video_filename, fourcc, FPS, (W_View_size, H_View_size))
        else:
            recording = False
            # out.release()

    if recording:
        frame_count += 1
        # out.write(img)

    if key == ord('0'):
        img_filename = "Images/" + time.strftime('%Y-%m-%d_%H-%M-%S') + ".jpg"
        # cv2.imwrite(img_filename, img)
        # print("dlalwl wjwkdehla!!")

cap.release()
if recording:
    pass
    # out.release()
cv2.destroyAllWindows()
