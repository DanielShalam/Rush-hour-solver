import numpy as np
import GameNodes
from Board import Board
import Algorithm
from Const import puzzles


#   initialize board from given puzzle (string)
def initFromString(puzzle):
    board = np.chararray((1, 36))
    board[:] = [char for char in puzzle]
    board = np.reshape(board, (6, 6))
    print(board[1][1] == b'.')
    return board


if __name__ == "__main__":
    #   for p in puzzles:
    initial_board = initFromString("AA...OP..Q.OPXXQ.OP..Q..B...CCB.RRR.")
    print(initial_board)
    initial_board = Board(initial_board)
    root = GameNodes.Node(initial_board)
    result = Algorithm.aStarSearch(root)
    print("Game is done: ")
    print(result.board.board_state)
