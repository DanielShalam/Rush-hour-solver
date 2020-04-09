import threading
import GameNodes
from Board import Board
from Algorithm import *
from Const import puzzles
import pandas as pd
import ProblemGenerator

TIME_LIMIT = 0
PUZZLES_NUM = 40
horizontal_list = []
vertical_list = []


#   customize new threading class for our needs
class myThread(threading.Thread):
    def __init__(self, thread_id, name, counter):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.counter = counter

    def run(self):
        global horizontal_list
        global vertical_list

        if self.thread_id == 1:
            horizontal_list = aStarSearch(root, heuristic, True, 1)
        else:
            vertical_list = aStarSearch(root, heuristic, True, 2)

    def returning(self):
        global horizontal_list
        global vertical_list

        if self.thread_id == 1:
            return horizontal_list
        else:
            return vertical_list


#   initialize board as numpy array from given puzzle (string)
#   The board will be kept in bytes for optimization of certain operations
def initFromString(_puzzle):
    board = np.chararray((1, 36))
    board[:] = [char for char in _puzzle]
    board = np.reshape(board, (6, 6))
    return board


#   function to insert statistics from each iteration to our goal data frame
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

    return _statistics_df


if __name__ == '__main__':
    TIME_LIMIT = float(input("Enter time limit for each puzzle (in seconds) : "))

    # initialize some vars
    threadLock = threading.Lock()
    threads = []

    pd.set_option('display.max_columns', None)
    columns_for_df = ['Problem ', 'Heuristic name ', 'N ', 'd/N ', 'Success (Y/N) ', 'Time (ms) ', 'EBF ',
                      'avg H value ', 'Min ', 'Avg ', 'Max ']
    puzzle_counter = 0
    statistics_df = pd.DataFrame(columns=columns_for_df)
    solved_or_failed = [0, 0, 0, 0]
    statistics_list = list()

    heuristics = [1, 2, 3, 4]

    # new_board = ProblemGenerator.makePuzzle()
    # print(new_board)

    for heuristic in heuristics:
        for puzzle in puzzles:
            stop_threads = False
            event = threading.Event()
            # create initial board
            initial_board = initFromString(puzzle)
            print(initial_board.astype('U13'), '\n')
            initial_board = Board(initial_board)

            # creates 2 threads - solving for vertical and horizontal successors of the initial board in each thread

            thread1 = myThread(1, "Thread-horizontal", 1)
            thread2 = myThread(2, "Thread-vertical", 2)
            root = GameNodes.Node(initial_board)

            thread1.start()
            thread2.start()

            # Add threads to thread list
            threads.append(thread1)
            threads.append(thread2)

            while True:
                if not threads[0].is_alive() and threads[1].is_alive():
                    statistics_list = threads[0].returning()
                    if type(statistics_list[2]) != str:
                        break
                elif not threads[1].is_alive() and threads[0].is_alive():
                    statistics_list = threads[1].returning()
                    if type(statistics_list[2]) != str:
                        break
                elif not threads[1].is_alive() and not threads[0].is_alive():
                    statistics_list = threads[1].returning()
                    break

            print("For heuristic", heuristic, puzzle_counter)
            # insert and displaying statistics
            if statistics_list[0] <= TIME_LIMIT and type(statistics_list[2]) is not str:
                winner_state = statistics_list[2].astype('U13')
                winner_state = np.array2string(winner_state.flatten(), precision=2, separator=',', suppress_small=True)
                print('The Solution is: \n', winner_state, '\n')

                solved_or_failed[heuristic - 1] += 1
            else:
                print('The Solution is: \n', statistics_list[2], '\n')

            # insert statistics to the data frame
            if heuristic is 1:
                statistics_df = insertStatistics(statistics_df, statistics_list, 'Advanced Blocking', puzzle,
                                                 puzzle_counter)
            elif heuristic is 2:
                statistics_df = insertStatistics(statistics_df, statistics_list, 'Advanced Double Blocking', puzzle,
                                                 puzzle_counter)
            elif heuristic is 3:
                statistics_df = insertStatistics(statistics_df, statistics_list, 'Vertical From Right', puzzle,
                                                 puzzle_counter)
            else:
                statistics_df = insertStatistics(statistics_df, statistics_list, 'Uniformed search', puzzle,
                                                 puzzle_counter)

            puzzle_counter += 1

    # print final statistics
    print('Global Statistics table: \n')
    print(statistics_df)

    compression_opts = dict(method='zip', archive_name='statistics.csv')
    statistics_df.to_csv('statistics.zip', index=False, compression=compression_opts)

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
