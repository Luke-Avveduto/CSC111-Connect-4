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
from typing import Optional

class Game:

    window: tkinter.Tk
    canvas: tkinter.Canvas
    board: list[list[int]]
    human_move: Optional[int]
    exit_flag: bool

    def __init__(self, window, red: Player, yellow: Player):

        self.window = window
        self.window.geometry('700x700')
        self.canvas = tkinter.Canvas(self.window, width=700, height=700)
        self.canvas.pack()
        self.exit_flag = False
        button = tkinter.Button(self.canvas, text='Quit', command=self.quit)
        button.place(x=600, y=40)

        game = Connect4Game()
        self.board = game.get_game_board()

        self._draw_board()

        current_player = red
        self.human_move = None

        self.window.update()
        self.window.update_idletasks()
        self.canvas.update()
        self.canvas.update_idletasks()

        while game.get_winner() is None and not self.exit_flag:

            if current_player.is_human:
                move = self._check_input()
            else:
                move = current_player.make_move(game)

            game.make_move(move)

            if current_player is red:
                current_player = yellow
            else:
                current_player = red

            self._update_board()

            self.window.update()
            self.window.update_idletasks()
            self.canvas.update()
            self.canvas.update_idletasks()

        self._update_board()
        if game.get_winner() == 1:
            self.canvas.create_text(100, 20, font='Times 20 italic bold',
                                    text="Red Wins")
        else:
            self.canvas.create_text(100, 20, font='Times 20 italic bold',
                                    text="Yellow Wins")
        self.canvas.update()

    def _check_input(self) -> int:

        while self.human_move is None:
            self.window.update()
            self.window.update_idletasks()
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

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 1:
                    self.canvas.create_oval(j * 100, 600 - i * 100, 100 + j * 100,
                                            100 + (600 - i * 100), fil='red')
                elif self.board[i][j] == 2:
                    self.canvas.create_oval(j * 100, 600 - i * 100, 100 + j * 100,
                                            100 + (600 - i * 100), fil='yellow')

    def quit(self):
        self.exit_flag = True
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


def run_game(red: Player, yellow: Player):
    """Runs a game of Connect 4 using a GUI"""
    window = tkinter.Tk()
    game = Game(window, red, yellow)



