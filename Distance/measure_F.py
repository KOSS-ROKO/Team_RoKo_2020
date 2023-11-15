import cv2
import numpy as np

def measure_focal_length(W, w, d_prime):
    # 측정을 위해 물체를 카메라로부터 d' 거리에 위치시킴
    # 이때, d' 값은 임의로 설정
    # 여기서는 임의로 50cm로 설정
    d_prime = 50

    # 초점 거리(f) 측정
    f = (w * d_prime) / W
    return f

def measure_distance(W, w, f):
    # 실제 거리(d) 측정
    d = (W * f) / w
    return d

def main():
    # 물체의 크기와 카메라 센서에 표시되는 크기를 측정
    # 이 값들은 미리 측정되어야 합니다.
    W = 4  # 물체의 실제 크기 (단위: cm)
    w = 100  # 카메라 센서에 표시되는 물체의 크기 (단위: pixel)

    # 초점 거리(f) 측정
    f = measure_focal_length(W, w, 50)  # 50cm로 설정한 임의의 거리

    print(f"측정된 초점 거리(f): {f} cm")

    # 측정한 초점 거리를 이용하여 실제 거리(d) 측정
    d = measure_distance(W, w, f)

    print(f"측정된 실제 거리(d): {d} cm")

if __name__ == "__main__":
    main()
