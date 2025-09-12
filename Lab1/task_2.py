import cv2

Image = "Image.jpeg"

image1 = cv2.imread(Image, cv2.IMREAD_ANYDEPTH)
image2 = cv2.imread(Image, cv2.IMREAD_REDUCED_GRAYSCALE_2)
image3 = cv2.imread(Image, cv2.IMREAD_REDUCED_COLOR_2)

cv2.namedWindow("anydepth_image", cv2.WINDOW_AUTOSIZE)
cv2.namedWindow("reduced_gray_image", cv2.WINDOW_KEEPRATIO)
cv2.namedWindow("reduced_color_image", cv2.WINDOW_NORMAL)

cv2.imshow("anydepth_image", image1)
cv2.imshow("reduced_gray_image", image2)
cv2.imshow("reduced_color_image", image3)

cv2.waitKey(0)
cv2.destroyAllWindows()

