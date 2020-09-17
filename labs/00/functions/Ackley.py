import math


class Ackley:
    def __init__(self):
        self.left = -32.768
        self.right = 32.768
        self.a = 20
        self.b = 0.2
        self.c = 2 * math.pi

    def run(self, vector):
        result = 0
        sum1 = 0
        sum2 = 0
        d = len(vector)
        for i in range(d):
            sum1 += vector[i] ** 2
        for i in range(d):
            sum2 += math.cos(self.c * vector[i])

        result = (
            -self.a * math.exp(-self.b * math.sqrt(((1 / (d - 1)) * sum1)))
            - math.exp(((1 / (d - 1)) * sum2))
            + self.a
            + math.exp(1)
        )
        return result
