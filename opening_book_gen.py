"""CSC111 Final Project: Exploring Using Graph Based Data Structures to Implement a Connect 4 AI

Module Description
==================

This module contains functions that pertain to the creation and loading of a 'opening book' for
the ComplexAIPlayer to use. An 'opening book' is a dictionary that maps board positions to
evaluations. These opening books can be generated from any list of connect 4 positions, however, the
functions in this module deal with saving the transposition table built up by the AI during play.

The boards are converted into hashes using the Zobrist hashing algorithm on which a detailed
explanation can be found here: https://en.wikipedia.org/wiki/Zobrist_hashing

The keys used in for the Zobrist hashing can be found in:
data/Zobrist_Hash_keys/Zobrist_red_keys.csv
data/Zobrist_Hash_keys/Zobrist_yellow_keys.csv

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 Brian Cho and Luke Avveduto
"""
import csv
import math


def save_opening_book(output: str, table: dict[int: (int, 'str', int)],
                      original_depth: int) -> None:
    """Saves a transposition table into a csv file to be read from later. Different starting
    depths are incompatible with each other and so separate files are created. These files are
    indexed by adding '_' + str(original_depth) + '.csv' to the end of there name.

    Preconditions:
        - original_depth >= 0
        - table must be a transposition table produced by AIPlayerComplex
    """
    with open(output + '_' + str(original_depth) + '.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        for board in table:
            row = [board, table[board][0], table[board][1], table[board][2]]
            writer.writerow(row)
        csv_file.close()


def load_opening_book(file: str) -> {int: (int, str)}:
    """Returns a dictionary (transposition table) that maps board hashes to their evaluation.
    Preconditions:
        - 'file' must be a path to a file created by 'save_opening_book'
    """
    opening_book = {}
    with open(file) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if row[1] == 'inf':
                value = math.inf
            elif row[1] == '-inf':
                value = -math.inf
            else:
                value = int(row[1])
            opening_book[int(row[0])] = (value, row[2], int(row[3]))
    return opening_book


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['csv', 'math'],  # the names (strs) of imported modules
        'allowed-io': ['load_opening_book', 'save_opening_book'],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })
