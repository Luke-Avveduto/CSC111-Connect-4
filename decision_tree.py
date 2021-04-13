from __future__ import annotations
from typing import Any, Optional
import csv


class DecisionTree:
    """An implementation of the Tree ADT designed to work as a decision tree for the
    AI of the connect 4 game.

    Representation Invariants:
    - self._move is not None or self._subtrees == []
    - all(not subtree.is_empty() for subtree in self._subtrees)
    - if self._move is None or self._move in {0, 1, 2, 3, 4, 5, 6, -1}
    - -1 <= self._eval <= 1
    """
    # Private Instance Attributes:
    #   - _move: The column number, starting at 0 and going to 6 inclusively, of the piece placed
    #           on this move in the game. Or, -1, to signal the start of the game
    #   - _subtrees:
    #       The list of subtrees of this tree. This attribute is empty when
    #       self._root is None (representing an empty tree). However, this attribute
    #       may be empty when self._root is not None, which represents a tree consisting
    #       of just one item.
    #   - _length: The length of this tree
    #   - _eval: The evaluation of the board if all of its ancestors moves have been mad

    _move: Optional[int]
    _subtrees: list[DecisionTree]
    _length: int = 0
    _eval: float
    _turn: str

    def __init__(self, move: Optional[int], subtrees: list[DecisionTree], turn) -> None:
        """Initialize a new DecisionTree with the given move value and subtrees.

        If move is None, the tree is empty.

        Preconditions:
            - move is not None or subtrees == []
        """
        self._move = move
        self._subtrees = subtrees
        self._turn = turn
        self._length = len(subtrees) + 1

    def get_subtrees(self) -> list[DecisionTree]:
        """A simple getter function for the self._subtrees value
        """
        return self._subtrees

    def get_eval(self) -> float:
        """A simple getter function for the self._eval value
        """
        return self._eval

    def update_eval(self) -> None:
        # for subtree in self._subtrees:
        #     subtree.update_eval()  # Should create a cascading effect so all the numbers are fresh
        subtree_eval_set = {subtree.get_eval() for subtree in self._subtrees}
        if self._turn == 'red':
            self._eval = max(subtree_eval_set)
        else:
            self._eval = sum(subtree_eval_set)/len(subtree_eval_set)

    def is_empty(self) -> bool:
        """Return whether this tree is empty.
        """
        return self._move is None

    def __len__(self) -> int:
        """Return the number of items contained in this tree.
        """
        return self._length

    def __str__(self) -> str:
        """Return a string representation of this tree.
        """

        # Version 2: with indentation (and a recursive helper method!)
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            s = depth * '  ' + f'{self._move}' + '---' + f'{self._eval}\n'  # Note how we're using depth to indent
            for subtree in self._subtrees:
                s += subtree._str_indented(depth + 1)  # Note the argument depth + 1
            return s

    def get_this_move(self, move: int) -> Optional[DecisionTree]:
        """Checks to see if there is a child of this tree that has move value equal to 'move'
        if there is, then it will be returned, if not, then None will be returned.
        """
        for subtree in self._subtrees:
            if subtree._move == move:
                return subtree

    def output_list(self) -> list[list[int]]:
        """Returns a 2-d list of ints that can be written to a csv so that this tree can be
        reconstructed from that file. It uses recursion to do this.
        """
        if self._subtrees == []:
            return [[self._move, self._eval]]

        output = []
        for subtree in self._subtrees:
            sub_output = subtree.output_list()
            for sub_list in sub_output:
                output.append([self._move] + sub_list)
        return output

    def add_game(self, game_sequence: list[int]) -> None:
        """Recursive function that extends the tree to include a new branch that represents a game
        played with all the moves in the 'game_sequence'. If the first move in the sequence already
        has a subtree, then it will be recursively called on that subtree with the first element
        of the list sliced off. If the first move of the sequence doesn't already have a subtree,
        then a new one is created and the same as before is done but then this new subtree is added
        onto this tree.
        """

        if len(game_sequence) == 1:
            # The last element of this list says whether the game was won or not
            self._eval = game_sequence[0]
            return None

        possible_subtree = self.get_this_move(game_sequence[0])
        if possible_subtree is not None:
            return possible_subtree.add_game(game_sequence[1:])
        else:
            if self._turn == 'red':
                new_subtree = DecisionTree(move=game_sequence[0], turn='yellow', subtrees=[])
            else:
                new_subtree = DecisionTree(move=game_sequence[0], turn='red', subtrees=[])
            new_subtree.add_game(game_sequence[1:])
            self._subtrees.append(new_subtree)
            self.update_eval()  # This is needed as a new subtree has been added

    def get_best_move(self) -> int:
        """Returns the the move of the subtree with the highest eval value.
        Preconditions:
            - self._subtrees != []
        """
        best_subtree = self._subtrees[0]
        for subtree in self._subtrees:
            if subtree._eval > best_subtree._eval:
                best_subtree = subtree
        return best_subtree._move


def build_from_file(file_name: str) -> DecisionTree:
    """Creates a decision tree from a csv file in the correct format.

    Preconditions:
        - file_name is the address to a csv file in the proper format
    """
    d_tree = DecisionTree(move=-1, turn='yellow', subtrees=[])
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            move_list = [int(move) for move in row]
            d_tree.add_game(move_list)
    return d_tree


def write_to_file(d_tree: DecisionTree, output_file) -> None:
    """Writes the decision tree "d_tree" into a csv file in such a way that it can be reconstructed
    by the build_from_file function.
    """
    data = []
    for subtree in d_tree.get_subtrees():
        data.extend(subtree.output_list())
    with open(output_file, mode='w', newline="") as output_csv:
        writer = csv.writer(output_csv)

        for game in data:
            writer.writerow(game)
        output_csv.close()
