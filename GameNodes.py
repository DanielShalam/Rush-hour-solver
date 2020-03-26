import numpy as np

""" Node class """


class Node:
    # constructor
    def __init__(self, board, father=None, board_size=6, g=0):
        self.board = board
        self.father = father
        self.horizontal_cars = []
        self.vertical_cars = []
        self.successors = []  # list of moves we can do (will be added to the open list)
        self.symbols = []  # list of symbols represent different cars
        self.size = board_size
        self.g = g  # the g will be defined as the depth were looking
        self.h = 0  # the h will be defined by the heuristic value of the board state

    # function to find the cars and the way they are on the board (horizontal/vertical)
    def findCars(self):
        for row in range(0, self.size):
            for col in range(0, self.size):
                if self.board[row][col] is not '.' and self.board[row][col] not in self.symbols:
                    flag = False  # flags for letting us know if we found a car with length of 3
                    # check for vertical cars
                    if row + 2 < self.size:
                        if self.board[row + 1][col] == self.board[row][col] and self.board[row + 2][col] == \
                                self.board[row][col]:
                            self.vertical_cars.append([[row, col], [row + 1, col], [row + 2, col]])
                            self.symbols.append(self.board[row][col])
                            flag = True
                    if flag is False and row + 1 < self.size:  # if we didnt find car
                        if self.board[row + 1][col] == self.board[row][col]:
                            self.vertical_cars.append([[row, col], [row + 1, col]])
                            self.symbols.append(self.board[row][col])
                    # check for horizontal car is we didnt find vertical one from the current coordinate
                    if col + 2 < self.size and flag is False:
                        if self.board[row][col + 1] == self.board[row][col] and self.board[row][col + 2] == \
                                self.board[row][col]:
                            self.horizontal_cars.append([[row, col], [row, col + 1], [row, col + 2]])
                            self.symbols.append(self.board[row][col])
                            flag = True
                    if flag is False and col + 1 < self.size:
                        if self.board[row][col + 1] == self.board[row][col]:
                            self.horizontal_cars.append([[row, col], [row, col + 1]])
                            self.symbols.append(self.board[row][col])

    def generateSuccessors(self):
        self.findCars()  # first we will find the cars in the board state
        for car in self.vertical_cars:
            [last_row, last_col] = car[-1]  # extract the end of the car
            [first_row, first_col] = car[0]  # extract the beginning of the car
            if last_row + 1 < 6:
                if self.board[last_row + 1][last_col] == '.':
                    self.successors.append(self.makeNewBoard([last_row, last_col], 1, car, False))
            if first_row - 1 > -1:
                if self.board[last_row - 1][first_col] == '.':
                    self.successors.append(self.makeNewBoard([first_row, first_col], -1, car, False))

        for car in self.horizontal_cars:
            [last_row, last_col] = car[-1]  # extract the end of the car
            [first_row, first_col] = car[0]  # extract the beginning of the car
            if last_col + 1 < 6:
                if self.board[last_row][last_col + 1] == '.':
                    self.successors.append(self.makeNewBoard([last_row, last_col], 1, car, True))
            if first_col - 1 > -1:
                if self.board[first_row][first_col - 1] == '.':
                    self.successors.append(self.makeNewBoard([first_row, first_col], -1, car, True))

    # making the new board from the movement of the car
    def makeNewBoard(self, coordinate, index, car, is_horizontal):
        temp_board = np.copy(self.board)  # create a copy of the previous board
        row, col = coordinate  # unpacking the coordinate of part of the car in the previous board
        symbol = self.board[row][col]

        for rows, cols in car:  # cleaning the new board from the previous car
            temp_board[rows][cols] = '.'

        for rows, cols in car:
            if is_horizontal is True:  # change the coordinates due to the movement (horizontal/vertical)
                temp_board[rows][cols + index] = symbol
            else:
                temp_board[rows + index][cols] = symbol

        return Node(board=temp_board, father=self, g=self.g + 1)  # making a new Node with the new properties
