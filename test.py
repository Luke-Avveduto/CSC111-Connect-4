import numpy as np
import csv
from scipy.signal import convolve2d

line = []
with open('data/opening_books/8-ply.csv') as file:
    reader = csv.reader(file)

horizontal_kernel = np.array([[1, 1, 1, 1]])
vertical_kernel = np.transpose(horizontal_kernel)
diag1_kernel = np.eye(4, dtype=np.uint8)
diag2_kernel = np.fliplr(diag1_kernel)
detection_kernels_red = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]

BOARD = [[1, 1, 1, 0, 0, 0, 0],
         [1, 0, 0, 0, 0, 0, 0],
         [1, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0]]

temp_board = np.array(BOARD)

for kernel in detection_kernels_red:
    arr = convolve2d(temp_board, kernel, mode='valid')
    print(arr)
    print(np.count_nonzero(arr == 3))
