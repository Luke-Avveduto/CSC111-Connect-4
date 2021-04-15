"""CSC111 Final Project: Exploring Using Graph Based Data Structures to Implement a Connect 4 AI

Module Description
==================

This module contains classes and functions that run a game of connect 4.

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 Brian Cho and Luke Avveduto
"""
from __future__ import annotations

from typing import Optional
import tkinter
import numpy as np
from scipy.signal import convolve2d
from board import Board
import networkx as nx

BOARD_ROW = 6
BOARD_COLUMN = 7


class Connect4Game:
    """A class representing a state of a game of Connect 4"""
    _board: Board
    _move_sequence: list[int]


    def __init__(self, board: list[list[int]] = None, red_active: bool = True) -> None:
        if board is not None:
            self._board = Board(python_board=board)
        else:
            self._board = Board()

        self._move_sequence = []

    def get_valid_moves(self) -> list[int]:
        """Return a list of the valid moves for the active player."""
        return self._board.get_valid_moves()

    def get_game_board(self) -> Board:
        """Return a Connect 4 gameboard at its current state"""
        return self._board

    def get_move_sequence(self) -> list[int]:
        """Return a list of moves that have been made up to the current game state"""
        return self._move_sequence

    def make_move(self, move: int) -> None:
        """Make the give move. This instance of Connect4Game will be mutated, and will
        afterwards represent the game state after move is made

        If move is not a currently valid move, raise a Value Error
        """
        self._board.make_move(move)
        self._move_sequence.append(move)
        if self.get_winner() is not None:
            self._move_sequence.append(self.get_winner())
        # if move not in self._valid_moves:
        #     raise ValueError(f'Move "{move}" is not valid')
        #
        # new_slot = self._update_board(move)
        # self._move_sequence.append(move)
        #
        # self._recalculate_valid_moves()
        # win = self._check_winner(new_slot)
        # self._win_state = win
        # self._is_red_active = not self._is_red_active

    # def _update_board(self, move: int) -> tuple[int, int]:
    #     """Update the gameboard by the new move"""
    #     for row in range(0, BOARD_ROW):
    #         if self._board[row][move] == 0:
    #             if self._is_red_active:
    #                 self._board[row][move] = 1  # array set to 1 for red tile
    #                 new_slot = (row, move)
    #                 return new_slot
    #             else:
    #                 self._board[row][move] = 2  # array set to 2 for yellow tile
    #                 new_slot = (row, move)
    #                 return new_slot

    def get_winner(self) -> Optional[int]:
        """Returns the winner of the game

        If the game is a tie, return 0
        If red has won the game, return 1
        If yellow has won the game, return 2
        If the game does not have a winner yet, return None
        """
        return self._board.get_winner()

    # def _recalculate_valid_moves(self) -> None:
    #     """Recalculates the valid moves the next player can make"""
    #     new_valid_moves = []
    #     for i in range(len(self._board[5])):
    #         if self._board[5][i] == 0:
    #             new_valid_moves.append(i)
    #     self._valid_moves = new_valid_moves
    #     # for i in range(len(self._valid_moves)):
    #     #     if self._board[5][self._valid_moves[i]] != 0:
    #     #         self._valid_moves.pop(i)

    # def _check_winner(self, new_slot: tuple[int, int]) -> Optional[int]:
    #     """Checks whether the current game state has a winner
    #
    #     If the game state is a tie, return 0
    #     If the game state represents a win for red, return 1
    #     If the game state represents a win for yellow, return 2
    #     If the game state does not have a winner, return None
    #     """
    #
    #     new_row, new_col = new_slot[0], new_slot[1] # row number and column number of new slot
    #     new_value = self._board[new_row][new_col] # the value at the new slot (0 or 1 or 2)
    #     num_in_a_row, is_in_a_row = 0, False # keeps track of same values in a row
    #
    #     for col in range(0, BOARD_COLUMN):
    #         if self._board[new_row][col] == new_value: # checks whether current spot is same
    #             if is_in_a_row:                        # if previous slot was the same value
    #                 num_in_a_row += 1
    #                 if num_in_a_row >= 4:  # checks whether there was a 4-in-a-row
    #                     return new_value
    #             else:                                  # if previous slot was not the same value
    #                 num_in_a_row = 1
    #                 is_in_a_row = True
    #         else:                                      # if the current spot is not the same
    #             num_in_a_row = 0
    #             is_in_a_row = False
    #
    #     num_in_a_row, is_in_a_row = 0, False           # reset counter
    #
    #     for row in range(0, new_row + 1):                  # same method was above
    #         if self._board[row][new_col] == new_value:
    #             if is_in_a_row:
    #                 num_in_a_row += 1
    #                 if num_in_a_row >= 4:
    #                     return new_value
    #             else:
    #                 num_in_a_row = 1
    #                 is_in_a_row = True
    #         else:
    #             num_in_a_row = 0
    #             is_in_a_row = False
    #
    #
    #     col_index, row_index = new_col, new_row                     # declare index
    #     num_in_a_row, is_in_a_row = 0, False                        # reset counter
    #
    #     while col_index - 1 >= 0 and row_index - 1 >= 0:            # traverse until the bottom of / path
    #         col_index, row_index = col_index - 1, row_index - 1
    #
    #     while col_index + 1 < BOARD_COLUMN and row_index + 1 < BOARD_ROW:
    #         if self._board[row_index][col_index] == 0:
    #             break
    #         elif self._board[row_index][col_index] == new_value:
    #             if is_in_a_row:
    #                 num_in_a_row += 1
    #                 if num_in_a_row >= 4:
    #                     return new_value
    #             else:
    #                 num_in_a_row = 1
    #                 is_in_a_row = True
    #         else:
    #             num_in_a_row = 0
    #             is_in_a_row = False
    #         col_index, row_index = col_index + 1, row_index + 1
    #
    #     col_index, row_index = new_col, new_row
    #     num_in_a_row, is_in_a_row = 0, False
    #
    #     while col_index + 1 < BOARD_COLUMN and row_index - 1 >= 0:  # traverse until the bottom of \ path
    #         col_index, row_index = col_index + 1, row_index - 1
    #
    #     while col_index - 1 >= 0 and row_index + 1 < BOARD_ROW:
    #         if self._board[row_index][col_index] == 0:
    #             break
    #         elif self._board[row_index][col_index] == new_value:
    #             if is_in_a_row:
    #                 num_in_a_row += 1
    #                 if num_in_a_row >= 4:
    #                     return new_value
    #             else:
    #                 num_in_a_row = 1
    #                 is_in_a_row = True
    #         else:
    #             num_in_a_row = 0
    #             is_in_a_row = False
    #         col_index, row_index = col_index - 1, row_index + 1
    #
    #     if len(self._valid_moves) == 0:
    #         return 0
    #     else:
    #         return None

