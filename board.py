import numpy as np
from scipy import signal

class Board:

    board_array: np.array
    _column_to_row:

    def __init__(self, python_board: list[list[int]]):
        self._board_array = np.array(python_board)