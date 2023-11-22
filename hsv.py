import cv2
import numpy as np

# 초기화
mouse_x, mouse_y = 0, 0

# 마우스 이벤트 콜백 함수 정의
def mouse_callback(event, x, y, flags, param):
    global mouse_x, mouse_y
    mouse_x, mouse_y = x, y

# 내장 카메라 열기
cap = cv2.VideoCapture(0)

# 해상도, 프레임 설정
cap.set(3, 640)
cap.set(4, 480)
cap.set(5, 5)

# 윈도우 생성
cv2.namedWindow('Camera')

# 마우스 이벤트 콜백 함수 등록
cv2.setMouseCallback('Camera', mouse_callback)

while True:
    # 프레임 읽기
    ret, frame = cap.read()

    # 마우스 포인터 현재 위치 표시
    cv2.putText(frame, f'coordinate: ({mouse_x},{mouse_y})', (mouse_x, mouse_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

    # 마우스 포인터 위치의 색상값 (BGR) 출력
    if mouse_y < frame.shape[0] and mouse_x < frame.shape[1]:
        color_bgr = frame[mouse_y, mouse_x]
        # cv2.putText(frame, f'BGR: {color_bgr}', (mouse_x, mouse_y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

        # BGR을 HSV로 변환
        color_hsv = cv2.cvtColor(np.uint8([[color_bgr]]), cv2.COLOR_BGR2HSV)[0][0]
        cv2.putText(frame, f'HSV: {color_hsv}', (mouse_x, mouse_y + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

    # 화면에 프레임 출력
    cv2.imshow('Camera', frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 종료할 때 카메라 해제 및 윈도우 닫기
cap.release()
cv2.destroyAllWindows()
