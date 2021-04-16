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
    """An implementation of the abstract class Player that uses a combination of the
    minimax algorithm, alpha-beta pruning, and a transposition table in order to chose what move it
    will make. This implementation works well with depth between 5 and 7. While it will technically
    work with any depth level, values below 5 will not produce that accurate moves while values
    above 7 will result in the AI taking several minutes to make a move, especially in the beginning
    of the game, so use at your own risk.

    Details on the minimax algorithm can be found here: https://en.wikipedia.org/wiki/Minimax
    Details on transposition tables can be found here: https://en.wikipedia.org/wiki/Transposition_table

    Representation Invariants:
        - self._depth >= 0
        - all({self._transposition_table[1] in {'exact', 'high', 'low'} for key in self._transposition_table})
        - all({self._depth >= self._transposition_table[2] >= 0 for key in self._transposition_table})
    """
    # Private Instance Attributes:
    #   - _transposition_table: This is a dict that maps boards to their evaluation by the minimax
    #   algorithm. In particular, it doesn't actually map Board objects to evaluations, instead each
    #   has a hash and that is mapped to a tuple the contains the evaluation of that board with the
    #   by the minimax algorithm, a string that says whether the value is exact, an upperbound, or
    #   a lower bound, and finally the depth those values were calculated at For more information on
    #   these hashes, see opening_book_gen.py
    _depth: int
    _transposition_table: dict[int:(int, str, int)]

    def __init__(self, opening_book: str = 'data/opening_books/opening_book.csv') -> None:
        """Creates a new instance of the AIPlayerComplex class. Reads in the values in it's opening
        book.
        """
        self.is_human = False
        # self._transposition_table = opening_book_gen.load_opening_book(opening_book)
        self._transposition_table = {}

    def make_move(self, board: Board) -> int:
        """Returns a move that can be played in the game represented by the 'board' argument.
        Move selection is done using the 'minimax' function which uses the minimax algorithm with
        a depth of self.depth to decide on the best move to play.
        """
        move, evalutation = self.minimax(board, -math.inf, math.inf, 7, 1)
        return move

    def minimax(self, board: Board, alpha: int, beta: int, depth: int, color: int) -> (int, int):
        """This function implements the minimax algorithm with alpha-beta pruning and a
        transposition table with a depth of 'depth'. This algorithm uses recursion to explore the
        tree like structure of all the possible games that could happen from the current 'board'
        state and will eventually return a tuple of ints containing the best move in for the player
        with color 'color' and the evaluation of how good the resulting position will be
        for the player.

        Preconditions:
            - depth >= 0
            - color in {-1, 1}
        """
        possible_moves = board.get_valid_moves()

        for move in possible_moves:
            board.make_move(move)
            winner = board.get_winner()
            if winner == 1:
                board.un_move(move)
                return move, 1000000
            elif winner == -1:
                board.un_move(move)
                return move, -1000000
            elif winner == 0:
                board.un_move(move)
                return move, 0
            board.un_move(move)

        if len(possible_moves) == 0 or depth == 0:
            if depth == 0:
                return None, board.evaluate_score(color)
            else:
                return None, 0  # Game is a draw

        if color == 1:
            return self.max_player(board, alpha, beta, depth)

        else:
            return self.min_player(board, alpha, beta, depth)

    def min_player(self, board: Board, alpha: int, beta: int, depth: int) -> (int, int):
        """This function uses the minimax algorithm with depth 'depth', to determine the move that
        results in the best position for the minimising player. It uses alpha-beta pruning
        and a transposition table to help cut down on running time. It eventually returns the best
        move and the evaluation it gives of the board after it is played.

        Preconditions:
            - depth >= 0
        """
        base_beta = beta
        value = math.inf
        best_move = 0
        possible_moves = board.get_valid_moves()
        for move in possible_moves:
            board.make_move(move)

            if board.hash in self._transposition_table and self._transposition_table[board.hash][2] >= depth:
                entry = self._transposition_table[board.hash]
                if entry[1] == 'exact':
                    score = entry[0]
                    if score < value:
                        value = score
                        best_move = move
                elif entry[1] == 'low':
                    alpha = max(alpha, entry[0])
                elif entry[1] == 'high':
                    beta = min(beta, entry[0])
            else:
                score = self.minimax(board, alpha, beta, depth - 1, 1)[1]
                if score < value:
                    value = score
                    best_move = move
            beta = min(value, beta)
            if alpha >= beta:
                if value <= alpha:
                    entry = (value, 'high', depth)
                elif value >= base_beta:
                    entry = (value, 'low', depth)
                else:
                    entry = (value, 'exact', depth)
                self._transposition_table[board.hash] = entry
                board.un_move(move)
                return move, value
            else:
                board.un_move(move)

        board.make_move(best_move)
        hash_value = board.hash
        board.un_move(best_move)

        if value <= alpha:
            entry = (value, 'high', depth)
        elif value >= base_beta:
            entry = (value, 'low', depth)
        else:
            entry = (value, 'exact', depth)
        self._transposition_table[hash_value] = entry
        return best_move, value

    def max_player(self, board: Board, alpha: int, beta: int, depth: int) -> (int, int):
        """This function uses the minimax algorithm with depth 'depth', to determine the move that
        results in the best position for the maximising player. It uses alpha-beta pruning
        and a transposition table to help cut down on running time. It eventually returns the best
        move and the evaluation it gives of the board after it is played.

        Preconditions:
            - depth >= 0
        """
        base_alpha = alpha
        value = -math.inf
        best_move = 0
        possible_moves = board.get_valid_moves()
        for move in possible_moves:
            board.make_move(move)

            if board.hash in self._transposition_table and self._transposition_table[board.hash][2] >= depth:
                entry = self._transposition_table[board.hash]
                if entry[1] == 'exact':
                    score = entry[0]
                    if score > value:
                        value = score
                        best_move = move
                elif entry[1] == 'low':
                    alpha = max(alpha, entry[0])
                elif entry[1] == 'high':
                    beta = min(beta, entry[0])
            else:
                score = self.minimax(board, alpha, beta, depth - 1, -1)[1]
                if score > value:
                    value = score
                    best_move = move
            alpha = max(value, alpha)
            if alpha >= beta:
                if value <= base_alpha:
                    entry = (value, 'high', depth)
                elif value >= beta:
                    entry = (value, 'low', depth)
                else:
                    entry = (value, 'exact', depth)
                self._transposition_table[board.hash] = entry
                board.un_move(move)
                return best_move, value
            else:
                board.un_move(move)

        board.make_move(best_move)
        hash_value = board.hash
        board.un_move(best_move)
        if value <= base_alpha:
            entry = (value, 'high', depth)
        elif value >= beta:
            entry = (value, 'low', depth)
        else:
            entry = (value, 'exact', depth)
        self._transposition_table[hash_value] = entry
        return best_move, value
