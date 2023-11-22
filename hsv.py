import cv2
import numpy as np

cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)
cap.set(5, 5)

# 마우스 이벤트 콜백 함수 정의
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"마우스 좌표: ({x}, {y})")

        # 좌표에서 색상값 (BGR) 출력
        color_bgr = frame[y, x]
        # print(f"BGR 값: {color_bgr}")

        # BGR을 HSV로 변환
        color_hsv = cv2.cvtColor(np.uint8([[color_bgr]]), cv2.COLOR_BGR2HSV)[0][0]
        print(f"HSV 값: {color_hsv}")

# 내장 카메라 열기

# 윈도우 생성 및 마우스 이벤트 콜백 함수 등록
cv2.namedWindow('Camera')
cv2.setMouseCallback('Camera', mouse_callback)

while True:
    # 프레임 읽기
    ret, frame = cap.read()

    # 마우스 포인터 현재 위치 표시
    x, y = cv2.getWindowImageRect('Camera')[0:2]
    x += frame.shape[1] + 10
    cv2.putText(frame, f'Mouse: ({x},{y})', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

    # 화면에 프레임 출력
    cv2.imshow('Camera', frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 종료할 때 카메라 해제 및 윈도우 닫기
cap.release()
cv2.destroyAllWindows()
