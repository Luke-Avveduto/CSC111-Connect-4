"""CSC111 Final Project: Exploring Using Graph Based Data Structures to Implement a Connect 4 AI

Module Description
==================

This module contains functions that pertain to the creation and loading of a 'opening book' for
the ComplexAIPlayer to use. An 'opening book' is a dictionary that maps board positions to
evaluations. These evaluations are either 1 for a win for the AI, 0 for a draw, and -1 for a loss
for the AI. This opening book is constructed using data originally created by John Tromp, whose
website about connect 4 can be found here: https://tromp.github.io/c4/c4.html

The boards are converted into hashes using the Zobrist hashing algorithm on which a detailed
explanation can be found here: https://en.wikipedia.org/wiki/Zobrist_hashing

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 Brian Cho and Luke Avveduto
"""
import numpy as np
import csv


def create_opening_book(file: str, output: str) -> None:
    """Generates an opening book in the form of csv where the first value on a line contains a
    hash of a board given by Zobrist hashing using the values found in 'Zobrist_red_key.csv' and
    'Zobrist_yellow_key.csv' and second and final value is a score for the board of the
    corresponding hash. The score takes the form of 1 if the player 1 (red) wins, 0 for a draw, and
    -1 if player 2 (yellow) wins.

    Preconditions:
        - 'file' is the path to a file in the form described by "connect-4.names"
    """
    board_list = []
    with open(file) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            outcome = row.pop()
            if outcome == 'win':
                outcome = 1
            elif outcome == 'draw':
                outcome = 0
            else:
                outcome = -1

            convert = {'x': 1, 'o': -1, 'b': 0}
            row = [convert[r] for r in row]
            row_board = np.array(row).reshape((7, 6)).transpose()

            board_list.append((row_board, outcome))
            board_list.append((np.flip(row_board, 1), outcome))

    red_hash_keys = []
    with open('data/Zobrist_Hash_Keys/Zobrist_red_key.csv') as file:
        reader = csv.reader(file)
        for row in reader:
            red_hash_keys.append([int(r) for r in row])

    yellow_hash_keys = []
    with open('data/Zobrist_Hash_Keys/Zobrist_yellow_key.csv') as file:
        reader = csv.reader(file)
        for row in reader:
            yellow_hash_keys.append([int(r) for r in row])

    with open(output, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        for board in board_list:
            writer.writerow([_get_board_hash(board[0], red_hash_keys, yellow_hash_keys), board[1]])

        output_file.close()


def _get_board_hash(board: np.array, red_hash_keys: list[list[int]],
                   yellow_hash_keys: list[list[int]]) -> int:
    """Returns the hash value of the board according to Zobrist hashing algorithm with the keys for
    the red pieces being in 'red_hash_keys' and the yellow ones being in 'yellow_hash_keys'.
    Preconditions:
        - 'board' must be a 2d numpy array that represents a connect 4 board
        - 'red_hash_keys' must be a a list of list of ints that contain the keys for the red pieces
        - 'yellow_hash_keys' must be a a list of list of ints that contain the
           keys for the yellow pieces
    """
    hash_value = 0
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if board[i][j] == 1:
                hash_value = hash_value ^ red_hash_keys[i][j]
            elif board[i][j] == -1:
                hash_value = hash_value ^ yellow_hash_keys[i][j]
    return hash_value


def load_opening_book(file: str) -> {int: (int, str)}:
    """Returns a dictionary (transposition table) that maps board hashes to their evaluation.
    Preconditions:
        - 'file' must be a path to a file created by 'create_opening_book'
    """
    opening_book = {}
    with open(file) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            opening_book[int(row[0])] = (int(row[1]), 'exact')
    return opening_book
