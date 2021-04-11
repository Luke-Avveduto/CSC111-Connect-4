"""CSC111 Lecture 8 examples"""
from __future__ import annotations
from typing import Any, Optional


class Tree:
    """A recursive tree data structure.

    Representation Invariants:
        - self._root is not None or self._subtrees == []
        - all(not subtree.is_empty() for subtree in self._subtrees)
            # "Every subtree in self._subtrees is non-empty"
    """
    # Private Instance Attributes:
    #   - _root:
    #       The item stored at this tree's root, or None if the tree is empty.
    #   - _subtrees:
    #       The list of subtrees of this tree. This attribute is empty when
    #       self._root is None (representing an empty tree). However, this attribute
    #       may be empty when self._root is not None, which represents a tree consisting
    #       of just one item.
    _root: Optional[Any]
    _subtrees: list[Tree]

    def __init__(self, root: Optional[Any], subtrees: list[Tree]) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If root is None, the tree is empty.

        Preconditions:
            - root is not none or subtrees == []
        """
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """Return whether this tree is empty.
        """
        return self._root is None

    def __len__(self) -> int:
        """Return the number of items contained in this tree.

        >>> t1 = Tree(None, [])
        >>> len(t1)
        0
        >>> t2 = Tree(3, [Tree(4, []), Tree(1, [])])
        >>> len(t2)
        3
        """
        if self.is_empty():
            return 0
        else:
            # return 1 + sum(subtree.__len__() for subtree in self._subtrees)
            len_so_far = 0
            for subtree1 in self._subtrees:
                for subtree2 in self._subtrees:
                    len_so_far += subtree1.__len__() * subtree2.__len__()
            return len_so_far

    def __str__(self) -> str:
        """Return a string representation of this tree.
        """
        # Version 1: no indentation
        # if self.is_empty():
        #     return ''
        # else:
        #     s = f'{self._root}\n'
        #     for subtree in self._subtrees:
        #         s += subtree.__str__()
        #     return s

        # Version 2: with indentation (and a recursive helper method!)
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            s = depth * '  ' + f'{self._root}\n'  # Note how we're using depth to indent
            for subtree in self._subtrees:
                s += subtree._str_indented(depth + 1)  # Note the argument depth + 1
            return s

    def __contains__(self, item: Any) -> bool:
        """Return whether the given item is in this tree."""
        if self.is_empty():
            return False
        elif self._root == item:
            return True
        else:
            for subtree in self._subtrees:
                if subtree.__contains__(item):
                    return True

            return False

    def remove(self, item: Any) -> bool:
        """Delete *one* occurrence of the given item from this tree.

        Do nothing if the item is not in this tree.
        Return whether the given item was deleted.
        """
        if self.is_empty():
            return False
        elif self._root == item:
            # Need to remove the root of this tree
            # self._root = None  <-- doesn't work, self._subtrees might be non-empty
            self._delete_root()
            return True
        else:
            for subtree in self._subtrees:
                if subtree.remove(item):
                    # Idea 1: call a helper to remove all empty subtrees
                    # self._remove_empty_subtrees()

                    # Idea 2: check whether (the current) subtree is empty
                    if subtree.is_empty():
                        # Warning: in general, shouldn't mutate self._subtrees as we loop over
                        # it. But okay here because we're returning right after this line.
                        list.remove(self._subtrees, subtree)
                    return True

            return False

    def _delete_root(self) -> None:
        """Remove the root of this tree.

        Preconditions:
            - not self.is_empty()
        """
        if self._subtrees == []:
            self._root = None     # If self has size one, we turn it into an empty tree
        else:
            # Strategy 1
            # last_subtree = self._subtrees.pop()
            #
            # self._root = last_subtree._root
            # self._subtrees.extend(last_subtree._subtrees)
            # self._subtrees = self._subtrees + last_subtree._subtrees  (alternate version)

            # Strategy 2
            self._root = self._extract_leaf()

    def _extract_leaf(self) -> Any:
        """Remove and return the leftmost leaf in this tree.

        Preconditions:
            - not self.is_empty()
        """
        if self._subtrees == []:   # Similar to _delete_root, but also returns the root value
            root = self._root
            self._root = None
            return root
        else:
            # Homework: need to update this method as well to preserve the "no empty
            # subtrees" representation invariant!
            return self._subtrees[0]._extract_leaf()  # Recurse on leftmost subtree