def read_settings_from_file(file_path):
    settings = []
    with open(file_path, 'r') as file:
        for line in file:
            values = [int(val) for val in line.strip().split(',')]
            settings.append(values)
    return settings

def yuv_to_hsv(y, u, v):
    # YUV to RGB 변환 공식
    r = y + 1.402 * (v - 128)
    g = y - 0.344136 * (u - 128) - 0.714136 * (v - 128)
    b = y + 1.772 * (u - 128)

    # RGB to HSV 변환 공식
    r /= 255.0
    g /= 255.0
    b /= 255.0

    cmax = max(r, g, b)
    cmin = min(r, g, b)
    delta = cmax - cmin

    # 계산된 Hue
    if delta == 0:
        hue = 0
    elif cmax == r:
        hue = 60 * (((g - b) / delta) % 6)
    elif cmax == g:
        hue = 60 * (((b - r) / delta) + 2)
    elif cmax == b:
        hue = 60 * (((r - g) / delta) + 4)

    # 계산된 Saturation
    saturation = 0 if cmax == 0 else delta / cmax

    # 계산된 Value
    value = cmax

    return int(hue), int(saturation * 100), int(value * 100)

settings = read_settings_from_file('YUV.dat')

hsv_max_list = []
hsv_min_list = []


for setting in settings:
    color_num, y_max, y_min, u_max, u_min, v_max, v_min, min_area = setting

    # HSV 값을 RGB로 변환합니다.
    hsv_max = yuv_to_hsv(y_max, u_max, v_max)
    hsv_min = yuv_to_hsv(y_min, u_min, v_min)
    # 결과를 리스트에 추가합니다.

    hsv_max_list.append(hsv_max)
    hsv_min_list.append(hsv_min)
    
print("hsv_max: ", hsv_max_list)
print("hsv_max: ", hsv_min_list)
    