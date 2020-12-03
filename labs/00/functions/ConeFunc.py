import numpy as np


class ConeFunc:
    def __init__(self):
        pass

    def sub_calculation(self, vector):
        return np.sqrt(np.sum(np.power(vector, 2)))
