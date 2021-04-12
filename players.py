from connect4 import Connect4Game


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
