import cv2
import numpy as np

# 이미지를 로드합니다.
image = cv2.imread('src/f1.png')

# HSV 색상 공간으로 변환합니다.
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# 초록색 범위를 정의합니다.
lower_green = np.array([0, 100, 0])
upper_green = np.array([85, 255, 100])

# 초록색 영역을 마스킹합니다.
mask = cv2.inRange(hsv, lower_green, upper_green)

# 마스크와 이미지를 비트 AND 연산합니다.
masked_image = cv2.bitwise_and(image, image, mask=mask)

# 그레이스케일로 변환합니다.
gray = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)

# 가우시안 블러를 적용합니다. (노이즈 감소)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Canny 엣지 검출을 수행합니다.
edges = cv2.Canny(blurred, 50, 150)

# 경계를 찾습니다.
contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 경계를 그립니다.
cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

# 결과 이미지를 표시합니다.
cv2.imshow('Edge Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
