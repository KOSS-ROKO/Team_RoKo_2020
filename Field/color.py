import cv2
import numpy as np

# 이미지를 로드합니다.
image = cv2.imread('./src/f1.png')

# 추출하려는 색상의 BGR 값 범위를 정의합니다.


#경기장 색깔 범위!!!!!!!!
lower_color = np.array([0, 0, 0]) 
upper_color = np.array([100, 255, 70])

# 이미지에서 해당 범위의 색상을 마스킹합니다.
mask = cv2.inRange(image, lower_color, upper_color)

# 마스크와 이미지를 비트 AND 연산하여 추출합니다.
result = cv2.bitwise_and(image, image, mask=mask)

# 결과 이미지를 표시합니다.
cv2.imshow('Extracted Color', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
