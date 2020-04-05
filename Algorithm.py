from GameNodes import Node
import numpy as np
from queue import PriorityQueue
from collections import deque
import Hueristics
import Board


def aStarSearch(start_node):
    open_list = PriorityQueue()
    closed_list = set()
    current_node = start_node
    f = Hueristics.advancedBlocking(start_node.board)
    open_list.put((f, start_node))

    while open_list.empty() is False:
        # Take from the open list the node current_node_ with the lowest
        # f(current_node) = g(current_node) + h(current_node)

        f_value, current_node = open_list.get()
        print(current_node)
        if current_node.isGoal():
            return current_node

        current_node.generateVerticalSuccessors()
        current_node.generateHorizontalSuccessors()

        for successor in current_node.successors:
            successor.g = current_node.g + 1
            successor.h = Hueristics.advancedBlocking(successor.board)
            successor_evaluation_value = successor.g + successor.h

            if successor in open_list:
                if successor.g <= current_node.g:
                    continue

            elif successor in closed_list:
                if successor.g <= current_node.g:
                    continue

                # move successor from closed_list back to open_list
                open_list.put(successor_evaluation_value, successor)
                closed_list.remove(successor)

            else:

                open_list.put(successor_evaluation_value, successor)
                successor.h = Hueristics.advancedBlocking(successor.board)

            closed_list.add(current_node)

    if current_node.isGoal() != 1:
        return "none"


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
