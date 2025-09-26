import cv2
import numpy as np

def gaussian_matrix(size, sigma=1.0, normalize=True):
    center = size // 2
    matrix = np.zeros((size, size), dtype=float)

    for x in range(size):
        for y in range(size):
            dx = x - center
            dy = y - center
            matrix[x, y] = (1 / (2 * np.pi * sigma**2)) * np.exp(-(dx**2 + dy**2) / (2 * sigma**2))

    if normalize:
        matrix /= matrix.sum()

    return matrix


def gaussian_filter(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    h, w = image.shape[:2]
    kh, kw = kernel.shape
    pad_h, pad_w = kh // 2, kw // 2

    padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w), (0, 0)), mode='reflect')
    result = np.zeros_like(image, dtype=float)

    for c in range(image.shape[2]):
        for i in range(h):
            for j in range(w):
                region = padded[i:i+kh, j:j+kw, c]
                result[i, j, c] = np.sum(region * kernel)

    return np.clip(result, 0, 255).astype(np.uint8)

img = cv2.imread("Image.png")
if img is None:
    raise FileNotFoundError("Файл Image.png не найден!")

kernel = gaussian_matrix(size=5, sigma=1.0, normalize=True)

filtered_img = gaussian_filter(img, kernel)

cv2.imwrite("output_gaussian.png", filtered_img)

