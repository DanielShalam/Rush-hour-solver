import Hueristics
from FiboHeap import *


def aStarSearch(start_node):
    open_list = FibonacciHeap()
    closed_list = dict()
    current_node = start_node
    f = Hueristics.advancedBlocking(start_node.board)
    open_list.insert(f, start_node.board.board_state, start_node)
    while open_list.min_node is not None:
        # Take from the open list the node current_node_ with the lowest
        # f(current_node) = g(current_node) + h(current_node)

        temp_fibo_node = open_list.extract_min()
        current_node = temp_fibo_node.game_node
        print(current_node.h)
        print(current_node.board.board_state)

        if current_node.isGoal():
            return current_node

        current_node.generateHorizontalSuccessors()
        current_node.generateVerticalSuccessors()

        for successor in current_node.successors:
            successor.g = current_node.g + 1
            successor.h = Hueristics.advancedBlocking(successor.board)
            successor_evaluation_value = successor.g + successor.h
            board_to_check = successor.board.board_state
            bytes_board = board_to_check.tobytes()
            for fibo_node in open_list.iterate(open_list.root_list):

                if fibo_node is None:
                    open_list.insert(successor_evaluation_value, board_to_check, successor)
                    break

                elif (board_to_check == fibo_node.value).all():
                    if successor.g <= current_node.g:
                        continue

                elif bytes_board in closed_list.keys():
                    if successor.g <= current_node.g:
                        continue

                    # move successor from closed_list back to open_list
                    open_list.insert(successor_evaluation_value, board_to_check, successor)
                    del closed_list[bytes_board]
                    break

                else:

                    open_list.insert(successor_evaluation_value, board_to_check, successor)
                    successor.h = Hueristics.advancedBlocking(successor.board)
                    break

                closed_list.update({bytes_board: successor})

    if current_node.isGoal() is False:
        return None


# TODO - implement A* using threshold which is given from IDA*
""" IDA* search Algorithm - Uses information from each search to limit the search by Threshold value.
    The Threshold value will be the smallest value that we found in the previous search that bigger from the previous Threshold.
    In A* we will expend nodes which are smaller or equal to the given Threshold."""


def IDAStar(node):
    threshold = 0
    is_goal_node_found = False
    while is_goal_node_found is False:
        new_scores, is_goal_node_found = aStarSearch(node)
        passed = (x for x in new_scores if x > threshold)
        threshold = min(passed)
