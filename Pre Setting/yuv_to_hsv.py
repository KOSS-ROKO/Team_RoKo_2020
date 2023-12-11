import numpy as np
import cv2

def read_settings_from_file(file_path):
    settings = []
    with open(file_path, 'r') as file:
        for line in file:
            values = [int(val) for val in line.strip().split(',')]
            settings.append(values)
    return settings

def rgb_to_hsv(r, g, b):
  r /= 255
  g /= 255
  b /= 255
  maxc = max(r, g, b)
  minc = min(r, g, b)
  v = maxc
  if minc == maxc:
      return 0.0, 0.0, v
  s = (maxc-minc) / maxc
  rc = (maxc-r) / (maxc-minc)
  gc = (maxc-g) / (maxc-minc)
  bc = (maxc-b) / (maxc-minc)
  if r == maxc:
      h = 0.0+bc-gc
  elif g == maxc:
      h = 2.0+rc-bc
  else:
      h = 4.0+gc-rc
  h = (h/6.0) % 1.0
  return h * 360, s * 100, v * 100

def yuv_to_hsv(yuv_list):
    y, u, v = yuv_list

    b = y + 1.402 * (v - 128)
    g = y - 0.344136 * (u - 128) - 0.714136 * (v - 128)
    r = y + 1.772 * (u - 128)

    # BGR 값을 0에서 255 사이로 클립하고 정수형으로 변환
    bgr = np.clip(np.array([b, g, r]), 0, 255).astype(np.uint8)

    # BGR를 HSV로 변환
    hsv = cv2.cvtColor(np.array([[bgr]]), cv2.COLOR_BGR2HSV)[0][0]
    hsv = hsv/ 2
    hsv = hsv.astype(int)

    return hsv

settings = read_settings_from_file('YUV.dat')

hsv_max_list = []
hsv_min_list = []


for setting in settings:
    color_num, y_max, y_min, u_max, u_min, v_max, v_min, min_area = setting

    yuv_max = [y_max, u_max, v_max]
    yuv_min = [y_min, u_min, v_min]

    # HSV 값을 RGB로 변환합니다.
    hsv_max = yuv_to_hsv(yuv_max)
    hsv_min = yuv_to_hsv(yuv_min)
    # 결과를 리스트에 추가합니다.

    hsv_max_list.append(hsv_max)
    hsv_min_list.append(hsv_min)
    
print("hsv_max:", [arr.tolist() for arr in hsv_max_list])
print("hsv_min:", [arr.tolist() for arr in hsv_min_list])