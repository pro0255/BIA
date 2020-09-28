import math
import numpy as np


class Zakharov:
    def __init__(self):
        self.left = -5
        self.right = 10

    def run(self, vector):
        result = 0
        d = len(vector)
        i_vector = np.arange(1, d + 1)
        sum1 = np.sum(np.power(vector, 2))
        sum2 = np.sum(0.5 * i_vector * vector)
        result = sum1 + math.pow(sum2, 2) + math.pow(sum2, 4)
        return result
