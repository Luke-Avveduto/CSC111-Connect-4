from __future__ import annotations
from typing import Any, Optional


class DecisionTree:
    """An implementation of the Tree ADT designed to work as a decision tree for the
    AI of the connect 4 game.

    Representation Invariants:
    - self._move is not None or self._subtrees == []
    - all(not subtree.is_empty() for subtree in self._subtrees)
    - if self._move is None or self._move in {0, 1, 2, 3, 4, 5, 6, -1}
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

    _move: Optional[int]
    _subtrees: list[DecisionTree]
    _length: int = 0

    def __init__(self, move: Optional[int], subtrees: list[DecisionTree]) -> None:
        """Initialize a new DecisionTree with the given move value and subtrees.

        If move is None, the tree is empty.

        Preconditions:
            - move is not None or subtrees == []
        """
        self._move = move
        self._subtrees = subtrees
        self._length = len(subtrees) + 1

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
            s = depth * '  ' + f'{self._move}\n'  # Note how we're using depth to indent
            for subtree in self._subtrees:
                s += subtree._str_indented(depth + 1)  # Note the argument depth + 1
            return s
