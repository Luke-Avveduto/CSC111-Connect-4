"""CSC111 Final Project: Exploring Using Graph Based Data Structures to Implement a Connect 4 AI

Module Description
==================

This module contains code that is required to run the project.

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 Brian Cho and Luke Avveduto
"""
from players import HumanPlayer
from players import AIPlayerComplex
from players import RandomPlayer
from visualization import run_game_visualized
from visualization import run_games


def play_with_ai(depth: int = 6) -> None:
    """A function that runs a visualized game of Connect4 between AIPlayerComplex and HumanPlayer.

    depth is the number of moves the AI will look ahead to calculate the best move to be made.
    Higher depth will result in a smarter AI that makes better moves and is harder to beat.
    But, if depth is too high, the AI will take too long to play the move. The function defaults
    the depth to 6, and that is recommended. depth of 7 is also playable, but note that
    the AI will take approximately 40s per move, especially in the beginning stages of the game.
    """
    red = AIPlayerComplex(depth=depth)
    yellow = HumanPlayer()

    run_game_visualized(red, yellow)


def ai_versus_random(depth: int = 6, num_games: int = 10,
                     visualize: bool = True, show_stats: bool = True) -> None:
    """A function that runs num_games games between AIPlayerComplex and RandomPlayer and
    visualizes the game tree generated by those games.

    The visualized game tree will represent all the move sequences played in the games. Each
    node represents a move and the number labelled on the node is the column in which the player
    selected to make a move. The colour of the node represents the player that made the move.
    The last node on each branch indicates the winner of the game. The colour on the last node is
    the player that won, and a green last node indicates a tie.

    num_games is the number of games the players will play. Considering that the AI takes some
    time (varying amount depending on the depth) to make a move, running too many games will take
    a long time. The function defaults to 10 games, and that is recommended. The result of
    running 100 games with default settings is included in the written report.

    depth is the number of moves the AI will look ahead, just like the function play_with_ai.
    Having a high depth does make the AI smarter, but high depth against a RandomPlayer is
    unnecessary. The function defaults to 6, and that is able to win a vast majority of games
    against the RandomPlayer, if not all of them.

    visualize enables each game to be visualized. For a better viewing experience, each game has
    delays in each turn and on the winning page. The default is True, but setting it to False
    will decrease the time needed to run the function. Regardless, the function takes too long
    over a certain number of games, so it is recommended to keep this as True.

    show_stats, when set as True, will show the number of games played, number of red and yellow
    wins, number of ties, and the win rate of each player on the Python console. It is by default
    True and recommended to be True.

    If visualize is True and the game window is forcefully closed using the 'x' button while the
    games are running, the function will stop and only return an instance of the game tree up to
    the point of the force quit. No visualization of the game tree nor stats will be provided.
    """
    red = AIPlayerComplex(depth=depth)
    yellow = RandomPlayer()

    run_games(red, yellow, num_games, visualize, show_stats)
