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
from players import Player
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

    def get_winner(self) -> Optional[int]:
        """Returns the winner of the game

        If the game is a tie, return 0
        If red has won the game, return 1
        If yellow has won the game, return 2
        If the game does not have a winner yet, return None
        """
        return self._board.get_winner()


def run_game(red: Player, yellow: Player, text: bool = False) -> list[int]:
    """Run a Connect 4 game between the two players"""
    game = Connect4Game()

    current_player = red
    while game.get_winner() is None:
        board = game.get_game_board()

        if text:
            for r in range(len(board.board_array) - 1, -1, -1):
                print(*board.board_array[r])

            print('The valid moves are:', end=' ')
            print(*game.get_valid_moves(), sep=', ')

        new_move = current_player.make_move(board)
        game.make_move(new_move)

        if current_player is red:
            current_player = yellow
        else:
            current_player = red

    return game.get_move_sequence()
