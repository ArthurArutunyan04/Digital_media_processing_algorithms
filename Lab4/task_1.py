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

def gaussian_filter_2d(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    h, w = image.shape
    kh, kw = kernel.shape
    pad_h, pad_w = kh // 2, kw // 2
    padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='reflect')
    result = np.zeros_like(image, dtype=float)
    for i in range(h):
        for j in range(w):
            region = padded[i:i+kh, j:j+kw]
            result[i, j] = np.sum(region * kernel)
    return np.clip(result, 0, 255).astype(np.uint8)

def blur(image_path: str, kernel_size: int, sigma: float):
    img = cv2.imread(image_path)

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    kernel = gaussian_matrix(kernel_size, sigma=sigma)

    blurred = gaussian_filter_2d(gray_img, kernel)

    blurred = cv2.resize(blurred, (800, 500))

    cv2.imshow("Blurred (Gaussian)", blurred)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    blur("img.png", kernel_size=5, sigma=1.0)

if __name__ == '__main__':
    main()