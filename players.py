from typing import Optional
from connect4 import Connect4Game
from decision_tree import DecisionTree
import random


class Player:
    """An abstract class representing a Connect 4 player"""
    is_human: bool

    def make_move(self, game: Connect4Game) -> int:
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

    def make_move(self, game: Connect4Game) -> int:
        """Make a move in the current game"""
        raise NotImplementedError

    def receive_move(self, move: int) -> None:
        """Tells this player what move the other player made
        """
        raise NotImplementedError

