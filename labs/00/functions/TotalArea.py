import math
import numpy as np

class TotalArea:
    def __init__(self):
        pass

    def sub_calculation(self, vector):
        return np.sqrt(np.sum(np.power(vector, 2)))

    def run(self, vector):
        return math.pi*vector[0]*(vector[0]+self.sub_calculation(vector))
