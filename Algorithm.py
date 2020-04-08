import Hueristics
from FiboHeap import *
import numpy as np
from GameNodes import Node
from time import time
from math import inf

# heuristic for un-informed search
NULL_HEURISTIC = 0


def aStarSearch(start_node, heuristic):
    # initialize some vars
    sum_heuristics = 0
    max_depth = 0
    sum_depth = 0
    min_depth = inf
    start_time = time()
    nodes_counter = 0
    hash_for_open = {}
    open_list = FibonacciHeap()
    closed_list = dict()
    current_node = start_node
    if heuristic is 1:
        f = Hueristics.advancedBlocking(start_node.board)
    elif heuristic is 2:
        f = Hueristics.advancedDoubleBlocking(start_node.board)
    elif heuristic is 3:
        f = Hueristics.verticalFromRight(start_node.board)
    else:
        f = NULL_HEURISTIC

    sum_heuristics += f

    current_string_for_hash = np.array2string(current_node.board.board_state, precision=2, separator=',',
                                              suppress_small=True)
    open_list.insert(f, current_node)
    hash_for_open[current_string_for_hash] = current_node

    while open_list.find_min() is not None:
        # Take from the open list the node current_node_ with the lowest
        # f(current_node) = g(current_node) + h(current_node)

        fib_node = open_list.extract_min()
        temp_current_node = fib_node.value
        if current_node.g < max_depth and temp_current_node not in current_node.successors:
            min_depth = current_node.g

        current_node = temp_current_node
        current_string_for_hash = np.array2string(current_node.board.board_state, precision=2, separator=',',
                                                  suppress_small=True)
        # print(current_node.board.board_state)
        closed_list[current_string_for_hash] = current_node

        if current_node.isGoal():
            elapsed_time = time() - start_time  # calculate the total time for solving
            return [elapsed_time, nodes_counter, current_node.board.board_state, current_node.g, sum_heuristics,
                    max_depth, sum_depth, min_depth]

        current_node.generateHorizontalSuccessors()
        current_node.generateVerticalSuccessors()

        for successor in current_node.successors:
            nodes_counter += 1
            successor_string_for_hash = np.array2string(successor.board.board_state, precision=2, separator=',',
                                                        suppress_small=True)
            successor.g = current_node.g + 1

            # check if we have new max depth
            if successor.g > max_depth:
                max_depth = successor.g

            sum_depth += successor.g
            # calculate heuristic value
            if heuristic is 1:
                successor.h = Hueristics.advancedBlocking(start_node.board)
            elif heuristic is 2:
                successor.h = Hueristics.advancedDoubleBlocking(start_node.board)
            elif heuristic is 3:
                successor.h = Hueristics.verticalFromRight(start_node.board)
            else:
                successor.h = NULL_HEURISTIC

            sum_heuristics += successor.h
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
                    # open_list.delete(((state_in_open.h + state_in_open.g), state_in_open))
                    hash_for_open[successor_string_for_hash] = successor
                    f = successor.h + successor.g
                    open_list.insert(f, successor)

                    # self.actual_game.move_car(state.car_name, self.get_opp_side(state.direction), state.steps)

    # if we didnt find solution at all
    if current_node.isGoal() is False:
        elapsed_time = time() - start_time  # calculate the total time for solving
        return [elapsed_time, nodes_counter, 'FAILED ', current_node.g, sum_heuristics,
                max_depth, sum_depth, min_depth]


# TODO - implement A* using threshold which is given from IDA*
""" IDA* search Algorithm - Uses information from each search to limit the search by Threshold value.
    The Threshold value will be the smallest value that we found in the previous search that bigger from the previous Threshold.
    In A* we will expend nodes which are smaller or equal to the given Threshold."""


def IDAStar(node):
    threshold = 0
    is_goal_node_found = False
    while is_goal_node_found is False:
        aStarSearch(node)
        # passed = (x for x in new_scores if x > threshold)
        # threshold = min(passed)
