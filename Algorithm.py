import Hueristics
from FiboHeap import *
import numpy as np
from GameNodes import Node
from time import time
from math import inf
from threading import Lock

NULL_HEURISTIC = 0  # heuristic for un-informed search
lock = Lock()
sum_heuristics = 0
max_depth = 0
min_depth = inf
sum_depth = 0  # will be used to calculate average depth
nodes_counter = 0


def aStarSearch(start_node, heuristic, multi_threading, thread_id):
    global max_depth
    global min_depth
    global sum_depth
    global sum_heuristics
    global nodes_counter
    # initialize the global vars
    sum_heuristics = 0
    nodes_counter = 1
    sum_depth = 0
    max_depth = 0
    min_depth = inf
    # initialize additional vars
    round_counter = 1
    start_time = time()
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

    lock.acquire()
    sum_heuristics += f
    lock.release()

    current_string_for_hash = np.array2string(current_node.board.board_state, precision=2, separator=',',
                                              suppress_small=True)
    open_list.insert(f, current_node)
    hash_for_open[current_string_for_hash] = current_node

    while open_list.find_min() is not None:
        # Take from the open list the node current_node_ with the lowest
        # f(current_node) = g(current_node) + h(current_node)

        fib_node = open_list.extract_min()
        temp_current_node = fib_node.value

        lock.acquire()
        # check for cut-off
        if current_node.g < min_depth and round_counter != 1:
            if temp_current_node not in current_node.successors:
                min_depth = current_node.g
        lock.release()

        current_node = temp_current_node
        current_string_for_hash = np.array2string(current_node.board.board_state, precision=2, separator=',',
                                                  suppress_small=True)
        # print(current_node.board.board_state)
        closed_list[current_string_for_hash] = current_node

        if current_node.isGoal():
            elapsed_time = time() - start_time  # calculate the total time for solving
            return [elapsed_time, nodes_counter, current_node.board.board_state, current_node.g, sum_heuristics,
                    max_depth, sum_depth, min_depth]

        #   generate successors due to thread terms (only at the first time)
        if round_counter is 1 and multi_threading is True:
            if thread_id is 1:
                current_node.generateHorizontalSuccessors()
            else:
                current_node.generateVerticalSuccessors()
            round_counter += 1
        #   generate regular successors
        else:
            current_node.generateHorizontalSuccessors()
            current_node.generateVerticalSuccessors()

        for successor in current_node.successors:
            successor_string_for_hash = np.array2string(successor.board.board_state, precision=2, separator=',',
                                                        suppress_small=True)
            successor.g = current_node.g + 1

            lock.acquire()
            # check if we have new max depth
            if successor.g > max_depth:
                max_depth = successor.g
            lock.release()

            successor.h = calcHeuristic(successor.board, heuristic)
            # index_for_state_in_open = self.does_it_exist_in_open(state)
            state_in_open: Node = hash_for_open.get(successor_string_for_hash)
            exists_in_open = state_in_open is not None

            state_in_closed: Node = closed_list.get(successor_string_for_hash)
            exists_in_closed: bool = state_in_closed is not None

            if not exists_in_closed and not exists_in_open:
                f = successor.h + successor.g
                lock.acquire()
                sum_heuristics += successor.h
                nodes_counter += 1
                sum_depth += successor.g
                lock.release()
                hash_for_open[successor_string_for_hash] = successor
                open_list.insert(f, successor)

            elif exists_in_closed:
                if (state_in_closed.g + state_in_closed.h) > (successor.h + successor.g):
                    closed_list.pop(successor_string_for_hash)

                    f = successor.h + successor.g
                    lock.acquire()
                    sum_heuristics += successor.h
                    nodes_counter += 1
                    sum_depth += successor.g
                    lock.release()

                    hash_for_open[successor_string_for_hash] = successor
                    open_list.insert(f, successor)

            else:
                if (state_in_open.h + state_in_open.g) > (successor.h + successor.g):
                    # open_list.delete(((state_in_open.h + state_in_open.g), state_in_open))
                    f = successor.h + successor.g
                    lock.acquire()
                    sum_heuristics += successor.h
                    nodes_counter += 1
                    sum_depth += successor.g
                    lock.release()

                    hash_for_open[successor_string_for_hash] = successor
                    open_list.insert(f, successor)

    # if we didnt find solution at all
    if current_node.isGoal() is False:
        elapsed_time = time() - start_time  # calculate the total time for solving
        return [elapsed_time, nodes_counter, 'FAILED ', current_node.g, sum_heuristics,
                max_depth, sum_depth, min_depth]


# function to calculate the heuristic value of given board state due to the current heuristic
def calcHeuristic(successor_board, heuristic):
    # calculate heuristic value due to the heuristic number
    if heuristic is 1:
        return Hueristics.advancedBlocking(successor_board)
    elif heuristic is 2:
        return Hueristics.advancedDoubleBlocking(successor_board)
    elif heuristic is 3:
        return Hueristics.verticalFromRight(successor_board)
    else:
        return NULL_HEURISTIC
