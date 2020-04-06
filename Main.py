import numpy as np
import GameNodes
from Board import Board
from Algorithm import *
from Const import puzzles
from multiprocessing import Process, Queue


#   initialize board as numpy array from given puzzle (string)
def initFromString(puzzle):
    board = np.chararray((1, 36))
    board[:] = [char for char in puzzle]
    board = np.reshape(board, (6, 6))
    return board


if __name__ == "__main__":
    time_limit = 1000*60
    for p in puzzles:
        return_queue = Queue()
        initial_board = initFromString(p)
        print(initial_board)
        initial_board = Board(initial_board)
        root = GameNodes.Node(initial_board)
        p = Process(target=aStarSearch, name="aStarSearch", args=(root, ))
        p.start()
        p.join(time_limit)

        if p.is_alive():

            # Terminate A*
            p.terminate()
            p.join()



