""" AdvancedBlocking heuristic - Admissible
    the number of cars which blocking the way to the exit +
    1 extra point for each blocking car that blocked by another car """


def advancedBlocking(board):
    board_length = board.board_length
    board_state = board.board_state
    [main_row, main_col] = board.main_car[-1]  # the end of the main car (right end)
    heuristic_value = 0
    # first we will check how many vertical cars are blocking the main car
    for col in range(main_col + 1, board_length):  # from the main car to the end
        if board_state[main_row][col] in board.symbols:
            car_symbol = board_state[main_row][col]  # the blocking car
            heuristic_value += 1  # adding 1 to the heuristic for blocking car that we found
            flag = False
            # now we need to check if the blocking car is blocked
            for i in range(1, board_length - main_row):
                if main_row + i < board_length and board_state[main_row + i][col] != b'.':
                    if board_state[main_row + i][col] != car_symbol:
                        flag = True
                        break
                else:
                    break

            if flag is True:
                for i in range(1, board_length - main_row):
                    if main_row - i < board_length and board_state[main_row - i][col] != b'.':
                        if board_state[main_row - i][col] != car_symbol:
                            heuristic_value += 1
                            break
                    else:
                        break

    return heuristic_value


""" AdvancedDoubleBlocking heuristic - InAdmissible
    The change from 'AdvancedBlocking' is that in this heuristic for each blocking car we will give score 3 instead of 1
    The reason is that in this way the program will try to remove the blocking cars harder than in 'AdvancedBlocking' + 
    1 extra point for each blocking car that blocked by another car  ,if its blocked from 2 sides it will get 2"""


def advancedDoubleBlocking(board):
    board_length = board.board_length
    board_state = board.board_state
    [main_row, main_col] = board.main_car[-1]  # the end of the main car (right end)
    heuristic_value = 0
    # first we will check how many vertical cars are blocking the main car
    for col in range(main_col + 1, board_length):  # from the main car to the end
        if board_state[main_row][col] in board.symbols:
            car_symbol = board_state[main_row][col]  # the blocking car
            heuristic_value += 2  # adding 1 to the heuristic for blocking car that we found
            # now we need to check if the blocking car is blocked
            for i in range(1, board_length - main_row):
                if main_row + i < board_length and board_state[main_row + i][col] != b'.':
                    if board_state[main_row + i][col] != car_symbol:
                        heuristic_value += 1
                        break
                else:
                    break

            for i in range(1, board_length - main_row):
                if main_row - i < board_length and board_state[main_row - i][col] != b'.':
                    if board_state[main_row - i][col] != car_symbol:
                        heuristic_value += 1
                        break
                else:
                    break

    return heuristic_value


""" VerticalFromRight heuristic - InAdmissible
    Calculates the Number of vertical cars to the right of the main car  +
    1 extra point for each vertical car with length 3"""


def verticalFromRight(board):
    board_length = board.board_length
    board_state = board.board_state
    [main_row, main_col] = board.main_car[-1]  # the end of the main car (right end)
    heuristic_value = 0
    for i in range(1, board_length - main_col):
        for row in range(0, board_length - 1):
            if board_state[row][main_col + i] != b'.' and board_state[row][main_col + i] == \
                    board_state[row + 1][main_col + i]:
                heuristic_value += 1

    return heuristic_value
