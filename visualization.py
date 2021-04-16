"""CSC111 Final Project: Exploring Using Graph Based Data Structures to Implement a Connect 4 AI

Module Description
==================

This module contains classes and functions that visualize a game of Connect 4. The games are
visualized through tkinter, which is a python library that allows for the creation of GUI.
This module also contains some functions that generate a game tree based on previous
games of Connect4 and visualizes the completed game tree. The game tree is created using
the library networkx, which has a built-in tree implementation and its visualization. Matplotlib
is also used in conjunction with networkx to visualize the tree.

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 Brian Cho and Luke Avveduto
"""
import tkinter
from connect4 import Connect4Game
from players import Player
from typing import Optional
import numpy as np
import networkx as nx
import time
import matplotlib.pyplot as plt
from connect4 import run_game


class VisualizedConnect4:
    """
    A class that handles the visualization for the given Connect4Game.

    Representation Invariants:
        - self._window is a valid instance of tkinter.TK (should not be a closed window)
        - self._board is a 6x7 2d array that represents the state of the game board
        - self._human_move is an int between 0 and 6, inclusive, or None
        - If self._is_replay is True, then self._exit_flag is True
    """
    # Private Instance Attributes:
    #   - _window:
    #       The tkinter window that is used to hold the tkinter.Canvas object
    #   - _game:
    #       The instance of the object Connect4Game. The state of the game
    #       is no winner or tie or red win or yellow win at all times.
    #   - _canvas:
    #       The tkinter.Canvas object that is used to draw elements of the game,
    #       such as game board and occupied slots.
    #   - _board:
    #       The 2d array that represents the current state of the game board.
    #       This array is always 6x7 in size and the value at each slot if 0 or -1 or 1.
    #   - _human_move:
    #       The move that a HumanPlayer just made. Normally, this attribute is None.
    #       When the HumanPlayer selects a move, it is an int between 0 and 6.
    #   - _exit_flag:
    #       Boolean value indicating that the quit or replay button has been pressed.
    #       True when the quit or replay button has been pressed and False otherwise.
    #   - is_replay:
    #       Boolean value indicating that the replay button has been pressed.
    #       True when the replay button has been pressed and False otherwise
    _window: tkinter.Tk
    _game: Connect4Game
    _canvas: tkinter.Canvas
    _board: np.array
    _human_move: Optional[int]
    _exit_flag: bool
    is_replay: bool

    def __init__(self, window: tkinter.Tk, red: Player, yellow: Player,
                 board: list[list[int]] = None, no_buttons: bool = None):
        """Initialize a new visualized connect 4 game starting at the board state provided by board

        If board is None, the game starts with an empty board.
        If no_human is True, both players, red and yellow, are not instances if HumanPlayer

        Instance Attributes:
            - window: an instance if tkinter.Tk
            - red: the red player of the game
            - yellow: the yellow player of the game
            - board: the starting position of the game
            - no_button: boolean indicating whether the visualization should contain
                         replay and quit buttons

        Preconditions:
            - If no_human is True, red and yellow are NOT instances of HumanPlayer
            - len(board) == 6
            - all(len(board[col]) == 7 for col in range(len(board)))
        """

        # Setting window size and initializing canvas
        self._window = window
        self._window.geometry('700x700')
        self._canvas = tkinter.Canvas(self._window, width=700, height=700)
        self._canvas.pack()

        # self._exit_flag and self._is_replay are both False by default
        self._exit_flag = False
        self.is_replay = False

        # check whether a human is playing the game
        if no_buttons is None:
            no_human = not red.is_human and not yellow.is_human
        else:
            no_human = no_buttons

        self._window.protocol('WM_DELETE_WINDOW', self.quit)

        # If a human is playing the game, create quit and replay buttons
        if not no_human:
            button_quit = tkinter.Button(self._canvas, text='Quit', command=self.quit)
            button_quit.place(x=600, y=40)
            button_replay = tkinter.Button(self._canvas, text='Replay', command=self.replay)
            button_replay.place(x=550, y=40)

        # If board is not None, initialize game to the given state of gameboard
        # otherwise, start a fresh game
        if board is not None:
            self._game = Connect4Game(board)
        else:
            self._game = Connect4Game()
        self._board = self._game.get_game_board()

        self._draw_board()
        self._update_board()

        current_player = red
        self._human_move = None

        if not self._exit_flag:
            self._window.update()
            self._window.update_idletasks()
            self._canvas.update()
            self._canvas.update_idletasks()

        # While no winner has been decided, keep making moves
        while self._game.get_winner() is None:

            # If the current_player is HumanPlayer, take move as the click input
            # otherwise, call the make_move function on the respective player
            # print(self._board.evaluate_score())
            if current_player.is_human:
                text = self._canvas.create_text(100, 20, font='Times 20 italic bold',
                                                text="Human's Turn")
                self._canvas.update()
                move = self._check_input()
            else:
                text = self._canvas.create_text(100, 20, font='Times 20 italic bold',
                                                text="AI is thinking")
                self._canvas.update()
                move = current_player.make_move(self._game.get_game_board())
                self._canvas.delete(text)

            if move is None:
                break

            # Do not make move until the received move is valid
            while move not in self._game.get_valid_moves():
                if self._exit_flag:
                    break
                if current_player.is_human:
                    move = self._check_input()
                else:
                    move = current_player.make_move(self._game.get_game_board())

            self._canvas.delete(text)

            if not self._exit_flag:
                self._game.make_move(move)

            # switch players every turn
            if current_player is red:
                current_player = yellow
            else:
                current_player = red

            if not self._exit_flag:
                self._update_board()
                self._window.update()
                self._canvas.update()
            else:
                break

            # add a delay if no human is playing the game
            if no_human:
                time.sleep(.1)

        if not self._exit_flag:
            self._update_board()

        # indicate winner
        if self._game.get_winner() == 1:
            self._canvas.create_text(100, 20, font='Times 20 italic bold',
                                     text="Red Wins")
            self._canvas.update()
        elif self._game.get_winner() == -1:
            self._canvas.create_text(100, 20, font='Times 20 italic bold',
                                     text="Yellow Wins")
            self._canvas.update()
        elif self._game.get_winner() == 0:
            self._canvas.create_text(100, 20, font='Times 20 italic bold',
                                     text="Tie")
            self._canvas.update()

        # keep the win screen up for a little longer
        if no_human:
            time.sleep(.8)
            self._window.destroy()
        elif not self._exit_flag:
            self._window.mainloop()

    def get_move_sequence(self) -> list[int]:
        """A function that returns all the moves that have been made in the game

        The last item in the list indicates the winner of the game
        1 if red has won the game
        -1 if yellow has won the game
        0 if the game was a tie

        Precondition:
            - self._game.get_winner is not None
        """
        return self._game.get_move_sequence()

    def _check_input(self) -> Optional[int]:
        """A function that returns the human input (click) made on the column

        Returns the number of the column that was clicked on
        Returns None if no click has been made
        """
        while self._human_move is None:
            if self._exit_flag:
                return None
            else:
                self._window.update()
        move_copy = self._human_move
        self._human_move = None
        return move_copy

    def _draw_board(self) -> None:
        """A function that draws the game board on the canvas"""
        col1 = self._canvas.create_rectangle(0, 100, 100, 700, fill='#9e9e9e')
        self._canvas.tag_bind(col1, '<Button-1>', self.on_col1_click)
        col2 = self._canvas.create_rectangle(100, 100, 200, 700, fill='#666666')
        self._canvas.tag_bind(col2, '<Button-1>', self.on_col2_click)
        col3 = self._canvas.create_rectangle(200, 100, 300, 700, fill='#9e9e9e')
        self._canvas.tag_bind(col3, '<Button-1>', self.on_col3_click)
        col4 = self._canvas.create_rectangle(300, 100, 400, 700, fill='#666666')
        self._canvas.tag_bind(col4, '<Button-1>', self.on_col4_click)
        col5 = self._canvas.create_rectangle(400, 100, 500, 700, fill='#9e9e9e')
        self._canvas.tag_bind(col5, '<Button-1>', self.on_col5_click)
        col6 = self._canvas.create_rectangle(500, 100, 600, 700, fill='#666666')
        self._canvas.tag_bind(col6, '<Button-1>', self.on_col6_click)
        col7 = self._canvas.create_rectangle(600, 100, 700, 700, fill='#9e9e9e')
        self._canvas.tag_bind(col7, '<Button-1>', self.on_col7_click)

    def _update_board(self) -> None:
        """A function that updates the canvas based on the current state of the game"""
        for i in range(len(self._board.board_array)):
            for j in range(len(self._board.board_array[i])):
                if self._board.board_array[i][j] == 1:
                    self._canvas.create_oval(j * 100, 600 - i * 100, 100 + j * 100,
                                             100 + (600 - i * 100), fil='red')
                elif self._board.board_array[i][j] == -1:
                    self._canvas.create_oval(j * 100, 600 - i * 100, 100 + j * 100,
                                             100 + (600 - i * 100), fil='yellow')

    def quit(self) -> None:
        """A function that exits the game.
        Triggered by the activation of the quit button
        """
        self._exit_flag = True
        self._window.quit()
        self._window.destroy()

    def replay(self) -> None:
        """A function that exits the game and allows for replay of a fresh game
        triggered by the activation of the replay button
        """
        self._exit_flag = True
        self.is_replay = True
        self._window.quit()
        self._window.destroy()

    def on_col1_click(self, event) -> None:
        """A function that records the click input of the human
        Triggered by the click of the first column on the game board
        """
        self._human_move = 0

    def on_col2_click(self, event) -> None:
        """A function that records the click input of the human
        Triggered by the click of the second column on the game board
        """
        self._human_move = 1

    def on_col3_click(self, event) -> None:
        """A function that records the click input of the human
        Triggered by the click of the third column on the game board
        """
        self._human_move = 2

    def on_col4_click(self, event) -> None:
        """A function that records the click input of the human
        Triggered by the click of the fourth column on the game board
        """
        self._human_move = 3

    def on_col5_click(self, event) -> None:
        """A function that records the click input of the human
        Triggered by the click of the fifth column on the game board
        """
        self._human_move = 4

    def on_col6_click(self, event) -> None:
        """A function that records the click input of the human
        Triggered by the click of the sixth column on the game board
        """
        self._human_move = 5

    def on_col7_click(self, event) -> None:
        """A function that records the click input of the human
        Triggered by the click of the seventh column on the game board
        """
        self._human_move = 6


def add_game(game_tree: nx.DiGraph, root, game_sequence: list[int], variant) -> None:
    """A function that adds a sequences of moves that were made in a Connect4Game

    If a move sequence already exists in the tree, no branches will be added.
    Branches are only added when there is a variation from the existing branch

    Instance Attributes:
        - game_tree: tree in which the move sequence will be added to
        - root: the value of the top-most level node in the tree
        - game_sequence: the list of integers that represent the moves that were made in the game
                         the last entry in the list indicates the winner
        - variant: integer indicating the number of the game to be added to the tree

    Preconditions:
        - nx.is_tree(game_tree)
        - root in game_tree.nodes
        - the game tree contains variant number of move sequences
    """

    prev_variant = None

    # searching for the first element in the sequence that is not already in the tree
    for i in range(len(game_sequence)):
        if any((game_sequence[i], i, v) in game_tree for v in range(variant)):
            for v in range(variant):
                if (game_sequence[i], i, v) in game_tree:
                    prev_variant = v
        else:
            # if the first branching move is found and is 0
            if i == 0:
                game_tree.add_node((game_sequence[i], i, variant))
                game_tree.add_edge(root, (game_sequence[i], i, variant))
                for j in range(i + 1, len(game_sequence)):
                    if j == len(game_sequence) - 1:
                        if game_sequence[j] == 1:
                            game_tree.add_node(('RED W', variant))
                            game_tree.add_edge((game_sequence[j - 1], j - 1, variant),
                                               ('RED W', variant))
                        elif game_sequence[j] == -1:
                            game_tree.add_node(('YEL W', variant))
                            game_tree.add_edge((game_sequence[j - 1], j - 1, variant),
                                               ('YEL W', variant))
                        else:
                            game_tree.add_node(('TIE', variant))
                            game_tree.add_edge((game_sequence[j - 1], j - 1, variant),
                                               ('TIE', variant))
                    else:
                        game_tree.add_node((game_sequence[j], j, variant))
                        game_tree.add_edge((game_sequence[j - 1], j - 1, variant),
                                           (game_sequence[j], j, variant))
                return
            # if the move sequence isn't already in game_tree
            elif i != len(game_sequence) - 1:
                game_tree.add_node((game_sequence[i], i, variant))
                game_tree.add_edge((game_sequence[i - 1], i - 1, prev_variant),
                                   (game_sequence[i], i, variant))
                for j in range(i + 1, len(game_sequence)):
                    if j == len(game_sequence) - 1:
                        if game_sequence[j] == 1:
                            game_tree.add_node(('RED W', variant))
                            game_tree.add_edge((game_sequence[j - 1], j - 1, variant),
                                               ('RED W', variant))
                        elif game_sequence[j] == -1:
                            game_tree.add_node(('YEL W', variant))
                            game_tree.add_edge((game_sequence[j - 1], j - 1, variant),
                                               ('YEL W', variant))
                        else:
                            game_tree.add_node(('TIE', variant))
                            game_tree.add_edge((game_sequence[j - 1], j - 1, variant),
                                               ('TIE', variant))
                    else:
                        game_tree.add_node((game_sequence[j], j, variant))
                        game_tree.add_edge((game_sequence[j - 1], j - 1, variant),
                                           (game_sequence[j], j, variant))
                return


def run_game_visualized(red: Player, yellow: Player):
    """Runs a game of Connect 4 using a GUI"""
    window = tkinter.Tk()
    game = VisualizedConnect4(window, red, yellow)
    while game.is_replay:
        window = tkinter.Tk()
        game = VisualizedConnect4(window, red, yellow)


def run_games(red: Player, yellow: Player, n: int,
              visualization: bool = False, show_stats: bool = False) -> nx.DiGraph:
    """Runs n number of games of Connect4 between red and yellow,
    then visualizes and returns the game tree created by the move sequences

    If visualization is True, each game will be visualized using the VisualizedConnect4 class.
    The visualization will be slowed down each move and on the win screen to allow for
    better viewing experience. This will slow the function down significantly. When running
    a large number of games, it is recommended to set visualization to False.
    Also, if one of the players is a HumanPlayer, it is recommended to set visualization to True
    or otherwise the player input will be taken through the python console as well as
    the visualization of the game itself at every stage.

    Instance Attributes:
        - red: the red player of the Connect4 games
        - yellow: the yellow player of the Connect4 games
        - n: number of Connect4 games to run
        - visualization: boolean indicating whether each game will be visualized or not
        - show_stats: boolean indicating whether to show the stats of the games

    Preconditions:
        - n >= 0
    """
    # initialize game tree
    game_tree = nx.DiGraph()
    game_tree.add_node('START')
    num_red_wins = 0
    num_yellow_wins = 0

    if visualization:
        for i in range(n):
            window = tkinter.Tk()
            game = VisualizedConnect4(window, red, yellow, no_buttons=True)
            game_moves = game.get_move_sequence()
            if game_moves[len(game_moves) - 1] == 1:
                num_red_wins += 1
            elif game_moves[len(game_moves) - 1] == -1:
                num_yellow_wins += 1
            add_game(game_tree, 'START', game_moves, i)
    else:
        if red.is_human or yellow.is_human:
            text = True
        else:
            text = False

        for i in range(n):
            game_moves = run_game(red, yellow, text=text)
            if game_moves[len(game_moves) - 1] == 1:
                num_red_wins += 1
            elif game_moves[len(game_moves) - 1] == -1:
                num_yellow_wins += 1
            add_game(game_tree, 'START', game_moves, i)

    labels = {}
    colour_map = []
    for node in game_tree.nodes():
        if node[0] == 'RED W':
            colour_map.append('red')
        elif node[0] == 'YEL W':
            colour_map.append('yellow')
        elif node[0] == 'TIE':
            colour_map.append('green')
        elif isinstance(node[1], int) and node[1] % 2 == 0:
            colour_map.append('red')
        elif isinstance(node[1], int) and node[1] % 2 != 0:
            colour_map.append('yellow')
        else:
            colour_map.append('green')

        if node[0] == 'RED W':
            labels[node] = 'RED W'
            colour_map.pop()
            colour_map.append('red')
        elif node[0] == 'YEL W:':
            labels[node] = 'YEL W'
            colour_map.pop()
            colour_map.append('yellow')
        elif node[0] == 'TIE':
            labels[node] = 'TIE'
            colour_map.pop()
            colour_map.append('green')
        else:
            labels[node] = node[0]

    plt.title('Game Results')
    pos = tree_pos(game_tree, 'START', width=1, vert_gap=0.2)
    nx.draw(game_tree, node_color=colour_map, pos=pos, labels=labels, arrows=True)
    plt.show()

    if show_stats:
        red_winrate = (num_red_wins / n) * 100
        yellow_winrate = (num_yellow_wins / n) * 100

        print('Number of Games: ' + str(n))
        print('Number of Red Wins: ' + str(num_red_wins))
        print('Number of Yellow Wins: ' + str(num_yellow_wins))
        print('Number of Ties: ' + str(n - num_red_wins - num_yellow_wins))
        print('Red Win Rate: ' + str(red_winrate))
        print('Yellow Win Rate: ' + str(yellow_winrate))

    return game_tree


def tree_pos(g: nx.DiGraph, root, width: float = 1.0, vert_gap: float = 0.2,
             vert_loc: float = 0, xcentre: float = 0.5) -> dict:
    """A function that calculates the position of each node in the tree G when it is visualized.
    Returns the position of each node as a dictionary.

    Instance Attributes:
        - G: the tree to be visualized
        - root: the root value of the tree
        - width: horizontal space occupied by the tree
        - vert_gap: the gap between each hierarchy
        - vert_loc: the vertical location of the root of the tree
        - xcentre: the horizontal location of the root of the tree

    Preconditions:
        - nx.is_tree(G)
        - root is an existing value in the tree
    """
    return _tree_pos(g, root, width, vert_gap, vert_loc, xcentre, None)


def _tree_pos(g, root, width, vert_gap, vert_loc, xcentre, pos,) -> dict:
    """Recursive helper function for tree_pos that returns a dictionary of node positions"""

    if pos is None:
        pos = {root: (xcentre, vert_loc)}
    else:
        pos[root] = (xcentre, vert_loc)

    subtrees = list(g.neighbors(root))

    if len(subtrees) != 0:
        dx = width / len(subtrees)
        next_pos = xcentre - width / 2 - dx / 2
        for subtree in subtrees:
            next_pos += dx
            pos = _tree_pos(g, subtree, dx, vert_gap, vert_loc - vert_gap, next_pos, pos)

    return pos
