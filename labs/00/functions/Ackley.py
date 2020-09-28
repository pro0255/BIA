import math
import numpy as np


class Ackley:
    def __init__(self):
        self.left = -32.768
        self.right = 32.768
        self.a = 20
        self.b = 0.2
        self.c = 2 * math.pi

    def run(self, vector):
        result = 0
        sum1 = np.sum(np.power(vector, 2))
        sum2 = np.sum(np.cos(self.c * vector))

        d = len(vector)

        result = (
            -self.a * math.exp(-self.b * math.sqrt(((1 / (d - 1)) * sum1)))
            - math.exp(((1 / (d - 1)) * sum2))
            + self.a
            + math.exp(1)
        )
        return result
