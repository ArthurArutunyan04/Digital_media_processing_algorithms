import cv2

cap = cv2.VideoCapture("voditel.mp4")
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
result = cv2.VideoWriter("new_voditel.mp4", fourcc, cap.get(cv2.CAP_PROP_FPS), (600, 600))

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.resize(frame, (600, 600))
    result.write(frame)
    cv2.imshow('result', frame)


    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
result.release()
cv2.destroyAllWindows()
