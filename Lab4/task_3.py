import cv2
import numpy as np


def gaussian_matrix(size, sigma=1.0, normalize=True):
    center = size // 2
    matrix = np.zeros((size, size), dtype=float)
    for x in range(size):
        for y in range(size):
            dx = x - center
            dy = y - center
            matrix[x, y] = (1 / (2 * np.pi * sigma ** 2)) * np.exp(-(dx ** 2 + dy ** 2) / (2 * sigma ** 2))
    if normalize:
        matrix /= matrix.sum()
    return matrix


def gaussian_filter_2d(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    h, w = image.shape
    kh, kw = kernel.shape
    pad_h, pad_w = kh // 2, kw // 2
    padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='reflect')
    result = np.zeros_like(image, dtype=float)
    for i in range(h):
        for j in range(w):
            region = padded[i:i + kh, j:j + kw]
            result[i, j] = np.sum(region * kernel)
    return np.clip(result, 0, 255).astype(np.uint8)


sobel_x = np.array([[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]], dtype=np.float64)

sobel_y = np.array([[-1, -2, -1],
                    [0, 0, 0],
                    [1, 2, 1]], dtype=np.float64)


def convolve(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    h, w = image.shape
    padded = np.pad(image, ((1, 1), (1, 1)), mode='reflect')
    out = np.zeros_like(image, dtype=np.float64)
    for i in range(h):
        for j in range(w):
            region = padded[i:i + 3, j:j + 3]
            out[i, j] = np.sum(region * kernel)
    return out


def get_quantized_angle(gx, gy, tg):
    quantized = np.zeros_like(gx, dtype=np.uint8)
    mask0 = ((gx > 0) & (gy < 0) & (tg < -2.414)) | ((gx < 0) & (gy < 0) & (tg > 2.414))
    quantized[mask0] = 0
    mask1 = (gx > 0) & (gy < 0) & (tg >= -2.414) & (tg < -0.414)
    quantized[mask1] = 1
    mask2 = ((gx > 0) & (gy < 0) & (tg >= -0.414)) | ((gx > 0) & (gy > 0) & (tg < 0.414))
    quantized[mask2] = 2
    mask3 = (gx > 0) & (gy > 0) & (tg >= 0.414) & (tg < 2.414)
    quantized[mask3] = 3
    mask4 = ((gx > 0) & (gy > 0) & (tg >= 2.414)) | ((gx < 0) & (gy > 0) & (tg <= -2.414))
    quantized[mask4] = 4
    mask5 = (gx < 0) & (gy > 0) & (tg > -2.414) & (tg <= -0.414)
    quantized[mask5] = 5
    mask6 = ((gx < 0) & (gy > 0) & (tg > -0.414)) | ((gx < 0) & (gy < 0) & (tg < 0.414))
    quantized[mask6] = 6
    mask7 = (gx < 0) & (gy < 0) & (tg >= 0.414) & (tg < 2.414)
    quantized[mask7] = 7
    return quantized


def non_max_suppression(magnitude, quantized_angle):
    h, w = magnitude.shape
    nms = np.zeros_like(magnitude, dtype=np.uint8)

    for i in range(1, h - 1):
        for j in range(1, w - 1):
            direction = quantized_angle[i, j]
            mag = magnitude[i, j]

            if direction in [0, 4]:
                n1, n2 = magnitude[i, j - 1], magnitude[i, j + 1]
            elif direction in [1, 5]:
                n1, n2 = magnitude[i - 1, j + 1], magnitude[i + 1, j - 1]
            elif direction in [2, 6]:
                n1, n2 = magnitude[i - 1, j], magnitude[i + 1, j]
            else:
                n1, n2 = magnitude[i - 1, j - 1], magnitude[i + 1, j + 1]

            if mag >= n1 and mag >= n2:
                nms[i, j] = mag
            else:
                nms[i, j] = 0
    return nms


def main():
    image_path = "img.png"
    kernel_size = 5
    sigma = 1.0

    img = cv2.imread(image_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gauss_kernel = gaussian_matrix(kernel_size, sigma)
    blurred = gaussian_filter_2d(gray, gauss_kernel)

    grad_x = convolve(blurred.astype(np.float64), sobel_x)
    grad_y = convolve(blurred.astype(np.float64), sobel_y)

    magnitude = np.sqrt(grad_x ** 2 + grad_y ** 2)
    magnitude = np.clip(magnitude, 0, 255).astype(np.uint8)

    grad_x_safe = np.where(grad_x == 0, 1e-6, grad_x)
    tg = grad_y / grad_x_safe
    quantized_angle = get_quantized_angle(grad_x, grad_y, tg)

    nms = non_max_suppression(magnitude, quantized_angle)

    print(nms)

    cv2.imshow("After Non-Maximum Suppression", cv2.resize(nms, (800, 500)))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()