import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    cx, cy = w // 2, h // 2

    b, g, r = [int(v) for v in frame[cy, cx]]

    red_dist = (b - 0) ** 2 + (g - 0) ** 2 + (r - 255) ** 2
    green_dist = (b - 0) ** 2 + (g - 255) ** 2 + (r - 0) ** 2
    blue_dist = (b - 255) ** 2 + (g - 0) ** 2 + (r - 0) ** 2

    if red_dist <= green_dist and red_dist <= blue_dist:
        color = (0, 0, 255)
    elif green_dist <= blue_dist:
        color = (0, 255, 0)
    else:
        color = (255, 0, 0)

    cross_thickness = 30
    cross_length = 80
    thickness = -1

# Верхняя часть
    x1 = cx - cross_thickness // 2
    x2 = cx + cross_thickness // 2
    y1 = cy - cross_length
    y2 = cy - cross_thickness // 2
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)

# Нижняя часть
    y1 = cy + cross_thickness // 2
    y2 = cy + cross_length
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)

# Горизонтальный прямоугольник
    x1 = cx - cross_length
    x2 = cx + cross_length
    y1 = cy - cross_thickness // 2
    y2 = cy + cross_thickness // 2
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)

    cv2.imshow("Camera+Cross+Color", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
