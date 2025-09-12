import cv2


cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
result = cv2.VideoWriter('Cam.mp4', fourcc, 60.0, (600, 600))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (600, 600))
    cv2.imshow('Camera', frame)
    result.write(frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break



cap.release()
result.release()
cv2.destroyAllWindows()


cap = cv2.VideoCapture('Cam.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow('Recorded Video', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
