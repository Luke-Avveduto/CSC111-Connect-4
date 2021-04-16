"""CSC111 Final Project: Exploring Using Graph Based Data Structures to Implement a Connect 4 AI

Module Description
==================

This module contains the Player abstract class and three implementations of it:
HumanPlayer, RandomPlayer, and AIPlayerComplex. The Player class is designed to
represent a player in a game of connect 4. This means they are given the state of the board in the
form of a Board object, and then must decide on a move to play. All of the provided implementations
do that, but how they achieve that varies massively.

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 Brian Cho and Luke Avveduto
"""
from typing import Optional
import random
import math
from board import Board
import opening_book_gen


class Player:
    """An abstract class representing a Connect 4 player
    """
    # Public Instance Attributes:
    #   - is_human: this is a boolean value that is True when instances of this class require
    #               human input to be played. False otherwise
    is_human: bool

    def make_move(self, board: Board) -> int:
        """Make a move in the current game"""
        raise NotImplementedError


class HumanPlayer(Player):
    """A Connect 4 player that requires an input"""

    def __init__(self) -> None:
        """Creates a new HumanPlayer object for use in connect 4 games.
        """
        self.is_human = True

    def make_move(self, board: Board) -> int:
        """Make a move in the current game.
        Preconditions:
            - board.get_valid_moves() != []
        """

        move = input()
        move = int(move)

        while move not in board.get_valid_moves():
            print("That is not a valid move")
            move = input()
            move = int(move)

        return move


class RandomPlayer(Player):
    """A connect 4 player that makes random valid moves.
    """

    def __init__(self) -> None:
        self.is_human = False

    def make_move(self, board: Board) -> int:
        """Make a move in the current game
        Preconditions:
            - board.get_valid_moves() != []
        """
        return random.choice(board.get_valid_moves())


class AIPlayerComplex(Player):
    """An implementation of the abstract class Player that uses a combination of the
    minimax algorithm, alpha-beta pruning, and a transposition table in order to chose what move it
    will make. This implementation works well with depth between 5 and 7. While it will technically
    work with any depth level, values below 5 will not produce very accurate moves while values
    above 7 will result in the AI taking several minutes to make a move, especially in the beginning
    of the game, so use at your own risk.

    Details on the minimax algorithm can be found here: https://en.wikipedia.org/wiki/Minimax
    Details on alpha-beta pruning can be found here: https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
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
    #   - _depth: this is the depth that minimax algorithm will use. This is measure of how many
    #            moves ahead the AI will look on any given turn.
    _depth: int
    _transposition_table: dict[int:(int, str, int)]

    def __init__(self, depth: int = 6, opening_book: Optional[str] = None) -> None:
        """Creates a new instance of the AIPlayerComplex class. Reads in the values in it's opening
        book. If an opening book is given, it will be loaded into it's transposition table.

        Preconditions:
            - depth >= 0
            - opening_book points to a csv file created by opening_book_gen.save_opening_book
        """
        self.is_human = False
        self._depth = depth

        if opening_book is None:
            if depth == 5:
                path = 'data\opening_books\opening_book_5.csv'
                self._transposition_table = opening_book_gen.load_opening_book(path)
            elif depth == 6:
                path = 'data\opening_books\opening_book_6.csv'
                self._transposition_table = opening_book_gen.load_opening_book(path)
            elif depth == 7:
                path = 'data\opening_books\opening_book_7.csv'
                self._transposition_table = opening_book_gen.load_opening_book(path)
        else:
            self._transposition_table = opening_book_gen.load_opening_book(opening_book)

    def make_move(self, board: Board) -> int:
        """Returns a move that can be played in the game represented by the 'board' argument.
        Move selection is done using the 'minimax' function which uses the minimax algorithm with
        a depth of self.depth to decide on the best move to play.
        """
        move, evalutation = self.minimax(board, -math.inf, math.inf, self._depth, 1)
        return move

    def minimax(self, board: Board, alpha: int, beta: int, depth: int, color: int) -> (int, int):
        """This function implements the minimax algorithm with alpha-beta pruning and a
        transposition table with a depth of 'depth'. This algorithm uses recursion to explore the
        tree like structure of all the possible games that could happen from the current 'board'
        state and will eventually return a tuple of ints containing the best move in for the player
        with color 'color' and the evaluation of how good the resulting position will be
        for the player.

        While board is mutated many MANY times during the running of this function, it when the
        function is finished, it will always be in the exact same state is was in when it was
        first called.

        Preconditions:
            - depth >= 0
            - color in {-1, 1}
        """
        possible_moves = board.get_valid_moves()

        for move in possible_moves:  # Checks to see if there is a win in any of the next moves
            board.make_move(move)  # Mutating the board in this way is faster than creating copies
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
            board.un_move(move)  # Undoes the move so the next moves can be tried

        if len(possible_moves) == 0 or depth == 0:
            if depth == 0:  # If depth is 0, we must stop recursion use a heuristic evaluation
                return None, board.evaluate_score(color)
            else:
                return None, 0  # Game is a draw

        if color == 1:  # AI/red is color 1
            return self._max_player(board, alpha, beta, depth)

        else:  # Otherwise, it is yellows/human players turn
            return self._min_player(board, alpha, beta, depth)

    def _min_player(self, board: Board, alpha: int, beta: int, depth: int) -> (int, int):
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

            # Checks to see if this board is in the transposition table, if it is,
            # We can save time by not computing it again
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
            else:  # If it's not in the table, we need to calculate it
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

                # Saves this value into the table so it doesn't need to be calculated again
                self._transposition_table[board.hash] = entry
                board.un_move(move)
                return move, value
            else:
                board.un_move(move)

        # Mutates the board, and thus it's hash, to save and use to store in the table
        board.make_move(best_move)
        hash_value = board.hash
        board.un_move(best_move)

        if value <= alpha:
            entry = (value, 'high', depth)
        elif value >= base_beta:
            entry = (value, 'low', depth)
        else:
            entry = (value, 'exact', depth)

        # Saves this value into the table so it doesn't need to be calculated again
        self._transposition_table[hash_value] = entry
        return best_move, value

    def _max_player(self, board: Board, alpha: int, beta: int, depth: int) -> (int, int):
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

            # Checks to see if this board is in the transposition table, if it is,
            # We can save time by not computing it again
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
            else:  # If it's not in the table, we need to calculate it
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

                # Saves this value into the table so it doesn't need to be calculated again
                self._transposition_table[board.hash] = entry
                board.un_move(move)
                return best_move, value
            else:
                board.un_move(move)

        # Mutates the board, and thus it's hash, to save and use to store in the table
        board.make_move(best_move)
        hash_value = board.hash
        board.un_move(best_move)

        if value <= base_alpha:
            entry = (value, 'high', depth)
        elif value >= beta:
            entry = (value, 'low', depth)
        else:
            entry = (value, 'exact', depth)

        # Saves this value into the table so it doesn't need to be calculated again
        self._transposition_table[hash_value] = entry
        return best_move, value


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['random', 'math', 'typing', 'board', 'opening_book_gen'],
        # the names (strs) of imported modules
        'allowed-io': [],
        # the names (strs) of functions that call print/open/input
        'max-line-length': 150,
        'disable': ['E1136', 'E9989', 'W1401']
    })
