import cv2


Image = "Image2.jpg"

original = cv2.imread(Image)
parody = cv2.cvtColor(original, cv2.COLOR_BGR2HSV)

cv2.imshow('Original', original)
cv2.imshow('Parody(HSV)', parody)

cv2.waitKey(0)
cv2.destroyAllWindows()
