from typing import Optional
from connect4 import Connect4Game
from decision_tree import DecisionTree
import random
from board import Board
import math

class Player:
    """An abstract class representing a Connect 4 player"""
    is_human: bool

    def make_move(self, board: Board):
        """Make a move in the current game"""
        raise NotImplementedError

    def receive_move(self, move: int) -> None:
        """Tells this player what move the other player made
        """
        raise NotImplementedError


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

    def receive_move(self, move: int) -> None:
        return None


class RandomPlayer(Player):
    """A connect 4 player that makes random valid moves
    """

    def make_move(self, game: Connect4Game) -> int:
        """Make a move in the current game
        """
        return random.choice(game.get_valid_moves())

    def receive_move(self, move: int) -> None:
        return None


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
    _transposition_table: dict[int:int]

    def __init__(self) -> None:
        """Creates a new instance of the AIPlayerComplex class. Reads in the values in it's opening
        book.
        """
        self.is_human = False

    def make_move(self, board: Board) -> int:
        """Make a move in the current game"""
        max_score = -math.inf
        best_move = None
        for move in board.get_valid_moves():
            score = self.evaluate(move, board, -math.inf, math.inf)
            if score > max_score:
                max_score = score
                best_move = move
        return best_move

    def receive_move(self, move: int) -> None:
        """Tells this player what move the other player made
        """
        raise NotImplementedError

    def evaluate(self, move: int, board: Board, alpha: float, beta: float) -> int:
        board.make_move(move)
        score = board.get_winner()
        if score is not None:
            board.un_move(move)
            return score
        value = -math.inf

        for next_move in board.get_valid_moves():  # Yellows moves
            value = max(value, -self.evaluate(next_move, board, -beta, -alpha))
            alpha = max(alpha, value)
            if alpha >= beta:
                board.un_move(move)
                return value
        board.un_move(move)
        return value

    def find_best_move(self, board: Board) -> int:
        if board.move_number == 6*7:  # Checks for a draw
            return 0

        for move in board.get_valid_moves():
            board.make_move(move)
            winner = board.get_winner()
            board.un_move(move)
            if winner is not None:
                return winner

        for move in board.get_valid_moves():
            board.make_move(move)
            winner = -self.find_best_move(board)



