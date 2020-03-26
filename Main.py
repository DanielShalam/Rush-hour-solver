import numpy as np
import GameNodes
from Const import puzzles


#   initialize board from given puzzle (string)
def initFromString(puzzle):
    board = [char for char in puzzle]
    board = np.reshape(board, (6, 6))
    return board


if __name__ == "__main__":
    #   for p in puzzles:
    initial_board = initFromString("A..OOOA..B.PXX.BCPQQQ.CP..D.EEFFDGG.")
    root = GameNodes.Node(initial_board)
    root.generateSuccessors()
