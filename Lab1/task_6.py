import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    cx, cy = w // 2, h // 2

    color = (0, 0, 255)
    thickness = 2

    cross_thickness = 30
    cross_length = 80

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

    cv2.imshow("Camera+Cross", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
