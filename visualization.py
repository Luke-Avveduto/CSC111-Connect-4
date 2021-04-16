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
import sys
# import matplotlib.pyplot as plt
# from test import hierarchy_pos

class Game:

    window: tkinter.Tk
    game: Connect4Game
    canvas: tkinter.Canvas
    board: np.array
    human_move: Optional[int]
    exit_flag: bool
    is_replay: bool

    def __init__(self, window, red: Player, yellow: Player, board: list[list[int]] = None, no_human: bool = False):
        # sys.setrecursionlimit(500000000)
        self.window = window
        self.window.geometry('700x700')
        self.canvas = tkinter.Canvas(self.window, width=700, height=700)
        self.canvas.pack()
        self.exit_flag = False
        self.is_replay = False
        if not no_human:
            button_quit = tkinter.Button(self.canvas, text='Quit', command=self.quit)
            button_quit.place(x=600, y=40)
            button_replay = tkinter.Button(self.canvas, text='Replay', command=self.replay)
            button_replay.place(x=550, y=40)

        if board is not None:
            self.game = Connect4Game(board)
        else:
            self.game = Connect4Game()
        self.board = self.game.get_game_board()

        self._draw_board()
        self._update_board()

        current_player = red
        self.human_move = None

        if not self.exit_flag:
            self.window.update()
            self.window.update_idletasks()
            self.canvas.update()
            self.canvas.update_idletasks()

        while self.game.get_winner() is None:

            if current_player.is_human:
                move = self._check_input()
            else:
                move = current_player.make_move(self.game.get_game_board())

            if move is None:
                break

            while move not in self.game.get_valid_moves():
                if self.exit_flag:
                    break
                if current_player.is_human:
                    move = self._check_input()
                else:
                    move = current_player.make_move(self.game.get_game_board())

            if not self.exit_flag:
                self.game.make_move(move)

            if current_player is red:
                current_player = yellow
            else:
                current_player = red

            if not self.exit_flag:
                self._update_board()

            if self.exit_flag:
                break

            self.window.update()
            self.canvas.update()

            if no_human:
                time.sleep(.1)

        if not self.exit_flag:
            self._update_board()

        if self.game.get_winner() == 1:
            self.canvas.create_text(100, 20, font='Times 20 italic bold',
                                            text="Red Wins")
            self.canvas.update()
        elif self.game.get_winner() == -1:
            self.canvas.create_text(100, 20, font='Times 20 italic bold',
                                            text="Yellow Wins")
            self.canvas.update()

        if no_human:
            time.sleep(.8)
            self.window.destroy()
        else:
            self.window.mainloop()

    def get_move_sequence(self) -> list[int]:
        return self.game.get_move_sequence()

    def _check_input(self) -> Optional[int]:

        while self.human_move is None:
            if self.exit_flag:
                return None
            else:
                self.window.update()
        move_copy = self.human_move
        self.human_move = None
        return move_copy

    def _draw_board(self):

        col1 = self.canvas.create_rectangle(0, 100, 100, 700, fill='#9e9e9e')
        self.canvas.tag_bind(col1, '<Button-1>', self.onCol1Click)
        col2 = self.canvas.create_rectangle(100, 100, 200, 700, fill='#666666')
        self.canvas.tag_bind(col2, '<Button-1>', self.onCol2Click)
        col3 = self.canvas.create_rectangle(200, 100, 300, 700, fill='#9e9e9e')
        self.canvas.tag_bind(col3, '<Button-1>', self.onCol3Click)
        col4 = self.canvas.create_rectangle(300, 100, 400, 700, fill='#666666')
        self.canvas.tag_bind(col4, '<Button-1>', self.onCol4Click)
        col5 = self.canvas.create_rectangle(400, 100, 500, 700, fill='#9e9e9e')
        self.canvas.tag_bind(col5, '<Button-1>', self.onCol5Click)
        col6 = self.canvas.create_rectangle(500, 100, 600, 700, fill='#666666')
        self.canvas.tag_bind(col6, '<Button-1>', self.onCol6Click)
        col7 = self.canvas.create_rectangle(600, 100, 700, 700, fill='#9e9e9e')
        self.canvas.tag_bind(col7, '<Button-1>', self.onCol7Click)

    def _update_board(self):

        for i in range(len(self.board.board_array)):
            for j in range(len(self.board.board_array[i])):
                if self.board.board_array[i][j] == 1:
                    self.canvas.create_oval(j * 100, 600 - i * 100, 100 + j * 100,
                                            100 + (600 - i * 100), fil='red')
                elif self.board.board_array[i][j] == -1:
                    self.canvas.create_oval(j * 100, 600 - i * 100, 100 + j * 100,
                                            100 + (600 - i * 100), fil='yellow')

    def quit(self):
        self.exit_flag = True
        self.window.destroy()

    def replay(self):
        self.exit_flag = True
        self.is_replay = True
        self.window.destroy()

    def onCol1Click(self, event):
        self.human_move = 0

    def onCol2Click(self, event):
        self.human_move = 1

    def onCol3Click(self, event):
        self.human_move = 2

    def onCol4Click(self, event):
        self.human_move = 3

    def onCol5Click(self, event):
        self.human_move = 4

    def onCol6Click(self, event):
        self.human_move = 5

    def onCol7Click(self, event):
        self.human_move = 6


def add_game(game_tree: nx.DiGraph, root, game_sequence: list[int], variant) -> None:
    for i in range(len(game_sequence)):
        if (game_sequence[i], i, variant - 1) not in game_tree:
            if i == 0:
                game_tree.add_node((game_sequence[i], i, variant))
                game_tree.add_edge('START', (game_sequence[i], i, variant))
                for j in range(i + 1, len(game_sequence)):
                    game_tree.add_node((game_sequence[j], j, variant))
                    game_tree.add_edge((game_sequence[j - 1], j - 1, variant), (game_sequence[j], j, variant))
                return
            else:
                game_tree.add_node((game_sequence[i], i, variant))
                game_tree.add_edge((game_sequence[i - 1], i - 1, variant - 1),
                                   (game_sequence[i], i, variant))
                for j in range(i + 1, len(game_sequence)):
                    game_tree.add_node((game_sequence[j], j, variant))
                    game_tree.add_edge((game_sequence[j - 1], j - 1, variant), (game_sequence[j], j, variant))
                return




        # if i == 0:
        #     if (game_sequence[i], i) not in game_tree:
        #         game_tree.add_node((game_sequence[i], i))
        #         game_tree.add_edge('START', (game_sequence[i], i))
        # elif i < len(game_sequence) - 1:
        #     if (game_sequence[i], i) not in game_tree:
        #         game_tree.add_node((game_sequence[i], i))
        #         game_tree.add_edge((game_sequence[i-1], i-1), (game_sequence[i], i))
        # else:
        #     game_tree.add_node(game_sequence[i])
        #     game_tree.add_edge((game_sequence[i - 1], i - 1), game_sequence[i])



def run_game(red: Player, yellow: Player):
    """Runs a game of Connect 4 using a GUI"""
    window = tkinter.Tk()
    # game = Game(window, red, yellow, TEST)
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

# def run_games(red: Player, yellow: Player, n:int,
#               visualization: bool = False, show_stats: bool = False) -> nx.DiGraph:
#     """Runs n number of games between red and yellow and returns the game tree"""
#     if red is not HumanPlayer and yellow is not HumanPlayer:
#         no_human = True
#     else:
#         no_human = False
#
#     if visualization:
#         game_tree = nx.DiGraph()
#         game_tree.add_node('START')
#         for i in range(n):
#             window = tkinter.Tk()
#             game = Game(window, red, yellow, no_human=no_human)
#             game_moves = game.get_move_sequence()
#             add_game(game_tree, 'START', game_moves, i)
#         plt.title('draw_networkx')
#         pos = hierarchy_pos(game_tree, 'START')
#         nx.draw(game_tree, pos=pos, with_labels=True, arrows=True)
#         plt.show()
#         print(nx.is_tree(game_tree))


TEST = [[0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, -1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, -1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, -1, 0, 0, 0]]
