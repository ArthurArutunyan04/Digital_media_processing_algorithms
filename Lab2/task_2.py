import cv2
import numpy as np

def empty(nothing):
    pass

cap = cv2.VideoCapture(0)

cv2.namedWindow('Trackbars')
cv2.createTrackbar('H_min', 'Trackbars', 0, 255, empty)
cv2.createTrackbar('H_max', 'Trackbars', 255, 255, empty)
cv2.createTrackbar('S_min', 'Trackbars', 131, 255, empty)
cv2.createTrackbar('S_max', 'Trackbars', 255, 255, empty)
cv2.createTrackbar('V_min', 'Trackbars', 58, 255, empty)
cv2.createTrackbar('V_max', 'Trackbars', 255, 255, empty)

cv2.namedWindow('Result')

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos('H_min', 'Trackbars')
    h_max = cv2.getTrackbarPos('H_max', 'Trackbars')
    s_min = cv2.getTrackbarPos('S_min', 'Trackbars')
    s_max = cv2.getTrackbarPos('S_max', 'Trackbars')
    v_min = cv2.getTrackbarPos('V_min', 'Trackbars')
    v_max = cv2.getTrackbarPos('V_max', 'Trackbars')

    lower_red = np.array([h_min, s_min, v_min])
    upper_red = np.array([h_max, s_max, v_max])

    mask = cv2.inRange(hsv, lower_red, upper_red)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    result = cv2.resize(result, (600, 300))

    cv2.imshow('Result', result)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()