import cv2
import numpy as np

class ImageProcessing:
    def __init__(self):
        pass

    def blur(self, img, val):
            return cv2.GaussianBlur(img, (val, val), 1)

    def light(self, img, val):  # 밝기
        arr = np.full(img.shape, (val, val, val), np.uint8)
        return cv2.add(img, arr)

    def bright(self, img, alpha):  # 명도
        return np.clip((1+alpha)*img - 128*alpha, 0, 255).astype(np.uint8)

    def correction(self, img, val):
        img = self.blur(img, val)
        img = self.light(img, 0)
        img = self.bright(img, 0.0)
        return img

    def RGB2GRAY(self, img):
        return cv2.cv2.Color(img, cv2.COLOR_RGB2GRAY)

    def HSV2BGR(self, hsv):  # hsv 포맷 이미지를 파라미터로 받음
        return cv2.cv2.Color(hsv, cv2.COLOR_HSV2BGR)

    def hsv_mask(self, img):
        hsv = cv2.cv2.Color(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        _, th_s = cv2.threshold(s, 120, 255, cv2.THRESH_BINARY)
        _, th_v = cv2.threshold(v, 100, 255, cv2.THRESH_BINARY_INV)

        th_mask = cv2.bitwise_or(th_s, th_v)
        hsv = cv2.bitwise_and(hsv, hsv, mask=th_mask)
        return hsv

    def mophorlogy(self, mask):
        kernel = np.ones(
            (setting.MORPH_kernel, setting.MORPH_kernel), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        return mask

    def get_s_mask(self, hsv, s_value):
        h, s, v = cv2.split(hsv)
        ret_s, s_bin = cv2.threshold(s, s_value, 255, cv2.THRESH_BINARY)
        # morphology 연산으로 노이즈 제거
        s_bin = self.mophorlogy(s_bin)
        return s_bin

    def get_v_mask(self, hsv, v_value):
        h, s, v = cv2.split(hsv)
        ret_v, v_bin = cv2.threshold(v, v_value, 255, cv2.THRESH_BINARY)
        # morphology 연산으로 노이즈 제거
        v_bin = self.mophorlogy(v_bin)
        return v_bin

    def get_color_mask(self, hsv, const):
        lower_hue, upper_hue = np.array(const[0]), np.array(const[1])
        mask = cv2.inRange(hsv, lower_hue, upper_hue)
        return mask