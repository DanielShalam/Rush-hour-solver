""" AdvancedBlocking heuristic - Admissible
    the number of cars which blocking the way to the exit +
    1 extra point for each blocking car that blocked by another car"""


def advancedBlocking(board):
    board_length = board.board_length
    board_state = board.board_state
    [main_row, main_col] = board.main_car[0][-1]  # the end of the main car (right end)
    heuristic_value = 0
    # first we will check how many vertical cars are blocking the main car
    for col in range(main_col + 1, board_length):  # from the main car to the end
        if board_state[main_row][col] != '.':
            car_symbol = board_state[main_row][col]  # the blocking car
            heuristic_value += 1  # adding 1 to the heuristic for blocking car that we found
            # now we need to check if the blocking car is blocked
            for i in range(1, board_length):
                if col + i < board_length:
                    if board_state[main_row][col + i] != '.' and board_state[main_row][col + i] != car_symbol:
                        heuristic_value += 1
                        break
                if col - i > -1:
                    if board_state[main_row][col - i] != '.' and board_state[main_row][col - i] != car_symbol:
                        heuristic_value += 1
                        break
    return heuristic_value
