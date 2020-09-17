import math


class Michalewicz:
    def __init__(self):
        self.left = 0
        self.right = math.pi
        self.m = 10

    def run(self, vector):
        result = 0
        sum = 0
        d = len(vector)
        for i in range(d):
            sum += math.sin(
                vector[i] * pow(math.sin((i * (vector[i] ** 2)) / math.pi), self.m * 2)
            )
        result = sum
        return -result
