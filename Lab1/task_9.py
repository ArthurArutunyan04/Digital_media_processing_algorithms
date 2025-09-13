import cv2


cap = cv2.VideoCapture('https://192.168.1.66:8080/video')

while cap.isOpened():
    ret, frame = cap.read()

    frame = cv2.resize(frame, (600, 400))
    cv2.imshow('mobile cam', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()