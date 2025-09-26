import numpy as np

def gaussian_matrix(size, sigma=1.0):
    center = size // 2
    matrix = np.zeros((size, size), dtype=float)

    for x in range(size):
        for y in range(size):
            dx = x - center
            dy = y - center
            matrix[x, y] = (1 / (2 * np.pi * sigma**2)) * np.exp(-(dx**2 + dy**2) / (2 * sigma**2))

    return matrix


sizes = [3, 5, 7]
sigma = 1.0

np.set_printoptions(precision=4, suppress=True)

for size in sizes:
    print(f"\nМатрица Гаусса {size}x{size} (sigma={sigma}):")
    matrix = gaussian_matrix(size, sigma)
    print(matrix)
    print("Сумма элементов:", matrix.sum())
