from typing import Optional
from connect4 import Connect4Game
from decision_tree import DecisionTree
import random


class Player:
    """An abstract class representing a Connect 4 player"""

    def make_move(self, game: Connect4Game) -> int:
        """Make a move in the current game"""
        raise NotImplementedError


class HumanPlayer(Player):
    """A Connect 4 player that requires an input"""

    def make_move(self, game: Connect4Game) -> int:
        """Make a move in the current game"""
        move = input()
        move = int(move)

        while move not in game.get_valid_moves():
            print("That is not a valid move")
            move = input()
            move = int(move)

        return move


class RandomPlayer(Player):
    """A connect 4 player that makes random valid moves
    """

    def make_move(self, game: Connect4Game) -> int:
        """Make a move in the current game
        """
        return random.choice(game.get_valid_moves())


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
            return self._d_tree.get_best_move()
