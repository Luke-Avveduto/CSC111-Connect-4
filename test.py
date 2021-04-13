import numpy as np
from scipy.signal import convolve2d

board = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, -1, 0, 0, 0],
]

fast_board = np.array(board)

horizontal_kernel = np.array([[1, 1, 1, 1]])
vertical_kernel = np.transpose(horizontal_kernel)
diag1_kernel = np.eye(4, dtype=np.uint8)
diag2_kernel = np.fliplr(diag1_kernel)
detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]

for kernel in detection_kernels:
    print(np.any(convolve2d(fast_board, kernel, mode='valid') == 4))

print(fast_board.clip(min=0, max=1))
print(fast_board)