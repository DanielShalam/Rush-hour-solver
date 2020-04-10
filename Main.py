import threading
import GameNodes
from Board import Board
from Algorithm import *
import pandas as pd
import PuzzleGenerator

TIME_LIMIT = 0
PUZZLES_NUM = 40
horizontal_list = []
vertical_list = []


#   customize new thread class for our needs
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
#   The board will kept in bytes for optimization of certain operations
def initFromString(_puzzle):
    board = np.chararray((1, 36))
    board[:] = [char for char in _puzzle]
    board = np.reshape(board, (6, 6))
    return board


#   function to insert statistics from each iteration to our goal data frame
def insertStatistics(_statistics_df, statistics_list_, heuristic_name, _puzzle, _puzzle_counter, input_solution):
    if statistics_list_[0] <= TIME_LIMIT:
        solved = 'Y'
    else:
        solved = 'N'

    new_row = [_puzzle, heuristic_name, statistics_list_[1],
               (statistics_list_[3] / statistics_list_[1]), solved, statistics_list_[0],
               (statistics_list_[1] ** (1 / statistics_list_[3])), (statistics_list_[4] / statistics_list_[1]),
               statistics_list_[7], (statistics_list_[6] / statistics_list_[1]), statistics_list_[5],
               statistics_list_[3] - input_solution]

    _statistics_df = _statistics_df.append(pd.Series(new_row, index=_statistics_df.columns, name=_puzzle_counter))

    return _statistics_df


#   function to get the input puzzles from rh.txt
def getPuzzles():
    input_puzzles = []
    with open("rh.txt", "r") as f:
        contents = f.readlines()

    i = contents.index('--- RH-input ---\n')
    for j in range(i + 1, contents.index('--- end RH-input ---\n')):
        input_puzzles.append(contents[j].split('\n')[0])

    return input_puzzles


#   function to get the suggested solutions from rh.txt
def getSolutions():
    input_solutions = []
    with open("rh.txt", "r") as f:
        contents = f.read()
        data = contents.split("Soln: ")
        data = data[1:]
        for sol in data:
            curr = sol.split(" .")

            solution = curr[0]
            solution = solution.replace("\n", " ")
            solution = solution.split(" ")
            newSolution = ""
            for move in solution:
                if move != "":
                    newSolution += move + " "

            # Turns the solutions into numbers and summing them
            solution_sum = sum(1 for x in newSolution if x.isdigit())
            input_solutions.append(solution_sum)

    # convert the solutions to integers

    return input_solutions


if __name__ == '__main__':

    command = int(input("To solve puzzle enter 1, To generate puzzle enter 2: "))
    if command == 2:
        requested_depth = int(input("Enter the depth of solution for the new puzzle: "))
        PuzzleGenerator.generetePuzzle(requested_depth)

    else:
        # getting time limit input
        TIME_LIMIT = float(input("Enter time limit for each puzzle (in seconds) : "))
        # getting puzzles from rh.txt
        PUZZLES = getPuzzles()
        SOLUTIONS = getSolutions()

        # initialize some vars
        threadLock = threading.Lock()
        threads = []
        pd.set_option('display.max_columns', None)
        columns_for_df = ['Problem ', 'Heuristic name ', 'N ', 'd/N ', 'Success (Y/N) ', 'Time (ms) ', 'EBF ',
                          'avg H value ', 'Min ', 'Avg ', 'Max ', 'Compare to input ']
        puzzle_counter = 0
        statistics_df = pd.DataFrame(columns=columns_for_df)
        solved_or_failed = [0, 0, 0, 0]
        statistics_list = list()

        heuristics = [1, 2, 3, 4]

        for heuristic in heuristics:
            for idx, puzzle in enumerate(PUZZLES):
                event = threading.Event()
                print("------------------------------------ New puzzle ------------------------------------\n")
                # create initial board
                initial_board = initFromString(puzzle)
                print(initial_board.astype('U13'), '\n')
                initial_board = Board(initial_board)

                # creates 2 threads - solving for vertical and horizontal successors of the initial board in each thread
                thread1 = myThread(1, "Thread-horizontal", 1)
                thread2 = myThread(2, "Thread-vertical", 2)
                root = GameNodes.Node(initial_board)

                # run the threads
                thread1.start()
                thread2.start()

                # Add threads to thread list
                threads.append(thread1)
                threads.append(thread2)

                thread1.join()
                thread2.join()

                # getting the output from the threads
                statistics_list_1 = threads[1].returning()
                statistics_list_0 = threads[0].returning()
                if type(statistics_list_1[2]) is not str and type(statistics_list_0[2]) is str:
                    statistics_list = statistics_list_1
                elif type(statistics_list_0[2]) is not str and type(statistics_list_1[2]) is str:
                    statistics_list = statistics_list_0
                else:
                    if statistics_list_1[0] <= statistics_list_0[0]:
                        statistics_list = statistics_list_1
                    else:
                        statistics_list = statistics_list_0

                # getting statistics and displaying the result
                if statistics_list[0] <= TIME_LIMIT and type(statistics_list[2]) is not str:
                    winner_state = statistics_list[2].astype('U13')
                    winner_state = np.array2string(winner_state.flatten(), precision=2, separator=',', suppress_small=True)
                    print(' Solution: \n', winner_state, '\n')
                    solved_or_failed[heuristic - 1] += 1
                else:
                    print(' Solution: \n', statistics_list[2], '\n')
                # insert statistics to the data frame
                if heuristic is 1:
                    statistics_df = insertStatistics(statistics_df, statistics_list, 'Advanced Blocking', puzzle,
                                                     puzzle_counter, SOLUTIONS[idx])
                elif heuristic is 2:
                    statistics_df = insertStatistics(statistics_df, statistics_list, 'Advanced Double Blocking', puzzle,
                                                     puzzle_counter, SOLUTIONS[idx])
                elif heuristic is 3:
                    statistics_df = insertStatistics(statistics_df, statistics_list, 'Vertical From Right', puzzle,
                                                     puzzle_counter, SOLUTIONS[idx])
                else:
                    statistics_df = insertStatistics(statistics_df, statistics_list, 'Uniformed search', puzzle,
                                                     puzzle_counter, SOLUTIONS[idx])
                puzzle_counter += 1
                statistics_list.clear()

        #   print final statistics and save to csv file:
        print('Global Statistics table: \n', statistics_df)
        compression_opts = dict(method='zip', archive_name='statistics.csv')
        statistics_df.to_csv('statistics.zip', index=False, compression=compression_opts)

        # print average statistics for each heuristic
        init_index = 0
        final_index = PUZZLES_NUM - 1
        heuristics = ['Advanced blocking', 'Advanced double blocking', 'Vertical from right', 'Uninformed search']
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
