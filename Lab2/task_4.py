import cv2
import numpy as np

cap = cv2.VideoCapture(0)

cv2.namedWindow('Result')

while True:
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 131, 58])
    upper_red = np.array([255, 255, 255])

    mask = cv2.inRange(hsv, lower_red, upper_red)

    kernel = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

    moments = cv2.moments(closing)
    area = moments['m00'] if moments['m00'] > 0 else 0

    if area > 0:
        center_x = int(moments['m10'] / moments['m00'])
        center_y = int(moments['m01'] / moments['m00'])
    else:
        center_x, center_y = 0, 0

    result = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.putText(result, f"Area: {area:.0f} px", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    result = cv2.resize(result, (350, 300))

    result = cv2.resize(result, (350, 300))
    closing = cv2.resize(closing, (350, 300))

    cv2.imshow('Result', result)
    cv2.imshow('Closing', closing)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()