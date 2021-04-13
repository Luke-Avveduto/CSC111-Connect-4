import numpy as np
from scipy.signal import convolve2d
from typing import Optional

GAME_BOARD = [[0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0]]

class Board:
    """A class representing a Connect 4 board"""
    board_array: np.array
    _column_to_row: dict[int: int]
    _is_red_active: bool
    _valid_moves: list[int]
    _win_state: Optional[int]
    _detection_kernels_red: list[np.array]
    _detection_kernels_yellow: list[np.array]

    def __init__(self, python_board: list[list[int]] = None, red_active: bool = True):
        if python_board is not None:
            self.board_array = np.array(python_board)
        else:
            self.board_array = np.array(GAME_BOARD)

        horizontal_kernel = np.array([[1, 1, 1, 1]])
        vertical_kernel = np.transpose(horizontal_kernel)
        diag1_kernel = np.eye(4, dtype=np.uint8)
        diag2_kernel = np.fliplr(diag1_kernel)
        self._detection_kernels_red = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]
        self._detection_kernels_yellow = [kernal * -1 for kernal in self._detection_kernels_red]

        self._is_red_active = red_active
        self._column_to_row = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        self._valid_moves = [0, 1, 2, 3, 4, 5, 6]
        self._win_state = None

    def get_valid_moves(self) -> list[int]:
        """Return a list of the valid moves for the active player."""
        return self._valid_moves

    def get_winner(self) -> int:
        """Return the winner of the current state of the board

        If the game is a tie, return 0
        If red has won the game, return 1
        If yellow has won the game, return -1
        If the game does not have a winner yet, return None"""
        return self._win_state

    def make_move(self, move: int) -> None:
        """Make the give move. This instance of Board will be mutated, and will
        afterwards represent the game state after move is made

        If move is not a currently valid move, raise a Value Error
        """
        if move not in self._valid_moves:
            raise ValueError(f'Move "{move}" is not valid')

        self._update_board(move)
        self._recalculate_valid_moves()

        self._win_state = self._check_winner()
        self._is_red_active = not self._is_red_active

    def _update_board(self, move: int) -> None:
        """Update board by the new move"""
        row = self._column_to_row[move]
        if self._is_red_active:
            self.board_array[row][move] = 1
        else:
            self.board_array[row][move] = -1
        self._column_to_row[move] += 1

    def _recalculate_valid_moves(self) -> None:
        """Recalculates the valid moves the next player can make"""
        for i in range(len(self._valid_moves)):
            if self.board_array[5][self._valid_moves[i]] != 0:
                self._valid_moves.pop(i)
                return

    def _check_winner(self) -> Optional[int]:
        """Checks whether the current game state has a winner

        If the game state is a tie, return 0
        If the game state represents a win for red, return 1
        If the game state represents a win for yellow, return -1
        If the game state does not have a winner, return None
        """
        if self._is_red_active:
            temp_board = self.board_array.clip(min=0, max=1)
            for kernel in self._detection_kernels_red:
                if np.any(convolve2d(temp_board, kernel, mode='valid') == 4):
                    return 1
        else:
            temp_board = self.board_array.clip(min=-1, max=0)
            for kernel in self._detection_kernels_yellow:
                if np.any(convolve2d(temp_board, kernel, mode='valid') == 4):
                    return -1

        if len(self._valid_moves) == 0:
            return 0

        return None


