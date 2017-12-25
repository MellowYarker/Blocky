"""Assignment 2 - Blocky

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Goal class hierarchy.
"""

from typing import List, Tuple
from block import Block


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """
    colour: Tuple[int, int, int]

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize this goal to have the given target colour.
        """
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal.
        """
        raise NotImplementedError


class BlobGoal(Goal):
    """A goal to create the largest connected blob of this goal's target
    colour, anywhere within the Block.
    """

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize a BlobGoal to have the given target colour.
        """
        Goal.__init__(self, target_colour)

    def score(self, board: Block) -> int:
        """Return the current score for the BlobGoal on the given board.

         The score is always greater than or equal to 0.
        """
        score = []
        blocks = board.flatten()
        for col in range(len(blocks)):
            for element in range(len(blocks[col])):
                if blocks[col][element] == self.colour:
                    score.append(self._undiscovered_blob_size((col, element),
                                                              blocks, []))
        return max(score)

    def description(self) -> str:
        """Return a descripton of this PerimeterGoal.
        """

        return "Blob Goal! Connect as many blocks of the background colour " \
               "as you can."

    def _undiscovered_blob_size(self, pos: Tuple[int, int],
                                board: List[List[Tuple[int, int, int]]],
                                visited: List[List[int]]) -> int:
        """Return the size of the largest connected blob that (a) is of this
        Goal's target colour, (b) includes the cell at <pos>, and (c) involves
        only cells that have never been visited.

        If <pos> is out of bounds for <board>, return 0.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure that, in each cell, contains:
           -1  if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.

        >>> z = BlobGoal((255, 211, 92))
        >>> lst = [[(138, 151, 71), (255, 211, 92), (138, 151, 71), (138, 151, 71), (255, 211, 92), (255, 211, 92), (138, 151, 71), (138, 151, 71)], [(138, 151, 71), (199, 44, 58), (138, 151, 71), (138, 151, 71), (255, 211, 92), (1, 128, 181), (138, 151, 71), (138, 151, 71)], [(138, 151, 71), (138, 151, 71), (255, 211, 92), (255, 211, 92), (138, 151, 71), (138, 151, 71), (199, 44, 58), (199, 44, 58)], [(138, 151, 71), (138, 151, 71), (199, 44, 58), (1, 128, 181), (199, 44, 58), (199, 44, 58), (199, 44, 58), (199, 44, 58)], [(199, 44, 58), (199, 44, 58), (138, 151, 71), (1, 128, 181), (255, 211, 92), (255, 211, 92), (255, 211, 92), (255, 211, 92)], [(199, 44, 58), (199, 44, 58), (255, 211, 92), (199, 44, 58), (255, 211, 92), (255, 211, 92), (255, 211, 92), (255, 211, 92)], [(255, 211, 92), (255, 211, 92), (138, 151, 71), (138, 151, 71), (255, 211, 92), (255, 211, 92), (255, 211, 92), (255, 211, 92)], [(199, 44, 58), (138, 151, 71), (138, 151, 71), (138, 151, 71), (255, 211, 92), (255, 211, 92), (255, 211, 92), (255, 211, 92)]]
        >>> z._undiscovered_blob_size((4, 5), lst, [])
        16

        """

        # if pos is out of bounds for board
        if pos[0] > len(board) - 1 or pos[1] > len(board[0]) - 1:
            return 0

        # initialize the "visited" list
        if len(visited) == 0:
            for i in range(len(board)):
                visited.append([])
                for _ in range(len(board[i])):
                    visited[i].append(-1)
        # if not visited
        score = 0
        lst = []
        if visited[pos[0]][pos[1]] == -1:
            # if it is the same colour, increase score by 1 and add it
            # to the list. Update visited.
            if board[pos[0]][pos[1]] == self.colour:
                score += 1
                visited[pos[0]][pos[1]] = 1
                # now check the neighbors
                for neighbor in neighbors(pos, board):
                    # if there is a neighbor that is not visited, recurse
                    if visited[neighbor[0]][neighbor[1]] == -1:
                        lst.append(self._undiscovered_blob_size(neighbor,
                                                                board,
                                                                visited))

                # if it is not the same colour, update visited.
            else:
                visited[pos[0]][pos[1]] = 0

        return score + sum(lst)


# helper for _undiscovered_blob_size
def neighbors(position: Tuple[int, int],
              board: List[List[Tuple[int, int, int]]]) -> List[Tuple[int, int]]:
    """Returns a list of position of neighbors of blob self.

    Precondition: board is flattened"""
    max_row = len(board) - 1
    max_column = len(board[0]) - 1
    list_ = []

    # left
    if position[0] >= 1:
        list_.append((position[0]-1, position[1]))

    # right
    if position[0] <= max_row - 1:
        list_.append((position[0] + 1, position[1]))

    # top
    if position[1] >= 1:
        list_.append((position[0], position[1] - 1))

    # bottom
    if position[1] <= max_column - 1:
        list_.append((position[0], position[1] + 1))
    return list_


class PerimeterGoal(Goal):
    """A goal to create the largest connection of this goal's target
    colour along the perimeter of the Block.
    """
    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize a PerimeterGoal to have the given target colour.
        """
        Goal.__init__(self, target_colour)

    def score(self, board: Block) -> int:
        """Return the current score for the PerimeterGoal on the given board.

         The score is always greater than or equal to 0.

         [[(1, 128, 181), (1, 128, 181), (255, 211, 92), (1, 128, 181)],
         [(1, 128, 181), (1, 128, 181), (199, 44, 58), (199, 44, 58)],
         [(255, 211, 92), (199, 44, 58), (255, 211, 92), (138, 151, 71)],
         [(1, 128, 181), (1, 128, 181), (199, 44, 58), (199, 44, 58)]]

         """
        score = 0
        lst = board.flatten()
        # Relevant blocks are:
        #   lst[0][:] (first column)
        #   lst[len(lst) - 1][0] (last column)
        #   and the first and last value of every column
        perimeter = []
        # add the first column
        for i in lst[0]:
            perimeter.append(i)

        # add the bottom of every column but the first and last
        for i in range(len(lst)):
            perimeter.append(lst[i][len(lst[0]) - 1])
        # add the last column
        for i in lst[len(lst) - 1]:
            perimeter.append(i)

        # add the top of every column
        for i in range(len(lst)):
            perimeter.append(lst[i][0])

        # get the score
        for i in perimeter:
            if i == self.colour:
                score += 1
        return score

    def description(self) -> str:
        """Return a descripton of this BlobGoal.
        """

        return "Perimeter Goal! Move blocks of the background colour to the " \
               "perimeter."


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing',
            'block', 'goal', 'player', 'renderer'
        ],
        'max-attributes': 15
    })
