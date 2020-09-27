import math
import numpy as np

# https://www.sfu.ca/~ssurjano/rastr.html
class Rastrigin:
    def __init__(self):
        self.left = -5.12
        self.right = 5.12

    def run(self, vector):
        sum = np.sum(np.power(vector, 2) - 10*np.cos(2*np.pi*vector))
        d = len(vector)
        return 10 * d + sum
