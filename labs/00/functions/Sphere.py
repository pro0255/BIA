import numpy as np
# https://www.sfu.ca/~ssurjano/spheref.html


class Sphere:
    def __init__(self):
        self.left = -5.12
        self.right = 5.12

    def run(self, vector):
        result = np.sum(np.power(vector, 2))
        return result
