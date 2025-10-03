import cv2
import numpy as np

cap = cv2.VideoCapture(0)

cv2.namedWindow('Result')

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    kernel = np.ones((7, 7), np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

    moments = cv2.moments(closing)
    area = moments['m00'] if moments['m00'] > 0 else 0

    if area > 100:
        center_x = int(moments['m10'] / moments['m00'])
        center_y = int(moments['m01'] / moments['m00'])
        cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

        y_coords, x_coords = np.where(closing > 0)

        if len(x_coords) > 50:
            min_x = np.min(x_coords)
            max_x = np.max(x_coords)
            min_y = np.min(y_coords)
            max_y = np.max(y_coords)

            width = max_x - min_x + 1
            height = max_y - min_y + 1

            cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 0, 0), 2)

    cv2.putText(frame, f"Area: {area:.0f} px", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    frame = cv2.resize(frame, (350, 300))

    cv2.imshow('Result', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()