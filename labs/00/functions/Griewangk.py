import math
import numpy as np

# https://www.sfu.ca/~ssurjano/griewank.html
class Griewangk:
    def __init__(self):
        self.left = -600
        self.right = 600

    def run(self, vector):
        result = 0
        d = len(vector)
        sum = np.sum(np.power(vector, 2)/4000)
        product = np.product(np.cos(vector/np.sqrt(2)))
        result = sum - product + 1
        return result
