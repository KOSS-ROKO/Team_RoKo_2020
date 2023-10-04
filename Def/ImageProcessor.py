# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as np
import os
import time
import platform
from imutils.video import WebcamVideoStream
from imutils.video import FileVideoStream
from imutils.video import FPS

import warnings
warnings.simplefilter(
    action='ignore', category=FutureWarning)  # FutureWarning 제거

print('code: ImageProcessor.py - ## Debug')


if __name__ == "__main__":
    from Line import Line
    from Stair import Stair  # 파일명 / class이름
    from Arrow import Arrow
    from Direction import Direction
    from Danger import Danger

    from Stair import Stair
    from Setting import setting
    from DataPath import DataPath

    e_ = [cv.imread('{}sam_e0{}.png'.format(DataPath.d_dirimg, x),
                    cv.IMREAD_GRAYSCALE) for x in range(1, 6)]
    w_ = [cv.imread('{}sam_w0{}.png'.format(DataPath.d_dirimg, x),
                    cv.IMREAD_GRAYSCALE) for x in range(1, 6)]
    n_ = [cv.imread('{}sam_s0{}.png'.format(DataPath.d_dirimg, x),
                    cv.IMREAD_GRAYSCALE) for x in range(1, 6)]
    s_ = [cv.imread('{}sam_n0{}.png'.format(DataPath.d_dirimg, x),
                    cv.IMREAD_GRAYSCALE) for x in range(1, 6)]
    font_img = [cv.imread('{}/{}.jpg'.format(DataPath.d_dirfont, x),
                          cv.IMREAD_GRAYSCALE) for x in range(4)]
    font_danger = [cv.imread('{}/{}.jpg'.format(DataPath.d_dangerfont, x),
                          cv.IMREAD_GRAYSCALE) for x in range(4)]
    arr_a = [cv.imread('{}a{}.png'.format(DataPath.d_alpha, x),
                       cv.IMREAD_GRAYSCALE) for x in range(4)]
    arr_b = [cv.imread('{}b{}.png'.format(DataPath.d_alpha, x),
                       cv.IMREAD_GRAYSCALE) for x in range(4)]
    arr_c = [cv.imread('{}c{}.png'.format(DataPath.d_alpha, x),
                       cv.IMREAD_GRAYSCALE) for x in range(4)]
    arr_d = [cv.imread('{}d{}.png'.format(DataPath.d_alpha, x),
                       cv.IMREAD_GRAYSCALE) for x in range(4)]

else:
    from Sensor.Stair import Stair
    from Sensor.Line import Line
    from Sensor.Arrow import Arrow
    from Sensor.Direction import Direction

    from Sensor.Danger import Danger
    from Sensor.Stair import Stair
    from Sensor.Setting import setting
    from Sensor.DataPath import DataPath

    e_ = [cv.imread('{}sam_e0{}.png'.format(DataPath.r_dirimg, x),
                    cv.IMREAD_GRAYSCALE) for x in range(1, 6)]
    w_ = [cv.imread('{}sam_w0{}.png'.format(DataPath.r_dirimg, x),
                    cv.IMREAD_GRAYSCALE) for x in range(1, 6)]
    n_ = [cv.imread('{}sam_s0{}.png'.format(DataPath.r_dirimg, x),
                    cv.IMREAD_GRAYSCALE) for x in range(1, 6)]
    s_ = [cv.imread('{}sam_n0{}.png'.format(DataPath.r_dirimg, x),
                    cv.IMREAD_GRAYSCALE) for x in range(1, 6)]
    font_img = [cv.imread('{}/{}.jpg'.format(DataPath.r_dirfont, x),
                          cv.IMREAD_GRAYSCALE) for x in range(4)]
    font_danger = [cv.imread('{}/{}.jpg'.format(DataPath.r_dangerfont, x),
                          cv.IMREAD_GRAYSCALE) for x in range(4)]
    arr_a = [cv.imread('{}a{}.png'.format(DataPath.r_alpha, x),
                       cv.IMREAD_GRAYSCALE) for x in range(4)]
    arr_b = [cv.imread('{}b{}.png'.format(DataPath.r_alpha, x),
                       cv.IMREAD_GRAYSCALE) for x in range(4)]
    arr_c = [cv.imread('{}c{}.png'.format(DataPath.r_alpha, x),
                       cv.IMREAD_GRAYSCALE) for x in range(4)]
    arr_d = [cv.imread('{}d{}.png'.format(DataPath.r_alpha, x),
                       cv.IMREAD_GRAYSCALE) for x in range(4)]


class ImageProccessor:
    def __init__(self, video: str = ""):
        print("init_imgprocessor")

        if video and os.path.exists(video):
            self._cam = FileVideoStream(path=video).start()
        else:
            print('# image processor #', platform.system())
            if platform.system() == "Linux":
                print('eee')
                self._cam = WebcamVideoStream(src=-1).start()
            else:
                self._cam = WebcamVideoStream(src=0).start()
            print('Acquire Camera ')

        self.fps = FPS()  # FPS
        print(self.fps)  # debuging: fps
        shape = (self.height, self.width, _) = self.get_img().shape
        print("Shape :: ", shape)  # debuging: image shape => height, width
        time.sleep(2)

    ########### 이미지 불러오기 ###########
    def get_img(self, show=False):
        img = self._cam.read()
        # 이미지를 받아오지 못하면 종료
        if img is None:
            exit()

        # 이미지를 받아오면 화면에 띄움
        if show:
            cv.imshow("imageProcessor-get_img", img)
            cv.waitKey(1)
        return img

    ########### 기본 공용 함수 ###########
    def blur(self, img, val):
        return cv.GaussianBlur(img, (val, val), 1)

    def light(self, img, val):  # 밝기
        arr = np.full(img.shape, (val, val, val), np.uint8)
        return cv.add(img, arr)

    def bright(self, img, alpha):  # 명도
        return np.clip((1+alpha)*img - 128*alpha, 0, 255).astype(np.uint8)

    def correction(self, img, val):
        img = self.blur(img, val)
        img = self.light(img, 0)
        img = self.bright(img, 0.0)
        return img

    def RGB2GRAY(self, img):
        return cv.cvtColor(img, cv.COLOR_RGB2GRAY)

    def HSV2BGR(self, hsv):  # hsv 포맷 이미지를 파라미터로 받음
        return cv.cvtColor(hsv, cv.COLOR_HSV2BGR)

    def hsv_mask(self, img):
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        h, s, v = cv.split(hsv)

        _, th_s = cv.threshold(s, 120, 255, cv.THRESH_BINARY)
        _, th_v = cv.threshold(v, 100, 255, cv.THRESH_BINARY_INV)

        th_mask = cv.bitwise_or(th_s, th_v)
        hsv = cv.bitwise_and(hsv, hsv, mask=th_mask)
        return hsv

    def mophorlogy(self, mask):
        kernel = np.ones(
            (setting.MORPH_kernel, setting.MORPH_kernel), np.uint8)
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
        return mask

    def get_s_mask(self, hsv, s_value):
        h, s, v = cv.split(hsv)
        ret_s, s_bin = cv.threshold(s, s_value, 255, cv.THRESH_BINARY)
        # morphology 연산으로 노이즈 제거
        s_bin = self.mophorlogy(s_bin)
        return s_bin

    def get_v_mask(self, hsv, v_value):
        h, s, v = cv.split(hsv)
        ret_v, v_bin = cv.threshold(v, v_value, 255, cv.THRESH_BINARY)
        # morphology 연산으로 노이즈 제거
        v_bin = self.mophorlogy(v_bin)
        return v_bin

    def get_color_mask(self, hsv, const):
        lower_hue, upper_hue = np.array(const[0]), np.array(const[1])
        mask = cv.inRange(hsv, lower_hue, upper_hue)
        return mask

    #######################################

    ########### LINE DETECTION ###########
    # 라인이 수평선인지 수직선인지 return해줌

    def is_line_horizon_vertical(self, show=False):
        img = self.get_img()
        origin = img.copy()
        img = self.correction(img, 7)
        hsv = self.hsv_mask(img)
        line_mask = Line.yellow_mask(self, hsv, setting.YELLOW_DATA)
        line_mask = self.HSV2BGR(line_mask)
        line_gray = self.RGB2GRAY(line_mask)

        if show:
            cv.imshow("tmp", line_mask)
            cv.waitKey(1) & 0xFF == ord('q')

        roi_img = Line.ROI(self, line_gray, self.height, self.width, origin)

        # get Line
        line_arr = Line.hough_lines(
            self, roi_img, 1, 1 * np.pi/180, 30, 10, 20)   # 허프 변환
        line_arr = np.squeeze(line_arr)
        # print(line_arr)
        if show:
            cv.imshow("show", origin)
            cv.waitKey(1) & 0xFF == ord('q')
        if line_arr != 'None':
            Line.draw_lines(self, origin, line_arr, [0, 0, 255], 2)
            # if show:
            #     cv.imshow("tmp", origin)
            #     cv.waitKey(1) & 0xFF == ord('q')

            state, horizon_arr, vertical_arr = Line.slope_filter(
                self, line_arr)
            h_line, v_line = Line.get_fitline(
                self, origin, horizon_arr), Line.get_fitline(self, origin, vertical_arr)

            # init
            v_slope = None
            h_slope = None

            if v_line:
                Line.draw_fitline(self, origin, v_line, [0, 255, 255])  # Debug
                v_slope = int(Line.slope_cal(self, v_line))
            if h_line:
                Line.draw_fitline(self, origin, h_line, [0, 255, 0])  # Debug
                h_slope = int(Line.slope_cal(self, h_line))

            # print(v_slope, h_slope)

            cv.putText(origin, "state: {}".format(state), (50, 210),
                       cv.FONT_HERSHEY_SIMPLEX, 1, [255, 255, 0], 2)
            cv.putText(origin, "v_slope: {}".format(v_slope),
                       (50, 100), cv.FONT_HERSHEY_SIMPLEX, 0.5, [0, 0, 0], 2)
            cv.putText(origin, "h_slope: {}".format(h_slope),
                       (50, 130), cv.FONT_HERSHEY_SIMPLEX, 0.5, [0, 0, 0], 2)
            ########### [Option] Show ##########
            if show:
                cv.imshow("show", origin)
                cv.waitKey(1) & 0xFF == ord('q')

            ####################################
            print(state, v_slope)
            if state == "BOTH":
                # is_center = Line.is_center(self, origin, v_line)
                # cv.putText(origin, "center: {}".format(is_center), (260, 80), cv.FONT_HERSHEY_SIMPLEX, 0.8, [0,255,100], 2)
                # if is_center != True:
                # return is_center
                if v_slope and not h_slope:  # vertical
                    if 90 - v_slope < 0:
                        cv.putText(origin, "motion: {}".format(
                            "TURN_RIGHT"), (100, 50), cv.FONT_HERSHEY_SIMPLEX, 1, [0, 255, 255], 2)
                        return "TURN_RIGHT"
                    else:
                        cv.putText(origin, "motion: {}".format(
                            "TURN_LEFT"), (100, 50), cv.FONT_HERSHEY_SIMPLEX, 1, [0, 255, 255], 2)
                        return "TURN_LEFT"
                elif h_slope and not v_slope:  # horizon
                    if h_slope < 90:
                        cv.putText(origin, "motion: {}".format(
                            "TURN_RIGHT"), (100, 50), cv.FONT_HERSHEY_SIMPLEX, 1, [0, 255, 255], 2)
                        return "TURN_RIGHT"
                    else:
                        cv.putText(origin, "motion: {}".format(
                            "TURN_LEFT"), (100, 50), cv.FONT_HERSHEY_SIMPLEX, 1, [0, 255, 255], 2)
                        return "TURN_LEFT"
                else:  # 선이 둘 다 인식됨
                    return state
            elif state == "VERTICAL" and v_line:
                print('******', setting.VSLOPE1, '******')
                is_center = Line.is_center(self, origin, v_line)
                # cv.putText(origin, "center: {}".format(is_center), (260, 80), cv.FONT_HERSHEY_SIMPLEX, 0.8, [0,255,100], 2)
                if is_center != True:
                    return is_center
                # if 88 < v_slope < 96:  # 수직
                if setting.VSLOPE1 <= v_slope <= setting.VSLOPE2:  # 수직
                    return state
                elif v_slope < setting.VSLOPE1:
                    # cv.putText(origin, "motion: {}".format("TURN_LEFT"), (100, 50), cv.FONT_HERSHEY_SIMPLEX, 1, [0,255,255], 2)
                    print(setting.VSLOPE1, "turn left turn left")
                    return "TURN_LEFT"
                elif setting.VSLOPE2 < v_slope:
                    # cv.putText(origin, "motion: {}".format("TURN_RIGHT"), (100, 50), cv.FONT_HERSHEY_SIMPLEX, 1, [0,255,255], 2)
                    return "TURN_RIGHT"
            elif state == "HORIZON" and h_line:
                if h_slope < 10 or 170 < h_slope:
                    return state
                if h_slope < 90:
                    # cv.putText(origin, "motion: {}".format("TURN_RIGHT"), (100, 50), cv.FONT_HERSHEY_SIMPLEX, 1, [0,255,255], 2)
                    return "TURN_RIGHT"
                else:
                    # cv.putText(origin, "motion: {}".format("TURN_LEFT"), (100, 50), cv.FONT_HERSHEY_SIMPLEX, 1, [0,255,255], 2)
                    return "TURN_LEFT"
            else:
                print("ELSE", state)
                # 예외처리 추가 데이터 필요

        else:  # 라인 자체를 인식 못할 경우 False 리턴
            print("FALSE")
            return False

    def black_line(self, show=False):
        img = self.get_img()
        origin = img.copy()
        img = self.correction(img, 7)
        img = self.RGB2GRAY(img)
        _, th = cv.threshold(img, 0, 255, cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
        edges = cv.Canny(th, 500, 700, apertureSize=3)

        roi_img = Line.ROI(self, edges, self.height,
                           self.width, origin, c="BLACK")

        # get Line
        line_arr = Line.hough_lines(self, roi_img)   # 허프 변환
        line_arr = np.squeeze(line_arr)
        v_slope = None
        h_slope = None
        if line_arr != 'None':
            Line.draw_lines(self, origin, line_arr, [0, 0, 255], 2)
            state, horizon_arr, vertical_arr = Line.slope_filter(
                self, line_arr, black=True)
            h_line, v_line = Line.get_black_fitline(
                self, origin, horizon_arr), Line.get_black_fitline(self, origin, vertical_arr)
            if v_line:
                Line.draw_fitline(self, origin, v_line, [0, 255, 255])  # Debug
                v_slope = abs(int(Line.slope_cal(self, v_line)))
            if h_line:
                Line.draw_fitline(self, origin, h_line, [0, 255, 0])  # Debug
                h_slope = abs(int(Line.slope_cal(self, h_line)))
            # print(state, v_slope, h_slope)

            if show:
                cv.imshow("show", origin)
                cv.waitKey(1) & 0xFF == ord('q')
            if show:
                cv.imshow("tmp", th)
                cv.waitKey(1) & 0xFF == ord('q')

            if h_slope:
                print(h_slope)
                if h_slope <= 10 or 170 <= h_slope:
                    return True
                if h_slope < 90:
                    # cv.putText(origin, "motion: {}".format("TURN_RIGHT"), (100, 50), cv.FONT_HERSHEY_SIMPLEX, 1, [0,255,255], 2)
                    print("TURN_RIGHT")
                    return "TURN_RIGHT"
                else:
                    # cv.putText(origin, "motion: {}".format("TURN_LEFT"), (100, 50), cv.FONT_HERSHEY_SIMPLEX, 1, [0,255,255], 2)
                    print("TURN_LEFT")
                    return "TURN_LEFT"
        print('FalseFlase')
        return False

    def is_yellow(self, show=False):
        img = self.get_img()
        origin = img.copy()
        img = self.correction(img, 7)
        hsv = self.hsv_mask(img)
        line_mask = Line.yellow_mask(self, hsv, setting.YELLOW_DATA)
        line_mask = self.HSV2BGR(line_mask)
        line_gray = self.RGB2GRAY(line_mask)
        # vertices = np.array([[(0,self.height-50),(0, self.height/2+50), (self.width, self.height/2+50), (self.width,self.height-50)]], dtype=np.int32)
        # mask = np.zeros_like(img)
        # cv.fillPoly(mask, vertices, 255)
        # roi_img = cv.bitwise_and(img, mask)

        # roi_img = Line.ROI(self, line_gray, self.height, self.width, origin)

        # line_arr = Line.hough_lines(self, roi_img)   # 허프 변환
        line_arr = Line.hough_lines(self, line_gray)   # 허프 변환
        line_arr = np.squeeze(line_arr)
        # print(line_arr)
        if show:
            cv.imshow("show", origin)
            cv.imshow("tmp", line_mask)
            cv.waitKey(1) & 0xFF == ord('q')
        if line_arr != 'None':
            print('T')
            # self.is_line_horizon_vertical()
            state, horizon_arr, vertical_arr = Line.slope_filter(
                self, line_arr, black=True)
            h_line, v_line = Line.get_black_fitline(
                self, origin, horizon_arr), Line.get_black_fitline(self, origin, vertical_arr)
            v_slope, h_slope = None, None
            if v_line:
                Line.draw_fitline(self, origin, v_line, [0, 255, 255])  # Debug
                v_slope = abs(int(Line.slope_cal(self, v_line)))
            if h_line:
                Line.draw_fitline(self, origin, h_line, [0, 255, 0])  # Debug
                h_slope = abs(int(Line.slope_cal(self, h_line)))
            print(state, v_slope, h_slope)
            return state, h_slope
            # return True
        else:
            print('F')
            return "None", None
    
    def is_yellow_danger(self, show=False):
        img = self.get_img()
        origin = img.copy()
        img = self.correction(img, 7)
        hsv = self.hsv_mask(img)
        line_mask = Line.yellow_mask(self, hsv, setting.YELLOW_DATA)
        line_mask = self.HSV2BGR(line_mask)
        line_gray = self.RGB2GRAY(line_mask)
        # vertices = np.array([[(0,self.height-50),(0, self.height/2+50), (self.width, self.height/2+50), (self.width,self.height-50)]], dtype=np.int32)
        # mask = np.zeros_like(img)
        # cv.fillPoly(mask, vertices, 255)
        # roi_img = cv.bitwise_and(img, mask)

        # roi_img = Line.ROI(self, line_gray, self.height, self.width, origin)

        # line_arr = Line.hough_lines(self, roi_img)   # 허프 변환
        line_arr = Line.hough_lines(self, line_gray)   # 허프 변환
        line_arr = np.squeeze(line_arr)
        # print(line_arr)
        # if show:
        #     cv.imshow("show", origin)
        #     cv.imshow("tmp", line_mask)
        #     cv.waitKey(1) & 0xFF == ord('q')
        if line_arr != 'None':
            print('T')
            
            return True
        else:
            print('F')
            return False


    ########### ENTRANCE PROCESSING ###########
    # 화살표 방향 인식 후 리턴

    def get_arrow(self, show=False):
        img = self.get_img()
        origin = img.copy()

        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img = self.blur(img, setting.ARROW_BLUR)
        img = self.bright(img, setting.ARROW_BRIGHT)
        _, img = cv.threshold(img, 0, 255, cv.THRESH_BINARY_INV+cv.THRESH_OTSU)

        ret = Arrow.get_arrow_info(self, img, origin)
        ########### [Option] Show ##########
        if show:
            cv.imshow("show", img)
            cv.waitKey(1) & 0xFF == ord('q')
        ####################################

        if not ret:
            _, img = cv.threshold(img, 0, 255, cv.THRESH_BINARY_INV)
            ret = Arrow.get_arrow_info(self, img, origin)

        print(ret)  # Debug: print arrow
        return ret

    # 방위 글자 인식 후 방위 리턴
    def get_ewsn(self, show=False):
        print('get_ewsn')
        img = self.get_img()
        x, y, w, h = 100, 100, 440, 480
        img = img[y:y+h, x:x+w]

        origin = img.copy()
        dir = Direction
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        dst = self.blur(gray, setting.DIR_BLUR)

        _, th = cv.threshold(dst, 0, 255, cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
        dst = cv.bitwise_and(img, img, mask=th)

        kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, 1))
        dst = cv.dilate(dst, kernel, iterations=1)

        contours, hierarchy = cv.findContours(
            th,  cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

        roi_contour = []
        for pos in range(len(contours)):
            peri = cv.arcLength(contours[pos], True)
            approx = cv.approxPolyDP(contours[pos], peri * 0.02, True)
            points = len(approx)
            if peri > 900 and points == 4:
                roi_contour.append(contours[pos])
                # cv.drawContours(img, [approx], 0, (0, 255, 255), 1) # Debug: Drawing Contours

        if show:
            cv.imshow("show", dst)
            cv.waitKey(1) & 0xFF == ord('q')
        ####################################
        roi_contour_pos = []
        for pos in range(len(roi_contour)):
            area = cv.contourArea(roi_contour[pos])
            print(area)
            if area > 20000:
                roi_contour_pos.append(pos)

        if roi_contour:
            x, y, w, h = cv.boundingRect(roi_contour[0])
            img_crop = origin[y:y+h, x:x+w]
            text_gray = cv.cvtColor(img_crop, cv.COLOR_BGR2GRAY)
            text = img_crop.copy()

            '''
            [Issue]
            현재 mt_gray(gray처리된 roi 부분을 matchTemplate 비교)값을 대표로 리턴함.
            mt_gray, mt_mask가 정확도가 가장 높으며 두 값은 항상 유사한 결과를 가짐.
            font 이미지와 비교한 2가지 값도 정확도가 낮지는 않으나, 가끔 로봇의 고개 각도에 따라 튀는 값이 나올 때가 있음
            '''

            sample_list = [e_, w_, s_, n_]
            # 1. matchTemplate - Gray Scale
            mt_gray = Direction.matching(sample_list, text_gray, 0.001, "EWSN")
            text_mask = Direction.text_masking(text)
            # 2. matchTemplate - Masking
            mt_mask = Direction.matching(sample_list, text_mask, 1, "EWSN")
            match_mask_font = Direction.match_font(
                font_img, text_mask)  # 3. font <-> masking
            match_gray_font = Direction.match_font(
                font_img, text_gray)  # 4. font <-> gray scale

            print('match: ', mt_gray, mt_mask, match_gray_font,
                  match_mask_font)  # Debug: printing
            set_ = {mt_gray, mt_mask, match_mask_font, match_gray_font}
            print(list(set_), list(set_)[0])
            ########### [Option] Show ##########
            if show:
                cv.imshow("show", img)
                cv.imshow("showw", img_crop)
                cv.waitKey(1) & 0xFF == ord('q')
            ####################################
            if len(set_) <= 2:
                cv.putText(img, "direction: {}".format(match_mask_font),
                           (100, 250), cv.FONT_HERSHEY_SIMPLEX, 1, [0, 255, 255], 2)
                ########### [Option] Show ##########
                if show:
                    cv.imshow("show", img)
                    # cv.imshow("show", img_crop)
                    cv.waitKey(1) & 0xFF == ord('q')
                ####################################
                return match_gray_font
            else:
                return ''
        else:  # False
            return ''

    ############ DANGER PROCESSING #############
    # 계단 지역인지(False) 위험 지역인지(True) detection

    def is_danger(self, show=False):
        img = self.get_img()
        img = self.bright(img, 2.0) 
        return Danger.is_danger(img, show)  # [return] DANGER / STAIR

    # 방 이름이 적힌 글자(A, B, C, D)의 색상 판단
    def get_alphabet_color(self):
        img = self.get_img()
        hsv = Danger.get_alphabet_roi(img)
        if hsv == "Failed":
            print("get_alphabet_color 실패")
            return False
        else:
            return Danger.get_alphabet_color(hsv)  # [return] RED / BLUE

    # 방 이름(알파벳) 인식
    def get_alphabet_name(self, show=False):
        img = self.get_img()

        roi = Danger.get_alphabet_roi(img, "GRAY")
        # roi = self.bright(roi,1.0)

        arr = [arr_a, arr_b, arr_c, arr_d]
        if roi != "Failed":
            roi_gray = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
            
            mt_gray = Direction.matching(arr, roi_gray, 0.001, "ABCD")
            text_mask = Direction.text_masking(roi)
            match_font = Direction.match_font(font_danger, text_mask, danger=True)
            match_fontg = Direction.match_font(font_danger, roi_gray, danger=True)

            print(mt_gray, match_font, match_fontg)
            ########### [Option] Show ##########
            if show:
                cv.imshow("show", text_mask)
                cv.imshow("show2", roi)
            ####################################
            # return mt_gray  # [return] 인식한 알파벳: A, B, C, D
            # return match_font  # [return] 인식한 알파벳: A, B, C, D
            return match_fontg  # [return] 인식한 알파벳: A, B, C, D
        print("get_alphabet_name 실패")
        return False  # 인식 실패

    # 장애물 들고 위험 지역에서 벗어났는지 확인 (show : imshow() 해줄 건지에 대한 여부)
    def is_out_of_black(self, show=False):
        img = self.get_img()
        # light보다 bright가 효과가 좋아서 추가해둠
        img = self.light(img, 0)  # 1128 hyerin
        img = self.bright(img, 3.0)  # 1128 hyerin
        return Danger.is_out_of_black(img, show)  # [return] T/F

    # 장애물을 떨어트리지 않고 여전히 들고 있는 지에 대한 체크
    def is_holding_milkbox(self, color, show=False):
        img = self.get_img()
        return Danger.is_holding_milkbox(img, color, show)  # [return] T/F

    # 장애물 위치 파악을 위한 함수
    def get_milkbox_pos(self, color, show=False):
        img = self.get_img()
        # [return] 0 ~ 8 (장애물 위치 idx 값)
        return Danger.get_milkbox_pos(img, color, show)

    # 장애물 집을 지 말 지 결정하는 함수 (7번 위치에서 충분히 가까운지)
    def can_hold_milkbox(self, color):
        img = self.get_img()
        return Danger.can_hold_milkbox(img, color)

    # 장애물 집을 지 말 지 결정하는 함수 (7번 위치에서 충분히 가까운지)
    def get_milkbox_mask(self, color):
        img = self.get_img()
        # cv.imshow('img',  img)
        img = self.correction(img, 7)
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        return Danger.get_milkbox_mask(hsv, color)

    ############# DANGER PROCESSING #############

    ############# STAIR PROCESSING #############
    # 로봇의 회전 완료 여부 반환
    # 알파벳 크기 측정 후 계단 지역으로 회전, 화살표 반대 방향.
    def first_rotation(self, Arrow):
        img = self.get_img()
        img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        s_mask = Stair.in_saturation_measurement(
            self, img, setting.STAIR_S, setting.ROOM_V)
        print(s_mask)
        cur_s_val = Stair.in_left_right(
            self, s_mask, Arrow)  # (Current_saturation_value)
        print(cur_s_val)
        ret = Stair.in_rotation(
            self, cur_s_val, setting.ALPHABET_ROTATION, Arrow)
        '''motion
        # T: (회전완료) 머리 아래 30도 변경
        # False 일 때는 LEFT, RIGHT 반환
        # LEFT: 왼쪽으로 회전, RIGHT: 오른쪽으로 회전
        '''
        return ret

    def second_rotation(self, Arrow, k):  # 계단 지역일 때 계단 쪽으로 도는 함수, 화살표 방향.
        img = self.get_img()
        img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        s_mask = Stair.in_saturation_measurement(
            self, img, setting.STAIR_S, setting.ROOM_V)

        s_val = int((np.count_nonzero(s_mask) / (640 * 480)) * 1000)
        print('채도{},세팅값{}'.format(s_val, setting.top_saturation))

        ret = Stair.in_rotation(self, k, s_val, Arrow)

        '''motion
        # T: (회전완료) 머리 아래 30도 변경
        # LEFT: 왼쪽으로 회전
        # RIGHT: 오른쪽으로 회전
        '''
        # print("stair_to_alphabet_rotation", ret) # Debug
        return ret

    def rect(self):
        img = self.get_img()
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        blur = cv.GaussianBlur(img_gray, (9, 9), 0)
        add = cv.add(blur, 0)
        alpha = 0.0
        dst = np.clip((1 + alpha) * add - 128 * alpha, 0, 255).astype(np.uint8)

        ret, th = cv.threshold(
            dst, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
        dst = cv.bitwise_or(dst, dst, mask=th)

        kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
        dst = cv.dilate(dst, kernel, iterations=1)

        contours, hierarchy = cv.findContours(
            dst, cv.RETR_LIST, cv.CHAIN_APPROX_TC89_L1)
        return contours

    def alphabet_center_check(self, show=False):
        img = self.get_img()

        if show:
            cv.imshow("show", img)
            cv.waitKey(1) & 0xFF == ord('q')

        contours = self.rect()
        try:
            alphabet_area, rect_x = Stair.in_rect(
                self, img, contours)  # contours를 리턴값으로 해서 함수 구성 다시 해보기
            # print(alphabet_area,rect_x)
            is_center = Stair.in_alphabet_center_check(self, rect_x)

            if is_center == True:  # [return] True
                sz_check = Stair.in_alphabet_size_calc(
                    self, alphabet_area, setting.STAIR_ALPHABET_SIZE)

                '''motion
                # T: second 회전
                # F: 전진
                '''
                return sz_check
            else:  # [return] (LEFT,걸음 수), (RIGHT, 걸음 수)
                '''motion
                # LEFT: 왼쪽으로 이동
                # RIGHT: 오른쪽으로 이동 '''
                return is_center
        except:
            return 'fail'

    def stair_top(self):
        img = self.get_img()
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        lower_hue, upper_hue = np.array(
            setting.STAIR_BLUE[0]), np.array(setting.STAIR_BLUE[1])
        b_mask = Stair.in_stair_top(
            self, hsv, lower_hue, upper_hue)  # roi blue mask
        top_ret = int((np.count_nonzero(b_mask) / (640 * 480)) * 1000)

        if top_ret >= setting.STAIR_UP:
            ''' motion
            cnt = 2
            2층->3층 올라가기
            샤샤샥 

            cnt = 3
            잘 올라갔는지 판단
            '''
            # stair_stage_check는 외부에서 계단 올라간거 체크하는 변수 만들어야 함.
            if int(setting.STAIR_LEVEL) < 3:
                print("2층입니다. 올라가세요")
                setting.STAIR_LEVEL = 3
                return True  # 올라가라
            elif int(setting.STAIR_LEVEL) >= 3:
                print("정상 도달")
                return 'Top'
        else:
            print("1층에서 좁은 보폭")  # motion: 2층에서 샤샤샥
            return False

    # 계단 내려가기 전에 파란색이 더 많은 부분 발이 먼저 내려가기
    # 넘어졌을 때 cnt

    # 계단 내려가기

    def stair_down(self):
        img = self.get_img()
        img = cv.cvtColor(img, cv.COLOR_RGB2HSV)
        img_mask = Stair.in_saturation_measurement(
            self, img, setting.STAIR_S, setting.ROOM_V)  # -->s_mask가 50 이면 좋겠어
        ''' motion 
        # T: 방 탈출
        # F: 계단 내려가기 '''
        return Stair.in_stair_down(self, img_mask, setting.ONE_F, setting.TWO_F, setting.THREE_F)

    # 허프라인 잡히면 2층으로 올라가기
    def draw_stair_line(self):
        img = self.get_img()
        x, y, w, h = 0, 200, 640, 200
        # x=0; y=200; w = 640; h = 200  # 계단 영역 ROI지정
        roi = img[y:y+h, x:x+w]
        img_canny = cv.Canny(roi, 20, 200)
        # try:

        lines = cv.HoughLines(img_canny, 0.8, np.pi/20,
                              100, min_theta=0, max_theta=50)

        if lines is not None:
            line_length = lines[0][0][1]
            if line_length >= 1 and line_length <= 2:  # 허프라인 짧은 노이즈 직선 제거
                # bool(T/F)
                ''' motion 
                # T: 1층 -> 2층 계단 올라가기 + 샤샤샥 -> draw_stair_line() 재실행
                # F: 샤샤샥 '''
                if Stair.in_draw_stair_line(self, lines, img, w, h, setting.LINE_HIGH):
                    setting.STAIR_LEVEL = 1
                return Stair.in_draw_stair_line(self, lines, img, w, h, setting.LINE_HIGH)
            else:
                return False  # 라인 추출 실패
        else:
            return self.stair_top()

    def top_processing(self):  # stair07~stair11
        img = self.get_img()
        img = cv.cvtColor(img, cv.COLOR_RGB2HSV)
        x, y, w, h = 250, 0, 390, 480
        img = img[y:y+h, x:x+w]
        mask = Stair.in_saturation_measurement(
            self, img, setting.STAIR_S, setting.ROOM_V)
        return Stair.in_top_processing(self, mask, setting.top_forward)

    def close_to_descent(self):
        img = self.get_img()
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        lower_hue, upper_hue = np.array(
            setting.STAIR_BLUE[0]), np.array(setting.STAIR_BLUE[1])
        b_mask = Stair.in_stair_top(
            self, hsv, lower_hue, upper_hue)  # blue mask

        top_ret = int((np.count_nonzero(b_mask) / (640 * 480)) * 1000)

        x = 270
        y = 150
        left_m = int(
            (np.count_nonzero(b_mask[y:y+480, x:x+70]) / (640 * 480)) * 1000)

        x = 360
        right_m = int(
            (np.count_nonzero(b_mask[y:y+480, x:x+70]) / (640 * 480)) * 1000)

        if right_m < left_m:
            ro = 'LEFT_DOWN'
        else:
            ro = 'RIGHT_DOWN'
        print(ro)

        if top_ret <= setting.STAIR_DOWN:
            return True, ro  # 내려가라
        else:
            return False, ro  # 전진

    def wall_move(self, Arrow):  # 계단 오를 때
        img = self.get_img()
        # cv.imshow("img", img)
        img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        mask = Stair.in_saturation_measurement(
            self, img, setting.STAIR_S, setting.ROOM_V)

        if Arrow == 'LEFT':
            x = 0
            y = 0
            left = int(
                (np.count_nonzero(mask[y:y + 480, x:x + 140]) / (640 * 480)) * 1000)
            return Stair.in_rotation(self, left, setting.top_move, Arrow)
        else:
            x = 500
            y = 0
            right = int(
                (np.count_nonzero(mask[y:y + 480, x:x + 320]) / (640 * 480)) * 1000)
            # cv.imshow("right", mask[y:y + 480, x:x + 320])
            return Stair.in_rotation(self, right, setting.top_move, Arrow)

    def stair_obstacle(self):
        img = self.get_img()
        return Stair.in_stair_obstacle(self,img) #True가 나오면 치워
    ############# STAIR PROCESSING #############


if __name__ == "__main__":
    img_processor = ImageProccessor(DataPath.stair05)
    # img_processor = ImageProccessor(video=DataPath.de1)

    ### Debug Run ###
    while True:
        # img_processor.get_arrow(show=True)
        # img_processor.get_ewsn(show=True)
        # img_processor.black_line(show=True)
        # img_processor.is_yellow(show=True)

        # print(img_processor.get_alphabet_name(show=True))
        # img_processor.get_alphabet_name(show=True)
        # img_processor.get_milkbox_pos("RED", True)

        ### stair ###
        # img_processor.first_rotation('RIGHT')
        # img_processor.alphabet_center_check()
        # img_processor.second_rotation(show=True)
        img_processor.draw_stair_line()
        # img_processor.top_processing()
        # img_processor.wall_move('RIGHT')
        # img_processor.stair_down()

        # img_processor.get_milkbox_mask("BLUE")
        # img_processor.is_holding_milkbox("BLUE", True)
        # img_processor.is_out_of_black(True)

        ### danger ###
        # print(img_processor.get_alphabet_color())
        # img_processor.is_out_of_black(True)
        # img_processor.is_danger(True)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break
