import Hueristics
from FiboHeap import *
import numpy as np
from GameNodes import Node


def aStarSearch(start_node):
    nodes_counter = 0
    hash_for_open = {}
    open_list = FibonacciHeap()
    closed_list = dict()
    current_node = start_node
    f = Hueristics.advancedBlocking(start_node.board)
    current_string_for_hash = np.array2string(current_node.board.board_state, precision=2, separator=',',
                                              suppress_small=True)
    open_list.insert(f, current_node)
    hash_for_open[current_string_for_hash] = current_node

    while open_list.find_min() is not None:
        # Take from the open list the node current_node_ with the lowest
        # f(current_node) = g(current_node) + h(current_node)

        fib_node = open_list.extract_min()
        current_node = fib_node.value
        current_string_for_hash = np.array2string(current_node.board.board_state, precision=2, separator=',',
                                                  suppress_small=True)
        nodes_counter += 1
        # print(current_node.board.board_state)
        closed_list[current_string_for_hash] = current_node

        if current_node.isGoal():
            print("Solution: \n", current_node.board.board_state)
            print("Number of checked nodes:", nodes_counter)
            return

        current_node.generateHorizontalSuccessors()
        current_node.generateVerticalSuccessors()

        for successor in current_node.successors:
            successor_string_for_hash = np.array2string(successor.board.board_state, precision=2, separator=',',
                                                        suppress_small=True)
            successor.g = current_node.g + 1
            successor.h = Hueristics.advancedBlocking(successor.board)
            successor_evaluation_value = successor.g + successor.h
            # index_for_state_in_open = self.does_it_exist_in_open(state)
            state_in_open: Node = hash_for_open.get(successor_string_for_hash)
            exists_in_open = state_in_open is not None

            state_in_closed: Node = closed_list.get(successor_string_for_hash)
            exists_in_closed: bool = state_in_closed is not None

            if not exists_in_closed and not exists_in_open:
                hash_for_open[successor_string_for_hash] = successor
                f = successor.h + successor.g
                open_list.insert(f, successor)

            elif exists_in_closed:
                if (state_in_closed.g + state_in_closed.h) > (successor.h + successor.g):
                    closed_list.pop(successor_string_for_hash)
                    hash_for_open[successor_string_for_hash] = successor
                    f = successor.h + successor.g
                    open_list.insert(f, successor)

            else:

                if (state_in_open.h + state_in_open.g) > (successor.h + successor.g):
                    #open_list.delete(((state_in_open.h + state_in_open.g), state_in_open))
                    hash_for_open[successor_string_for_hash] = successor
                    f = successor.h + successor.g
                    open_list.insert(f, successor)

                    # self.actual_game.move_car(state.car_name, self.get_opp_side(state.direction), state.steps)

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
        aStarSearch(node)
        #passed = (x for x in new_scores if x > threshold)
        #threshold = min(passed)
