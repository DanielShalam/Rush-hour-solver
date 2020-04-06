""" Node class """


class Node:
    # constructor
    def __init__(self, board, father=None, g=0):
        self.board = board
        self.father = father
        self.successors = []  # list of moves we can do (will be added to the open list)
        self.g = g  # the g will be defined as the depth were looking
        self.h = 0  # the h will be defined by the heuristic value of the board state

    def generateVerticalSuccessors(self):
        board_state = self.board.board_state
        v_cars = self.board.vertical_cars
        length = self.board.board_length

        for car in v_cars:
            [lower_row, last_col] = car[-1]  # extract the end of the car
            [upper_row, first_col] = car[0]  # extract the beginning of the car
            for i in range(1, 6):
                if upper_row - i > -1 and board_state[upper_row - i][last_col] == b'.':
                    new_board = self.board.makeNewBoard([upper_row, last_col], -i, car, False)
                    self.successors.append(Node(board=new_board, father=self, g=self.g + 1))
                else:
                    break

            for i in range(1, 6):
                if lower_row + i < length and board_state[lower_row + i][first_col] == b'.':
                    new_board = self.board.makeNewBoard([lower_row, last_col], i, car, False)
                    self.successors.append(Node(board=new_board, father=self, g=self.g + 1))
                else:
                    break

    def generateHorizontalSuccessors(self):
        board_state = self.board.board_state
        h_cars = self.board.horizontal_cars
        length = self.board.board_length

        for car in h_cars:
            [upper_row, last_col] = car[-1]  # extract the end of the car
            [lower_row, first_col] = car[0]  # extract the beginning of the car
            for i in range(1, 6):
                if last_col + i < length and board_state[upper_row][last_col + i] == b'.':
                    new_board = self.board.makeNewBoard([upper_row, last_col], i, car, True)
                    self.successors.append(Node(board=new_board, father=self, g=self.g + 1))
                else:
                    break

            for i in range(1, 6):
                if first_col - i > -1 and board_state[lower_row][first_col - i] == b'.':
                    new_board = self.board.makeNewBoard([lower_row, first_col], -i, car, True)
                    self.successors.append(Node(board=new_board, father=self, g=self.g + 1))
                else:
                    break

    def isGoal(self):
        main_row, main_col = self.board.main_car[-1]
        index = 0
        for i in range(1, self.board.board_length - main_col):
            index = i
            if self.board.board_state[main_row][main_col + i] != b'.':
                return False

        # Draw and return the Winning board
        self.board = self.board.makeNewBoard([main_row, main_col], index, self.board.main_car, True)
        return True
