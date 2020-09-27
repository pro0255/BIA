import math
import numpy as np

# https://www.sfu.ca/~ssurjano/schwef.html


class Schwefel:
    def __init__(self):
        self.left = -500
        self.right = 500

    def run(self, vector):
        sum = np.sum(vector * np.sin(np.sqrt(np.absolute(vector))))
        d = len(vector)
        return 418.9829 * d - sum
