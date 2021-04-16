"""CSC111 Final Project: Exploring Using Graph Based Data Structures to Implement a Connect 4 AI

Module Description
==================

This module contains classes and functions that visualize a game of Connect 4.

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 Brian Cho and Luke Avveduto
"""
import tkinter
from connect4 import Connect4Game
from players import Player
from players import HumanPlayer
from players import AIPlayerComplex
from players import RandomPlayer
from typing import Optional
import numpy as np
import networkx as nx
import time
import matplotlib.pyplot as plt
import random

class Game:
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

    def __init__(self, window, red: Player, yellow: Player,
                 board: list[list[int]] = None, no_human: bool = False):
        """Initialize a new visualized connect 4 game starting at the board state provided by board

        If board is None, the game starts with an empty board.
        If no_human is True, both players, red and yellow, are not instances if HumanPlayer

        Preconditions:
            - If no_human is True, red and yellow are NOT instances of HumanPlayer
            - len(board) == 6
            - all(len(board[col]) == 7 for col in range(len(board)))
        """

        # Setting window size and intializing canvas
        self._window = window
        self._window.geometry('700x700')
        self._canvas = tkinter.Canvas(self._window, width=700, height=700)
        self._canvas.pack()

        # self._exit_flag and self._is_replay are both False by default
        self._exit_flag = False
        self.is_replay = False

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
            if current_player.is_human:
                move = self._check_input()
            else:
                move = current_player.make_move(self._game.get_game_board())

            if move is None:
                break

            while move not in self._game.get_valid_moves():
                if self._exit_flag:
                    break
                if current_player.is_human:
                    move = self._check_input()
                else:
                    move = current_player.make_move(self._game.get_game_board())

            if not self._exit_flag:
                self._game.make_move(move)

            if current_player is red:
                current_player = yellow
            else:
                current_player = red

            if not self._exit_flag:
                self._update_board()

            if self._exit_flag:
                break

            self._window.update()
            self._canvas.update()

            if no_human:
                time.sleep(.1)

        if not self._exit_flag:
            self._update_board()

        if self._game.get_winner() == 1:
            self._canvas.create_text(100, 20, font='Times 20 italic bold',
                                     text="Red Wins")
            self._canvas.update()
        elif self._game.get_winner() == -1:
            self._canvas.create_text(100, 20, font='Times 20 italic bold',
                                     text="Yellow Wins")
            self._canvas.update()

        if no_human:
            time.sleep(.8)
            self._window.destroy()
        else:
            self._window.mainloop()

    def get_move_sequence(self) -> list[int]:
        return self._game.get_move_sequence()

    def _check_input(self) -> Optional[int]:

        while self._human_move is None:
            if self._exit_flag:
                return None
            else:
                self._window.update()
        move_copy = self._human_move
        self._human_move = None
        return move_copy

    def _draw_board(self) -> None:

        col1 = self._canvas.create_rectangle(0, 100, 100, 700, fill='#9e9e9e')
        self._canvas.tag_bind(col1, '<Button-1>', self.oncol1click)
        col2 = self._canvas.create_rectangle(100, 100, 200, 700, fill='#666666')
        self._canvas.tag_bind(col2, '<Button-1>', self.oncol2click)
        col3 = self._canvas.create_rectangle(200, 100, 300, 700, fill='#9e9e9e')
        self._canvas.tag_bind(col3, '<Button-1>', self.oncol3click)
        col4 = self._canvas.create_rectangle(300, 100, 400, 700, fill='#666666')
        self._canvas.tag_bind(col4, '<Button-1>', self.oncol4click)
        col5 = self._canvas.create_rectangle(400, 100, 500, 700, fill='#9e9e9e')
        self._canvas.tag_bind(col5, '<Button-1>', self.oncol5click)
        col6 = self._canvas.create_rectangle(500, 100, 600, 700, fill='#666666')
        self._canvas.tag_bind(col6, '<Button-1>', self.oncol6click)
        col7 = self._canvas.create_rectangle(600, 100, 700, 700, fill='#9e9e9e')
        self._canvas.tag_bind(col7, '<Button-1>', self.oncol7click)

    def _update_board(self) -> None:

        for i in range(len(self._board.board_array)):
            for j in range(len(self._board.board_array[i])):
                if self._board.board_array[i][j] == 1:
                    self._canvas.create_oval(j * 100, 600 - i * 100, 100 + j * 100,
                                             100 + (600 - i * 100), fil='red')
                elif self._board.board_array[i][j] == -1:
                    self._canvas.create_oval(j * 100, 600 - i * 100, 100 + j * 100,
                                             100 + (600 - i * 100), fil='yellow')

    def quit(self) -> None:
        self._exit_flag = True
        self._window.destroy()

    def replay(self) -> None:
        self._exit_flag = True
        self.is_replay = True
        self._window.destroy()

    def oncol1click(self, event) -> None:
        self._human_move = 0

    def oncol2click(self, event) -> None:
        self._human_move = 1

    def oncol3click(self, event) -> None:
        self._human_move = 2

    def oncol4click(self, event) -> None:
        self._human_move = 3

    def oncol5click(self, event) -> None:
        self._human_move = 4

    def oncol6click(self, event) -> None:
        self._human_move = 5

    def oncol7click(self, event) -> None:
        self._human_move = 6


def add_game(game_tree: nx.DiGraph, root, game_sequence: list[int], variant) -> None:

    prev_variant = -1

    for i in range(len(game_sequence)):
        if all((game_sequence[i], i, v) not in game_tree for v in range(variant)):
            if i == 0:
                game_tree.add_node((game_sequence[i], i, variant))
                game_tree.add_edge('START', (game_sequence[i], i, variant))
                for j in range(i + 1, len(game_sequence)):
                    if j == len(game_sequence) - 1:
                        if game_sequence[j] == 1:
                            game_tree.add_node(('RED W', variant))
                            game_tree.add_edge((game_sequence[j - 1], j - 1, variant),
                                               ('RED W', variant))
                        elif game_sequence[j] == 1:
                            game_tree.add_node(('YEL W', variant))
                            game_tree.add_edge((game_sequence[j - 1], j - 1, variant),
                                               ('YEL W', variant))
                        else:
                            game_tree.add_node(('TIE', variant))
                            game_tree.add_edge((game_sequence[j - 1], j - 1, variant),
                                               ('TIE', variant))
                    else:
                        game_tree.add_node((game_sequence[j], j, variant))
                        game_tree.add_edge((game_sequence[j - 1], j - 1, variant), (game_sequence[j], j, variant))
                return
            else:
                game_tree.add_node((game_sequence[i], i, variant))
                game_tree.add_edge((game_sequence[i - 1], i - 1, prev_variant),
                                   (game_sequence[i], i, variant))
                for j in range(i + 1, len(game_sequence)):
                    if j == len(game_sequence) - 1:
                        if game_sequence[j] == 1:
                            game_tree.add_node(('RED W', variant))
                            game_tree.add_edge((game_sequence[j - 1], j - 1, variant),
                                               ('RED W', variant))
                        elif game_sequence[j] == 1:
                            game_tree.add_node(('YEL W', variant))
                            game_tree.add_edge((game_sequence[j - 1], j - 1, variant),
                                               ('YEL W', variant))
                        else:
                            game_tree.add_node(('TIE', variant))
                            game_tree.add_edge((game_sequence[j - 1], j - 1, variant),
                                               ('TIE', variant))
                    else:
                        game_tree.add_node((game_sequence[j], j, variant))
                        game_tree.add_edge((game_sequence[j - 1], j - 1, variant), (game_sequence[j], j, variant))
                return
        else:
            for v in range(variant):
                if (game_sequence[i], i, v) in game_tree:
                    prev_variant = v


def run_game(red: Player, yellow: Player):
    """Runs a game of Connect 4 using a GUI"""
    window = tkinter.Tk()
    game = Game(window, red, yellow)
    while game.is_replay:
        window = tkinter.Tk()
        game = Game(window, red, yellow)

def test():
    red = RandomPlayer()
    yellow = RandomPlayer()
    for _ in range(10):
        window = tkinter.Tk()
        game = Game(window, red, yellow, no_human=True)

def run_games(red: Player, yellow: Player, n:int,
              visualization: bool = False, show_stats: bool = False) -> nx.DiGraph:
    """Runs n number of games between red and yellow and returns the game tree"""
    if red is not HumanPlayer and yellow is not HumanPlayer:
        no_human = True
    else:
        no_human = False

    if visualization:
        game_tree = nx.DiGraph()
        game_tree.add_node('START')
        for i in range(n):
            window = tkinter.Tk()
            game = Game(window, red, yellow, no_human=no_human)
            game_moves = game.get_move_sequence()
            add_game(game_tree, 'START', game_moves, i)
        labels = {}
        colour_map = []
        for node in game_tree.nodes():
            if isinstance(node[1], int) and node[1] % 2 == 0:
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
        pos = hierarchy_pos(game_tree, 'START', width=0.5, vert_gap=100)
        nx.draw(game_tree, node_color=colour_map, pos=pos, labels=labels, arrows=True)
        plt.show()
        return game_tree



def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    '''
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723.
    Licensed under Creative Commons Attribution-Share Alike

    If the graph is a tree this will return the positions to plot this in a
    hierarchical layout.

    G: the graph (must be a tree)

    root: the root node of current branch
    - if the tree is directed and this is not given,
      the root will be found and used
    - if the tree is directed and this is given, then
      the positions will be just for the descendants of this node.
    - if the tree is undirected and not given,
      then a random choice will be used.

    width: horizontal space allocated for this branch - avoids overlap with other branches

    vert_gap: gap between levels of hierarchy

    vert_loc: vertical location of root

    xcenter: horizontal location of root
    '''
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(
                iter(nx.topological_sort(G)))  # allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0.0, xcenter=0.5, pos=None,
                       parent=None):
        '''
        see hierarchy_pos docstring for most arguments

        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed

        '''

        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)
        if len(children) != 0:
            dx = width / len(children)
            nextx = xcenter - width / 2 - dx / 2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                     vert_loc=vert_loc - vert_gap, xcenter=nextx,
                                     pos=pos, parent=root)
        return pos

    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)


TEST = [[0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, -1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, -1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, -1, 0, 0, 0]]
