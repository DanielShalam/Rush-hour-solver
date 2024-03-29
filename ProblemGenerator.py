import numpy as np
from itertools import groupby
from Board import Board
import GameNodes
import random
import Hueristics
import Algorithm


# generate puzzle
# add the red car
# keep adding cars while the depth of solution (return value of A*) is less then difficulty
# place the new cars in blocking places 66% (selected from list)  or in random location 33%
# add the blocking points of new added cars to list


def makePuzzle(difficulty):
    limit_depth = difficulty
    two_squares_car_symbols = ["A", "B", "C", "D", "E", "F"]  # list of symbols represent different cars
    three_squares_car_symbols = ["O", "P", "Q"]  # list of symbols represent different cars
    two_squares_car_symbols_index = 0
    three_squares_car_symbols_index = 0
    blocking_cells_of_cars = []

    # start with empty board
    empty_board = np.chararray((1, 36))
    empty_board[:] = ['....................................']
    empty_board = np.reshape(empty_board, (6, 6))

    print(empty_board)
    # add the red (XX) car on random index at the 3rd (second in the array) line
    red_car_head_index = random.randint(0, 3)

    empty_board[2][red_car_head_index] = "X"
    empty_board[2][red_car_head_index + 1] = "X"

    blocking_cells_of_cars.append(12 + red_car_head_index + 2)

    empty = Board(empty_board)
    # while depth value of the board is less then difficulty add cars
    new_node = GameNodes.Node(empty)
    depth = 0  # 0 first iteration
    print(empty_board)
    while depth < limit_depth:
        empty = Board(empty_board)
        new_node = GameNodes.Node(empty)
        listed = Algorithm.aStarSearch(new_node, 1, multi_threading=False, thread_id=None)
        depth = listed[3]
        print(depth)

        car_type = random.randint(0, 1)  # 0 for 2 square 1 for 3 square
        direction = random.randint(0, 1)  # 0 for vertical position 1 for horizontal
        if car_type == 0:
            board_limit_index = 4
        else:
            board_limit_index = 3

        block_or_random_placement_flag = random.randint(0, 2)  # prioritize blocking over randomness
        if block_or_random_placement_flag == 1 or block_or_random_placement_flag == 2:
            block_or_random_placement_flag = 1

        if block_or_random_placement_flag == 0:  # 0 => choose random cell for the head of the car
            car_head = random.randint(0, 34)
        else:
            car_head = random.choice(blocking_cells_of_cars)

        #  place the car
        if isLegalPlacement(empty_board, car_head, direction, car_type):
            if canFit(empty_board, car_head, direction, car_type) \
                    and doesNotBlockRedCar(car_head, direction, red_car_head_index) \
                    and doesNotBlockingFullLineRow(empty_board, car_head, direction, car_type):
                if car_type == 0 and len(two_squares_car_symbols) != 0:  # 2 square car
                    putCar(empty_board, car_head, direction, car_type, two_squares_car_symbols,
                           three_squares_car_symbols)
                elif car_type == 1 and len(three_squares_car_symbols) != 0:  # 3 square truck
                    putCar(empty_board, car_head, direction, car_type, two_squares_car_symbols,
                           three_squares_car_symbols)

                #  after adding car
                new_blocking_point = findBlockingCell(empty_board, car_head, direction, car_type)
                if new_blocking_point != -1 and (new_blocking_point not in blocking_cells_of_cars):
                    blocking_cells_of_cars.append(new_blocking_point)
        new_board = Board(empty_board)
        print(new_board.board_state)

    return new_board


def isLegalPlacement(board_state, car_head, direction, car_type):
    # direction 0 for vertical position 1 for horizontal
    # car_type 0 for 2 square 1 for 3 square

    # check if boundaries are legal
    vertical_index = int(car_head / 6)
    horizontal_index = int(car_head % 6)

    if direction == 1:  # horizontal placement
        if car_type == 0 and vertical_index == 5:
            return 0
        elif car_type == 1 and vertical_index >= 4:
            return 0
        else:
            return 1

    elif direction == 0:  # vertical placement
        if car_type == 0 and horizontal_index == 5:
            return 0
        elif car_type == 1 and horizontal_index >= 4:
            return 0
        else:
            return 1
    else:
        return 1


def canFit(board_state, car_head, direction, car_type):
    vertical_index = int(car_head / 6)
    horizontal_index = int(car_head % 6)
    empty_board = board_state
    if isLegalPlacement(empty_board, car_head, direction, car_type) == 0:
        return 0

    if direction == 0:  # vertical placement of cars
        if car_type == 0:  # 2 square car
            if (empty_board[horizontal_index][vertical_index] == b'.') and (
                    empty_board[horizontal_index + 1][vertical_index] == b'.'):
                return 1
        else:  # 3 square car
            if (empty_board[horizontal_index][vertical_index] == b'.') and (
                    empty_board[horizontal_index + 1][vertical_index] == b'.') and (
                    empty_board[horizontal_index + 2][vertical_index] == b'.') and horizontal_index <= 4:
                return 1

    elif direction == 1:  # horizontal placement of cars
        if car_type == 0:  # 2 square car
            if (empty_board[horizontal_index][vertical_index] == b'.') and (
                    empty_board[horizontal_index][vertical_index + 1] == b'.') and vertical_index <= 4:
                return 1
        else:  # 3 square car
            if (empty_board[horizontal_index][vertical_index] == b'.') and (
                    empty_board[horizontal_index][vertical_index + 1] == b'.') and (
                    empty_board[horizontal_index][vertical_index + 2] == b'.') and horizontal_index <= 3:
                return 1

    else:
        return 0


def putCar(board_state, car_head, direction, car_type, two_squares_car_symbols, three_squares_car_symbols):
    vertical_index = int(car_head / 6)
    horizontal_index = int(car_head % 6)

    # select symbol
    if car_type == 0:  # 2 square car
        symbol = two_squares_car_symbols[0]
    else:
        symbol = three_squares_car_symbols[0]

    if direction == 0:  # vertical placement of cars
        if car_type == 0:  # 2 square car
            board_state[horizontal_index][vertical_index] = symbol
            board_state[horizontal_index + 1][vertical_index] = symbol
        else:  # 3 square car
            board_state[horizontal_index][vertical_index] = symbol
            board_state[horizontal_index + 1][vertical_index] = symbol
            board_state[horizontal_index + 2][vertical_index] = symbol
    else:  # direction == 1:  # horizontal placement of cars
        if car_type == 0:  # 2 square car
            board_state[horizontal_index][vertical_index] = symbol
            board_state[horizontal_index][vertical_index + 1] = symbol
        else:  # 3 square car
            board_state[horizontal_index][vertical_index] = symbol
            board_state[horizontal_index][vertical_index + 1] = symbol
            board_state[horizontal_index][vertical_index + 2] = symbol

    #  remove car symbol from list
    if car_type == 0:  # 2 square car
        two_squares_car_symbols.remove(symbol)
    else:
        three_squares_car_symbols.remove(symbol)


def findBlockingCell(board_state, car_head, direction, car_type):
    # cells enumerated 0-35
    left_wall_cells = [0, 6, 12, 18, 24, 30]
    right_wall_cells = [5, 11, 17, 23, 29, 35]
    car_right_boundaries_cells = [4, 10, 16, 22, 28, 34]
    truck_right_boundaries_cells = [3, 9, 15, 21, 27, 33]
    vertical_index = int(car_head / 6)
    horizontal_index = int(car_head % 6)

    if direction == 0:  # direction 0 for vertical position 1 for horizontal
        if car_type == 0:  # car_type 0 for 2 square 1 for 3 square
            if car_head <= 5:
                cell = car_head + 12
            elif 24 <= car_head <= 29:
                cell = car_head - 6
            elif 30 <= car_head <= 35:
                return -1
            else:
                cell = random.choice([car_head - 6, car_head + 12])
        else:  # car_type == 1 truck
            if car_head <= 5:
                cell = car_head + 18
            elif 18 <= car_head <= 23:
                cell = car_head - 6
            elif 24 <= car_head <= 35:
                return -1
            else:
                cell = random.randint(car_head - 6, car_head + 12)

    else:  # direction == 1 horizontal
        if car_type == 0:  # car_type 0 for 2 square 1 for 3 square
            if car_head in left_wall_cells:
                cell = car_head + 2
            elif car_head in car_right_boundaries_cells:
                cell = car_head - 1
            elif car_head in right_wall_cells:
                return -1
            else:
                cell = random.choice([car_head - 1, car_head + 2])
        else:  # car_type == 1 truck
            if car_head in left_wall_cells:
                cell = car_head + 3
            elif car_head in truck_right_boundaries_cells:
                cell = car_head - 1
            elif car_head in right_wall_cells or car_head in car_right_boundaries_cells:
                return -1
            else:
                cell = random.choice([car_head - 1, car_head + 3])

    if board_state[horizontal_index][vertical_index] == b'.':
        return cell
    else:
        return -1


# make sure not blocking the front the red car with horizontal car placement
def doesNotBlockRedCar(car_head, direction, red_car_head_index):
    if direction == 1:  # horizontal
        if car_head < red_car_head_index:
            return 0
    return 1


# make sure not blocking the full line/row - 2 trucks or 3 cars in same line
def doesNotBlockingFullLineRow(board_state, car_head, direction, car_type):
    truck_right_blocking_cells = [3, 9, 15, 21, 27, 33]
    truck_left_blocking_cells = [0, 6, 12, 18, 24, 30]
    truck_bottom_blocking_cells = [18, 19, 20, 21, 22, 23]
    truck_upper_blocking_cells = [0, 1, 2, 3, 4, 5]

    trucks_symbols = ["O", "P", "Q"]  # list of truck symbols
    two_squares_car_symbols = ["A", "B", "C", "D", "E", "F"]  # list of cars symbols
    vertical_index = int(car_head / 6)
    horizontal_index = int(car_head % 6)

    if car_type == 1:  # truck
        if direction == 1:  # horizontal
            # check for line with truck
            if car_head in truck_right_blocking_cells:
                if (board_state[horizontal_index][vertical_index - 1] == board_state[horizontal_index][
                    vertical_index - 2]) and \
                        (board_state[horizontal_index][vertical_index - 2] == board_state[horizontal_index][
                            vertical_index - 3]):
                    return 0
            elif car_head in truck_left_blocking_cells:
                if (board_state[horizontal_index][vertical_index + 3] == board_state[horizontal_index][
                    vertical_index + 4]) and \
                        (board_state[horizontal_index][vertical_index + 4] == board_state[horizontal_index][
                            vertical_index + 5]):
                    return 0

        else:  # vertical
            # check for row with truck
            if car_head in truck_upper_blocking_cells:
                if (board_state[horizontal_index + 3][vertical_index] == board_state[horizontal_index + 4][
                    vertical_index]) and \
                        (board_state[horizontal_index + 4][vertical_index] == board_state[horizontal_index + 5][
                            vertical_index]):
                    return 0
            elif car_head in truck_bottom_blocking_cells:  # [18, 19, 20, 21, 22, 23]
                if (board_state[horizontal_index - 1][vertical_index] == board_state[horizontal_index - 2][
                    vertical_index]) and \
                        (board_state[horizontal_index - 2][vertical_index] == board_state[horizontal_index - 3][
                            vertical_index]):
                    return 0

    else:  # car
        if direction == 1:
            cars_count = 0
            line_symbols = []
            for i in range(0, 6):
                if board_state[horizontal_index][i] != b'.':
                    line_symbols.append(board_state[horizontal_index][i])
            pairs_count = [len(list(group)) for key, group in groupby(line_symbols)]
            for count in pairs_count:
                if count == 2:
                    cars_count = cars_count + 1
            if cars_count == 2:
                return 0
        else:  # direction == 0 horizontal
            cars_count = 0
            row_symbols = []
            for i in range(0, 6):
                if board_state[i][vertical_index] != b'.':
                    row_symbols.append(board_state[i][vertical_index])
            pairs_count = [len(list(group)) for key, group in groupby(row_symbols)]
            for count in pairs_count:
                if count == 2:
                    cars_count = cars_count + 1
            if cars_count == 2:
                return 0

    return 1
