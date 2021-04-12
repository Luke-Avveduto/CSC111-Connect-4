from connect4 import Connect4Game
from players import Player, HumanPlayer


def run_game(red: Player, yellow: Player):
    """Run a Connect 4 game between the two players"""
    game = Connect4Game()

    current_player = red
    while game.get_winner() is None:
        board = game.get_game_board()

        for r in range(len(board) - 1, -1, -1):
            print(*board[r])

        print('The valid moves are:', end=' ' )
        print(*game.get_valid_moves(), sep=', ')

        new_move = current_player.make_move(game)
        game.make_move(new_move)

        if current_player is red:
            current_player = yellow
        else:
            current_player = red

    if game.get_winner() == 1:
        print('RED WINS')
    else:
        print('YELLOW WINS')

    for move in game.get_move_sequence():
        print(move, end=' ')
