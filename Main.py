import numpy as np
import GameNodes
from Board import Board
from Hueristics import advancedBlocking
import Algorithm
from Const import puzzles


#   initialize board from given puzzle (string)
def initFromString(puzzle):
    board = [char for char in puzzle]
    board = np.reshape(board, (6, 6))
    return board


if __name__ == "__main__":
    #   for p in puzzles:
    initial_board = initFromString("A..OOOA..B.PXX.BCPQQQ.CP..D.EEFFDGG.")
    print(initial_board)
    initial_board = Board(initial_board)
    initial_board.findCars()
    root = GameNodes.Node(initial_board)
    result = Algorithm.aStarSearch(root)
    print(result.board.board_state)
