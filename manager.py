from connect4 import Connect4Game
from players import Player, HumanPlayer, AIPlayerBasic, RandomPlayer
from decision_tree import DecisionTree, write_to_file, build_from_file
import time


def run_game(red: Player, yellow: Player, text: bool = False) -> (list[int], bool):
    """Run a Connect 4 game between the two players"""
    game = Connect4Game()

    current_player = red
    while game.get_winner() is None:
        board = game.get_game_board()

        if text:
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
        current_player.receive_move(new_move)

    if text:
        if game.get_winner() == 1:
            print('RED WINS')
        else:
            print('YELLOW WINS')

    # for move in game.get_move_sequence():
    #     print(move, end=' ')
    return game.get_move_sequence(), game.get_winner() == 1


def train(learning_curve: list[float], output_file: str = 'data/saved_trees/AIBasic.csv') -> None:
    results = []
    d_tree = DecisionTree(move=-1, turn='yellow', subtrees=[])
    random_player = RandomPlayer()
    for t in learning_curve:
        ai = AIPlayerBasic(d_tree, t)
        moves_played, ai_win = run_game(ai, random_player)
        if ai_win:
            moves_played.append(1)
        else:
            moves_played.append(0)

        d_tree.add_game(moves_played)

        results.append(ai_win)

    write_to_file(d_tree, output_file)

    total_win_percent = len([1 for result in results if result])/len(results)

    recent_wins = 0
    if len(results) > 100:
        flipped_results = results[::-1]
        for i in range(0, 100):
            if flipped_results[i]:
                recent_wins += 1

    recent_win_percent = recent_wins/100

    print('Recent Win Percentage:', recent_win_percent)
    print('Total Win Percentage:', total_win_percent)


def run_randoms(n: int, output_file: str = 'data/saved_trees/full_tree.csv') -> None:
    start_time = time.time()
    red = RandomPlayer()
    yellow = RandomPlayer()

    d_tree = DecisionTree(move=-1, subtrees=[], turn='yellow')

    for _ in range(0, n):
        results, red_win = run_game(red, yellow)

        if red_win:
            results.append(1)
        else:
            results.append(0)
        d_tree.add_game(results)

    write_to_file(d_tree, output_file)
    # print(d_tree)
    print('Final Run Time:', time.time() - start_time)


def saved_ai(n: int, input_file: str = 'data/saved_trees/full_tree.csv'):
    d_tree = build_from_file(input_file)
    results = []
    for _ in range(0, n):
        ai = AIPlayerBasic(d_tree, 0.95)
        random_player = RandomPlayer()

        moves_played, ai_win = run_game(ai, random_player)

        results.append(ai_win)

    total_win_percent = len([1 for result in results if result]) / len(results)

    recent_wins = 0
    if len(results) > 100:
        flipped_results = results[::-1]
        for i in range(0, 100):
            if flipped_results[i]:
                recent_wins += 1

    recent_win_percent = recent_wins / 100

    print('Recent Win Percentage:', recent_win_percent)
    print('Total Win Percentage:', total_win_percent)
