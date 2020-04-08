import GameNodes
from Board import Board
from Algorithm import *
from Const import puzzles
from multiprocessing import Process, Queue
import pandas as pd


#   initialize board as numpy array from given puzzle (string)
def initFromString(_puzzle):
    board = np.chararray((1, 36))
    board[:] = [char for char in _puzzle]
    board = np.reshape(board, (6, 6))
    return board


def insertStatistics(_statistics_df, statistics_list_, heuristic_name, _puzzle, _puzzle_counter):
    if statistics_list_[2] is not None:
        solved = 'Y'
    else:
        solved = 'N'
    new_row = [_puzzle, heuristic_name, statistics_list_[0], statistics_list_[1],
               statistics_list_[3] / statistics_list_[1], solved, statistics_list_[1] ** (1/statistics_list_[3]),
               statistics_list_[4] / statistics_list_[1], statistics_list_[6],
               statistics_list_[6] / statistics_list_[1], statistics_list_[5]]

    _statistics_df = _statistics_df.append(pd.Series(new_row, index=_statistics_df.columns, name=_puzzle_counter))

    statistics_list_.clear()

    return _statistics_df


if __name__ == "__main__":
    columns_for_df = ['Problem ', 'Heuristic name ', 'N ', 'd/N ', 'Success (Y/N) ', 'Time (ms) ', 'EBF ', 'avg H '
                                                                                                           'value ',
                      'Min', 'Avg', 'Max']
    solutions_list = list()
    puzzle_counter = 0
    time_limit = 1000 * 60
    statistics_df = pd.DataFrame(columns=columns_for_df)

    statistics_list = list()

    heuristics = [1, 2, 3]

    for heuristic in heuristics:
        for puzzle in puzzles:
            return_queue = Queue()
            initial_board = initFromString(puzzle)
            print(initial_board)
            initial_board = Board(initial_board)
            root = GameNodes.Node(initial_board)
            p = Process(target=aStarSearch, name="aStarSearch", args=(root, heuristic, return_queue,))
            p.start()
            p.join(time_limit)

            if p.is_alive():
                # Terminate A* if it didnt finish solving in time
                p.terminate()
                p.join()

            while not return_queue.empty():
                # saving statistics from each puzzle
                return_value = return_queue.get()
                statistics_list.append(return_value)

            if heuristic is 1:
                statistics_df = insertStatistics(statistics_df, statistics_list, "advancedBlocking", puzzle,
                                                 puzzle_counter)
            elif heuristic is 2:
                statistics_df = insertStatistics(statistics_df, statistics_list, "advancedDoubleBlocking", puzzle,
                                                 puzzle_counter)
            elif heuristic is 3:
                statistics_df = insertStatistics(statistics_df, statistics_list, "verticalFromRight", puzzle,
                                                 puzzle_counter)

            if statistics_list:
                print("The winner state is: \n", statistics_list[2].flatter().decode("utf-8"))

            puzzle_counter += 1
        # print final statistics

    print(statistics_df)
