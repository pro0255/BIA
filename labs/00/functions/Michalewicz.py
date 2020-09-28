import math
import numpy as np


class Michalewicz:
    def __init__(self):
        self.left = 0
        self.right = math.pi
        self.m = 10

    def run(self, vector):
        result = 0
        d = len(vector)
        i_vector = np.arange(1, d + 1)
        sum = np.sum(
            np.sin(vector)
            * np.power(np.sin((np.power(vector, 2) * i_vector) / np.pi), 2 * self.m)
        )
        result = sum
        return -result
