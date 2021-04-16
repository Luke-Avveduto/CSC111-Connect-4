"""CSC111 Final Project: Exploring Using Graph Based Data Structures to Implement a Connect 4 AI

Module Description
==================

This module contains classes and functions that run a game of connect 4. The visualization
of the game is done through the python console. Specifically, if two non-human players are
playing the game, the game will not be visualized.

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 Brian Cho and Luke Avveduto
"""
from __future__ import annotations

from typing import Optional
from players import Player
from board import Board


class Connect4Game:
    """A class representing a state of a game of Connect 4

    Representation Invariants:
        - self._board is a valid instance of the Board class
    """
    # Private Instance Attributes
    #   - _board:
    #       Instance of the class Board that represents the game board of a connect 4 game
    #   - _move_sequence:
    #       List of moves that have been made up to the current state of the game. The last
    #       entry in the list is a 1 if red has won the game, -1 if yellow has won the game
    #       and 0 if the game was a tie.
    _board: Board
    _move_sequence: list[int]

    def __init__(self, board: list[list[int]] = None) -> None:
        """Initialize a new Connect4Game starting at the state provided by board.

         If board is None, start a fresh game of Connect 4

         Instance Attributes:
            - board: a 6 x 7 nested list that contains the state of a connect 4 game

        Precondition:
            - len(board) == 6
            - all(len(board[col]) == 7 for col in range(len(board)))
            - state of board follows the conventions of connect 4
              (ex. no suspended chips and
              equal number of moves have been made by each player on every turn)
         """
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
        If yellow has won the game, return -1
        If the game does not have a winner yet, return None
        """
        return self._board.get_winner()


def run_game(red: Player, yellow: Player, text: bool = False) -> list[int]:
    """Run a Connect 4 game between the two players.

    If text is true, the game will be visualized using the python console.
    If one the players is a HumanPlayer, the input will be taken through the python console
    It is recommended to set text to True if one of the players is a HumanPlayer
    """
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


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['typing', 'players', 'board'],  # the names (strs) of imported modules
        'allowed-io': ['run_game'],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })

