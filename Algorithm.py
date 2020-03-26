from GameNodes import Node
import numpy as np

""" implementation of A* search algorithm. """


class AStar:

    def __init__(self):
        self.open_list = np.empty(100, dtype=Node)
