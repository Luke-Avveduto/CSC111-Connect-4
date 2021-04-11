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
import typing

def run_game():
    """Runs a game of Connect 4 using a GUI"""
    game = Connect4Game()
    board = game.get_game_board()

    window, canv = init_display(board)
    draw_slots(board, canv)



def init_display(board: list[list[int]]):
    """Initalize the display"""
    window = tkinter.Tk()
    window.geometry('700x700')
    canv = tkinter.Canvas(window, width=700, height=700)
    canv.pack()
    for i in range(len(board[0])):
        if i % 2 == 0:
            canv.create_rectangle(0 + i * 100, 100, 100 + i * 100, 700, fill='#9e9e9e')
        else:
            canv.create_rectangle(0 + i * 100, 100, 100 + i * 100, 700, fill='#666666')

    window.mainloop()

    return window, canv


def draw_slots(board: list[list[int]], canv: tkinter.Canvas):
    """Draw the current game board"""
    canv.create_oval(0, 600, 100, 700)
    canv.update()


