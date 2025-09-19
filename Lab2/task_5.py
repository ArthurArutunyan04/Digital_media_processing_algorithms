import cv2
import numpy as np

cap = cv2.VideoCapture(0)

cv2.namedWindow('Result')

while True:
    ret, frame = cap.read()
    if not ret:
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
    if area > 100:
        center_x = int(moments['m10'] / moments['m00'])
        center_y = int(moments['m01'] / moments['m00'])
        cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
    else:
        center_x, center_y = 0, 0
        print("Объект не найден")

    contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours and area > 100:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 2)
    cv2.putText(frame, f"Area: {area:.0f} px", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    frame = cv2.resize(frame, (350, 300))

    cv2.imshow('Result', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()