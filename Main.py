import GameNodes
from Board import Board
from Algorithm import *
from Const import puzzles
import pandas as pd
import ProblemGenerator
from matplotlib import pyplot as plt

TIME_LIMIT = 1000
PUZZLES_NUM = 40


#   initialize board as numpy array from given puzzle (string)
#   The board will be kept in bytes for optimization of certain operations
def initFromString(_puzzle):
    board = np.chararray((1, 36))
    board[:] = [char for char in _puzzle]
    board = np.reshape(board, (6, 6))
    return board


def insertStatistics(_statistics_df, statistics_list_, heuristic_name, _puzzle, _puzzle_counter):
    if statistics_list_[0] <= TIME_LIMIT:
        solved = 'Y'
    else:
        solved = 'N'
    new_row = [_puzzle, heuristic_name, statistics_list_[1],
               statistics_list_[3] / statistics_list_[1], solved, statistics_list_[0],
               statistics_list_[1] ** (1 / statistics_list_[3]), statistics_list_[4] / statistics_list_[1],
               statistics_list_[7], statistics_list_[6] / statistics_list_[1], statistics_list_[5]]

    _statistics_df = _statistics_df.append(pd.Series(new_row, index=_statistics_df.columns, name=_puzzle_counter))

    statistics_list_.clear()

    return _statistics_df


if __name__ == '__main__':
    # initialize some vars
    pd.set_option('display.max_columns', None)
    columns_for_df = ['Problem ', 'Heuristic name ', 'N ', 'd/N ', 'Success (Y/N) ', 'Time (ms) ', 'EBF ',
                      'avg H value ', 'Min ', 'Avg ', 'Max ']
    puzzle_counter = 0
    statistics_df = pd.DataFrame(columns=columns_for_df)
    uniformed_statistics_df = pd.DataFrame(columns=columns_for_df)
    solved_or_failed = [0, 0, 0]
    statistics_list = list()

    heuristics = [1, 2, 3]

    new_board = ProblemGenerator.makePuzzle()
    print(new_board)

    for heuristic in heuristics:
        for puzzle in puzzles:
            initial_board = initFromString(puzzle)
            print(initial_board.astype('U13'), '\n')
            initial_board = Board(initial_board)
            root = GameNodes.Node(initial_board)
            statistics_list = aStarSearch(root, heuristic)
            if statistics_list[0] <= TIME_LIMIT and statistics_list[2] is not 'Failed ':
                winner_state = statistics_list[2].astype('U13')
                winner_state = np.array2string(winner_state.flatten(), precision=2, separator=',', suppress_small=True)
                print('The Solution is: \n', winner_state, '\n')

                solved_or_failed[heuristic - 1] += 1
            else:
                print('The Solution is: \n', statistics_list[2], '\n')

            if heuristic is 1:
                statistics_df = insertStatistics(statistics_df, statistics_list, 'advancedBlocking', puzzle,
                                                 puzzle_counter)
            elif heuristic is 2:
                statistics_df = insertStatistics(statistics_df, statistics_list, 'advancedDoubleBlocking', puzzle,
                                                 puzzle_counter)
            elif heuristic is 3:
                statistics_df = insertStatistics(statistics_df, statistics_list, 'verticalFromRight', puzzle,
                                                 puzzle_counter)
            else:
                uniformed_statistics_df = insertStatistics(uniformed_statistics_df, statistics_list, '-', puzzle,
                                                           puzzle_counter)

            puzzle_counter += 1

    # print final statistics
    print('Global Statistics table: \n')
    print(statistics_df)

    # print average statistics for each heuristic
    init_index = 0
    final_index = PUZZLES_NUM - 1
    heuristics = ['Advanced blocking', 'Advanced double blocking', 'Vertical from right']
    print('Average Statistics for each heuristic: \n')
    for idx, heuristic in enumerate(heuristics):
        print('For', heuristic, 'heuristic:')
        print('Number of solved puzzles:', solved_or_failed[idx - 1])
        print('Average number of expended nodes:', statistics_df['N '].iloc[init_index:final_index].mean())
        print('Average rate of penetrability:', statistics_df['d/N '].iloc[init_index:final_index].mean())
        print('Average EBF value:', statistics_df['EBF '].iloc[init_index:final_index].mean())
        print('Average heuristic value:', statistics_df['avg H value '].iloc[init_index:final_index].mean())
        print('Average max depth:', statistics_df['Max '].iloc[init_index:final_index].mean())
        print('Average min depth:', statistics_df['Min '].iloc[init_index:final_index].mean())
        print('Average of depth Average:', statistics_df['Avg '].iloc[init_index:final_index].mean())
        print('Average solving time:', statistics_df['Time (ms) '].iloc[init_index:final_index].mean(), '\n')

        init_index += PUZZLES_NUM
        final_index += PUZZLES_NUM


def graphMaker(data1, data2):
    pass
