""" AdvancedBlocking heuristic - Admissible
    the number of cars which blocking the way to the exit +
    1 extra point for each blocking car that blocked by another car"""


def advancedBlocking(board):
    board_length = board.board_length
    board_state = board.board_state
    [main_row, main_col] = board.main_car[-1]  # the end of the main car (right end)
    heuristic_value = 0
    # first we will check how many vertical cars are blocking the main car
    for col in range(main_col + 1, board_length):  # from the main car to the end
        if board_state[main_row][col] in board.symbols:
            car_symbol = board_state[main_row][col]  # the blocking car
            heuristic_value += 5  # adding 1 to the heuristic for blocking car that we found
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
    for col in range(main_col + 1, board_length):
        for row in range(0, board_length):
            if board_state[row][col] != b'.' and board_state[row][col] == board_state[row + 1][col]:
                heuristic_value += 1

    return heuristic_value
