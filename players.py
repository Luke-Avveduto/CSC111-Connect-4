"""CSC111 Final Project: Exploring Using Graph Based Data Structures to Implement a Connect 4 AI

Module Description
==================

This module contains the Player abstract class and four implementations of it:
HumanPlayer, RandomPlayer, AIPlayerBasic, and AIPlayerComplex. The Player class is designed to
represent a player in a game of connect 4. This means they are given the state of the board in some
way shape or form, and then must decide on a move to play. All of the provided implementations do
that, but how they achieve that varies massively.

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 Brian Cho and Luke Avveduto
"""
from typing import Optional
from connect4 import Connect4Game
from decision_tree import DecisionTree
import random
from board import Board
import opening_book_gen
import math


class Player:
    """An abstract class representing a Connect 4 player
    """
    # Public Instance Attributes:
    #   - is_human: this is a boolean value that is True when instances of this class require
    #               human input to be played. False otherwise
    is_human: bool

    def make_move(self, board: Board):
        """Make a move in the current game"""
        raise NotImplementedError

    # def receive_move(self, move: int) -> None:
    #     """Tells this player what move the other player made
    #     """
    #     raise NotImplementedError


class HumanPlayer(Player):
    """A Connect 4 player that requires an input"""

    def __init__(self):
        self.is_human = True

    def make_move(self, game: Connect4Game) -> int:
        """Make a move in the current game"""
        move = input()
        move = int(move)

        while move not in game.get_valid_moves():
            print("That is not a valid move")
            move = input()
            move = int(move)

        return move

    # def receive_move(self, move: int) -> None:
    #     return None


class RandomPlayer(Player):
    """A connect 4 player that makes random valid moves
    """

    def __init__(self):
        self.is_human = False

    def make_move(self, board: Board) -> int:
        """Make a move in the current game
        """
        return random.choice(board.get_valid_moves())

    # def receive_move(self, move: int) -> None:
    #     return None


class AIPlayerBasic(Player):
    """A Connect 4 player that uses a mix of the greedy algorithm with a decision tree
    and making random moves to play the game automatically.
    """
    # Private Instance Attributes:
    #   - _d_tree: A decision

    _d_tree: Optional[DecisionTree]
    _orthodoxy: float

    def __init__(self, d_tree: DecisionTree, orthodoxy) -> None:
        self._d_tree = d_tree
        self._orthodoxy = orthodoxy

    def make_move(self, game: Connect4Game) -> int:
        if self._d_tree is None or self._d_tree.get_subtrees() == [] or random.uniform(0, 1) > self._orthodoxy:
            choice = random.choice(game.get_valid_moves())
            if self._d_tree is not None:
                choice_subtree = self._d_tree.get_this_move(choice)
                self._d_tree = choice_subtree
            return choice
        else:
            best_move = self._d_tree.get_best_move()
            self._d_tree = self._d_tree.get_this_move(best_move)
            return best_move

    def receive_move(self, move: int) -> None:
        if self._d_tree is not None:
            self._d_tree = self._d_tree.get_this_move(move)


class AIPlayerComplex(Player):
    """An implementation of the ADT Player that uses a combination of the negamax algorithm,
    alpha-beta pruning, a transposition table, and an opening book to in order to always play a
    winning move. In order to keep the running time down, this implementation only solves the game
    'weakly' meaning that while it will win 100% of the time since it goes first every game,
    (as connect 4 is solved game with player 1 being the winner), it will not always win the fewest
    number of turns.

    Details on the negamax algorithm can be found here: https://en.wikipedia.org/wiki/Negamax
    Details on transposition tables can be found here: https://en.wikipedia.org/wiki/Transposition_table

    Representation Invariants:
        - all({self._transposition_table[key] in {1, 0, -1} for key in self._transposition_table[key]})
    """
    # Private Instance Attributes:
    #   - _transposition_table: This is a dict that maps boards to their evaluation (whether it is
    #   a win for the AI or not). The values for this dict are in the set {1, 0, -1} and its keys
    #   are hashes that correspond to a board. For more information on these hashes, see
    #   opening_book_gen.py
    _transposition_table: dict[int:(int, str)]

    def __init__(self, opening_book: str = 'data/opening_books/opening_book.csv') -> None:
        """Creates a new instance of the AIPlayerComplex class. Reads in the values in it's opening
        book.
        """
        self.is_human = False
        self._transposition_table = opening_book_gen.load_opening_book(opening_book)
        print(len(self._transposition_table))

    def make_move(self, board: Board) -> int:
        """Returns a move that can be played in the game represented by the 'board' argument.
        Move selection is done using the 'evaluate' function which evaluates the potential board
        created by playing one of the possible valid moves. The move that creates the board with the
        highest evaluation for the AI is the move that is eventually returned.
        """
        max_score = -math.inf
        best_move = None
        for move in board.get_valid_moves():
            print(move)
            score = self.evaluate(move, board, -math.inf, math.inf)
            print(score)
            if score > max_score:
                max_score = score
                best_move = move
            if score == 1:
                return move
        return best_move

    def evaluate(self, move: int, board: Board, alpha: float, beta: float) -> int:
        """This function returns the evaluation of 'board' after the move 'move' is played. It does
        this via recursion, the negamax algorithm, alpha-beta pruning, and a transposition table.

        Board is NOT mutated when this function is run.
        self._transposition_table CAN be mutated. If it encounters a board that does not have an
        entry in self._transposition_table, the hash of the board and the evaluation will be added
        as an entry.

        Preconditions:
            - move in board.get_valid_moves()
        """
        base_alpha = alpha

        board.make_move(move)

        if board.hash in self._transposition_table:
            print('move in table')
            hash_value = board.hash
            print(hash_value)
            board.un_move(move)

            evaluation = self._transposition_table[hash_value]

            if evaluation[1] == 'exact':
                return evaluation[0]
            elif evaluation[1] == 'low':
                alpha = max(alpha, evaluation[0])
            elif evaluation[1] == 'high':
                beta = min(beta, evaluation[0])

            if alpha >= beta:
                return evaluation[0]

        score = board.get_winner()
        if score is not None:
            self._transposition_table[board.hash] = (score, 'exact')
            board.un_move(move)
            return score
        value = -math.inf

        for next_move in board.get_valid_moves():  # Yellows moves
            value = max(value, -self.evaluate(next_move, board, -beta, -alpha))
            alpha = max(alpha, value)
            if alpha >= beta:
                if value <= base_alpha:
                    entry = (value, 'high')
                elif value >= beta:
                    entry = (value, 'low')
                else:
                    entry = (value, 'exact')
                self._transposition_table[board.hash] = entry
                board.un_move(move)
                return value
        if value <= base_alpha:
            entry = (value, 'high')
        elif value >= beta:
            entry = (value, 'low')
        else:
            entry = (value, 'exact')
        self._transposition_table[board.hash] = entry
        board.un_move(move)
        return value

    # def find_best_move(self, board: Board) -> int:
    #     if board.move_number == 6*7:  # Checks for a draw
    #         return 0
    #
    #     for move in board.get_valid_moves():
    #         board.make_move(move)
    #         winner = board.get_winner()
    #         board.un_move(move)
    #         if winner is not None:
    #             return winner
    #
    #     for move in board.get_valid_moves():
    #         board.make_move(move)
    #         winner = -self.find_best_move(board)



