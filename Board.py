import numpy as np


class Board:
    # constructor
    def __init__(self, board_state, board_length=6):
        self.board_state = board_state
        self.main_car = []  # the coordinate of the main car on the board
        self.horizontal_cars = []
        self.vertical_cars = []
        self.symbols = []  # list of symbols represent different cars
        self.board_length = board_length

    # function to find the cars and the way they are on the board (horizontal/vertical)
    def findCars(self):
        for row in range(0, self.board_length):
            for col in range(0, self.board_length):
                if self.board_state[row][col] is not '.' and self.board_state[row][col] not in self.symbols:
                    flag = False  # flags for letting us know if we found a car with length of 3
                    # check for vertical cars
                    if row + 2 < self.board_length:
                        if self.board_state[row + 1][col] == self.board_state[row][col] and self.board_state[row + 2][
                            col] == \
                                self.board_state[row][col]:
                            self.vertical_cars.append([[row, col], [row + 1, col], [row + 2, col]])
                            self.symbols.append(self.board_state[row][col])
                            flag = True
                    if flag is False and row + 1 < self.board_length:  # if we didnt find car
                        if self.board_state[row + 1][col] == self.board_state[row][col]:
                            self.vertical_cars.append([[row, col], [row + 1, col]])
                            self.symbols.append(self.board_state[row][col])
                    # check for horizontal car is we didnt find vertical one from the current coordinate
                    if col + 2 < self.board_length and flag is False:
                        if self.board_state[row][col + 1] == self.board_state[row][col] and self.board_state[row][
                            col + 2] == \
                                self.board_state[row][col]:
                            if self.board_state[row][col] == 'X':   # if the car is the main car
                                self.main_car.append([[row, col], [row, col + 1], [row, col + 2]])
                            else:
                                self.horizontal_cars.append([[row, col], [row, col + 1], [row, col + 2]])
                            self.symbols.append(self.board_state[row][col])
                            flag = True
                    if flag is False and col + 1 < self.board_length:
                        if self.board_state[row][col + 1] == self.board_state[row][col]:
                            if self.board_state[row][col] == 'X':   # if the car is the main car
                                self.main_car.append([[row, col], [row, col + 1]])
                            else:
                                self.horizontal_cars.append([[row, col], [row, col + 1]])
                            self.symbols.append(self.board_state[row][col])

    # making the new board from the movement of the car
    def makeNewBoard(self, coordinate, index, car, is_horizontal):
        temp_board = np.copy(self.board_state)  # create a copy of the previous board
        row, col = coordinate  # unpacking the coordinate of part of the car in the previous board
        symbol = self.board_state[row][col]

        for rows, cols in car:  # cleaning the new board from the previous car
            temp_board[rows][cols] = '.'

        for rows, cols in car:
            if is_horizontal is True:  # change the coordinates due to the movement (horizontal/vertical)
                temp_board[rows][cols + index] = symbol
            else:
                temp_board[rows + index][cols] = symbol
        return Board(board_state=temp_board)  # making a new Board object with the new properties
