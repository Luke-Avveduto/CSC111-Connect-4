"""CSC111 Final Project: Exploring Using Graph Based Data Structures to Implement a Connect 4 AI

Module Description
==================

This module contains a class that represents the game board of a Connect4Game. The board
handles most operations needed to run the game, such as calculating valid moves, making moves,
and checking for the winner. The board itself is represented in a 2d numpy array. The class
also uses Zobrist Hashing to represent a unique state of the game board as a hash. This is done
using the bitwise XOR operation and two list of keys. For more information, see
opening_book_gen.py

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 Brian Cho and Luke Avveduto
"""
from typing import Optional
import csv
import numpy as np
from scipy.signal import convolve2d


class Board:
    """A class representing a Connect 4 board. This class keeps track of the position of all
    the pieces as well as what moves are valid, whose turn it is, and many other things.

    Representation Invariants:
        - all({move in {0, 1, 2, 3, 4, 5, 6} for move in self._valid_moves})
    """
    # Public Instance Attributes:
    #   - board_array: this is a numpy 2d array that stores the board as a 6 x 7 grid of 0's, 1's,
    #     and -1's. A 0 is a blank space, a 1 is a red piece, and a -1 is a yellow piece.
    #   - move_number: this is the number of moves that has been played so far/
    #   - hash: this is a hash for the board produced via the Zobrist hashing algorithm. A board
    #     that has the pieces in the same position will always have the same hash, regardless of
    #     what moves were made to get there. This is used as a key in a transposition table. More
    #     info on this can be found in opening_book_gen.py
    # Private Instance Attributes:
    #   - _valid_moves: this is a list of the moves that can be made in the boards current state. A
    #     'move' is one of the seven columns, numbered 0-6 inclusively. If a column is full, it is
    #      no longer available and so it will not be present in this list
    #   - _valid_move_order: this is a dict that maps columns to their original indices in
    #      self._valid_more_order. This order is very important for optimising alpha-beta pruning.
    #   - _column_to_row: this is dict that maps a column to what row in the array a piece placed in
    #     that column in needs to be placed.
    #   - _is_red_active: this is a boolean that is True when it is red's turn and False when it is
    #     yellow's turn. Red goes first every game, and so this is True by default.
    #   - _win_state: this is 1 when the board is in a state where 4 has won, -1 if yellow has won,
    #     0 if it is draw, and None otherwise.
    #   - _detection_kernels_red: this is a list of numpy arrays where each numpy array encodes
    #     one of the four possible patterns you can create to win a game of connect 4. This list is
    #     for red so all the elements are 1.
    #   - _detection_kernels_yellow: The same as above but with every element being a -1 as it is
    #     for yellow.
    #   - _red_hash_keys: This is a 2d numpy array that, for each possible location of a piece on
    #     board, a 64 bit number is stored. This is used to calculate a hash for the board using
    #     Zobrist's hashing algorithm. This one contains the keys for all the possible places red
    #     pieces can go. See opening_book_gen.py for more information.
    #   - _yellow_hash_keys: Same as above but for the yellow pieces.

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

    def __init__(self, python_board: list[list[int]] = None, red_active: bool = True) -> None:
        """Creates a new instance of the Board class. By default, the board is initialised to a
        state of all zeros, meaning the board is blank and no moves has been played yet. However,
        this can be changed if you provide a argument 'python_board'

        Preconditions:
            - all({n in {-1, 0, 1} for n in row for row in python_board})
        """

        game_board = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0]]

        if python_board is not None:
            self.board_array = np.array(python_board)
        else:
            self.board_array = np.array(game_board)

        self.move_number = 0

        # Creating the kernels to use in a 2d convolution to check the board for a winner later
        across = np.array([[1, 1, 1, 1]])
        vertical = np.transpose(across)
        main_diagonal = np.eye(4, dtype=np.uint8)
        off_diagonal = np.fliplr(main_diagonal)
        self._detection_kernels_red = [across, vertical, main_diagonal, off_diagonal]
        self._detection_kernels_yellow = [kernel * -1 for kernel in self._detection_kernels_red]

        self._is_red_active = red_active

        # Matches moves to their indices in self._valid_moves, this order is very important
        # for optimising alpha-beta pruning
        self._valid_move_order = {3: 0, 2: 1, 4: 2, 5: 3, 1: 4, 0: 5, 6: 6}
        self._valid_moves = [3, 2, 4, 5, 1, 0, 6]
        self._column_to_row = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

        self._win_state = None

        # This code reads in the hash keys for use in Zobrist hashing, for more information, see
        # opening_book_gen.py
        red_hash_keys = []
        with open('data/Zobrist_Hash_Keys/Zobrist_red_key.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                red_hash_keys.append([int(r) for r in row])
        self._red_hash_keys = np.array(red_hash_keys)

        yellow_hash_keys = []
        with open('data/Zobrist_Hash_Keys/Zobrist_yellow_key.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                yellow_hash_keys.append([int(r) for r in row])
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
        """Make the given move. This instance of Board will be mutated, and will
        afterwards represent the game state after move is made

        If move is not a currently valid move, raise a Value Error
        """
        if move not in self._valid_moves:
            raise ValueError(f'Move "{move}" is not valid')

        self._update_board(move)

        self._win_state = self._check_winner()
        self._is_red_active = not self._is_red_active
        self.move_number += 1

    def un_move(self, previous_move: int) -> None:
        """Return the board to the state before the previous move.
        Precondition:
            - previous_move must have been the last move played
        """
        self._column_to_row[previous_move] -= 1
        if self._column_to_row[previous_move] == 5:
            self._valid_moves.insert(self._valid_move_order[previous_move], previous_move)
        row = self._column_to_row[previous_move]
        self.board_array[row][previous_move] = 0

        self._is_red_active = not self._is_red_active

        if self._is_red_active:
            self.hash = self.hash ^ int(self._red_hash_keys[row][previous_move])
        else:
            self.hash = self.hash ^ int(self._red_hash_keys[row][previous_move])

        if self._win_state is not None:
            self._win_state = None

        self.move_number -= 1

    def _update_board(self, move: int) -> None:
        """Update board by the new move.
        Preconditions:
            - move in self._valid_moves
        """
        row = self._column_to_row[move]  # Find what row to place the disk in
        if self._is_red_active:
            self.board_array[row][move] = 1
            self.hash = self.hash ^ int(self._red_hash_keys[row][move])  # Update hash
        else:
            self.board_array[row][move] = -1
            self.hash = self.hash ^ int(self._yellow_hash_keys[row][move])  # # Update hash

        self._column_to_row[move] += 1
        if self._column_to_row[move] == 6:
            self._valid_moves.remove(move)

    def _check_winner(self) -> Optional[int]:
        """Checks whether the current game state has a winner

        If the game state is a tie, return 0
        If the game state represents a win for red, return 1
        If the game state represents a win for yellow, return -1
        If the game state does not have a winner, return None
        """

        if self._is_red_active:
            temp_board = self.board_array.clip(min=0, max=1)  # Turns all -1's into 0's
            for kernel in self._detection_kernels_red:
                # For each of the patterns that produce a win, do a 2d convolution on the copy
                # of the board. If there 4's in the resulting array, one of the kernels found a
                # match and so there is a 4 in a row somewhere. This is done this way to save
                # as much time as possible, because optimisation is very important to the
                # AI's performance and python is already quite slow
                if np.any(convolve2d(temp_board, kernel, mode='valid') == 4):
                    return 1
        else:
            temp_board = self.board_array.clip(min=-1, max=0)  # Turns all 1's into 0's
            for kernel in self._detection_kernels_yellow:
                # Same as before
                if np.any(convolve2d(temp_board, kernel, mode='valid') == 4):
                    return -1

        if len(self._valid_moves) == 0:
            return 0

        return None

    def evaluate_score(self, color: int) -> float:
        """Calculates the score of the current state of the board using the
        following evaluation heuristic:
            (# of 3 in a rows the current player has)*100 + # of 2 in a rows the current player has
            - (# of 3 in a rows the other player has)*100 - # of 2 in a rows the other player has

        The score is calculated in favor of the player that is making the next move.

        Preconditions:
            - color in {-1, 1}
        """
        # We want to judge how good the board is for color
        winner = self.get_winner()
        if winner == 1:
            return 10000 * color
        if winner == -1:
            return -10000 * color
        if winner == 0:
            return 0

        # Score the board for how good it is for red
        # Positive if color is good
        # Negative if color is bad
        num_three_red, num_two_red = 0, 0
        red_board = self.board_array.clip(min=0, max=1)
        for kernel in self._detection_kernels_red:
            # Similar to what is done in _check_win, it looks for the patterns of
            # two in a rows and tree in a rows.
            convolved_arr = convolve2d(red_board, kernel, mode='valid')
            num_three_red += np.count_nonzero(convolved_arr == 3)
            num_two_red += np.count_nonzero(convolved_arr == 2)

        num_three_yel, num_two_yel = 0, 0
        yellow_board = self.board_array.clip(min=-1, max=0)
        for kernel in self._detection_kernels_yellow:
            # Same as above but for yellow
            convolved_arr = convolve2d(yellow_board, kernel, mode='valid')
            num_three_yel += np.count_nonzero(convolved_arr == 3)
            num_two_yel += np.count_nonzero(convolved_arr == 2)

        # This is our evaluation heuristic
        score = (num_three_red * 100 + num_two_red) - (num_three_yel * 100 + num_two_yel)
        return score * color


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['numpy', 'scipy.signal', 'typing', 'csv'],  # the names (strs) of imported modules
        'allowed-io': [],
        # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })
