import numpy as np
from scipy.signal import convolve2d
from typing import Optional
import csv


GAME_BOARD = [[0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0]]


class Board:
    """A class representing a Connect 4 board"""
    board_array: np.array
    move_number: int
    hash: int
    _valid_move_order: dict[int: int]
    _red_hash_keys: np.array
    _yellow_hash_keys: np.array
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

        self.move_number = 0

        horizontal_kernel = np.array([[1, 1, 1, 1]])
        vertical_kernel = np.transpose(horizontal_kernel)
        diag1_kernel = np.eye(4, dtype=np.uint8)
        diag2_kernel = np.fliplr(diag1_kernel)
        self._detection_kernels_red = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]
        self._detection_kernels_yellow = [kernal * -1 for kernal in self._detection_kernels_red]

        self._valid_move_order = {3: 0, 2: 1, 4:2, 5: 3, 1:4, 0:5, 6:6}

        self._is_red_active = red_active
        self._column_to_row = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        self._valid_moves = [3, 2, 4, 5, 1, 0, 6]
        self._win_state = None

        red_hash_keys = []
        with open('data/Zobrist_Hash_Keys/Zobrist_red_key.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                red_hash_keys.append(row)
        self._red_hash_keys = np.array(red_hash_keys)

        yellow_hash_keys = []
        with open('data/Zobrist_Hash_Keys/Zobrist_yellow_key.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                yellow_hash_keys.append(row)
        self._yellow_hash_keys = np.array(yellow_hash_keys)

        self.hash = 0

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
        self.move_number += 1

    def un_move(self, previous_move) -> None:
        """Return the board to the state before the previous move
        Precondition:
            - previous_move must have been the last move played
        """
        self._column_to_row[previous_move] -= 1
        # if self._column_to_row[previous_move] < 6:
        #     self._valid_moves.insert(self._valid_move_order[previous_move], previous_move)
        row = self._column_to_row[previous_move]
        self.board_array[row][previous_move] = 0

        self._is_red_active = not self._is_red_active

        if self._is_red_active:
            self.hash = self.hash ^ int(self._red_hash_keys[row][previous_move])
        else:
            self.hash = self.hash ^ int(self._red_hash_keys[row][previous_move])

        self._recalculate_valid_moves()

        if self._win_state is not None:
            self._win_state = None

        self.move_number -= 1

    def _update_board(self, move: int) -> None:
        """Update board by the new move"""
        row = self._column_to_row[move]
        if self._is_red_active:
            self.board_array[row][move] = 1
            self.hash = self.hash ^ int(self._red_hash_keys[row][move])
        else:
            self.board_array[row][move] = -1
            self.hash = self.hash ^ int(self._yellow_hash_keys[row][move])

        self._column_to_row[move] += 1

        # if self._column_to_row[move] == 6:
        #     self._valid_moves.remove(move)

    def _recalculate_valid_moves(self) -> None:
        """Recalculates the valid moves the next player can make"""
        new_valid_moves = []
        for i in range(len(self.board_array[5])):
            if self.board_array[5][i] == 0:
                new_valid_moves.append(i)
        self._valid_moves = new_valid_moves
        # for i in range(len(self._valid_moves)):
        #     if self.board_array[5][self._valid_moves[i]] != 0:
        #         self._valid_moves.pop(i)
        #         return

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


