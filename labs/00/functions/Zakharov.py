import math

class Zakharov():
    def __init__(self):
        self.left = -5
        self.right = 10

    def run(self, vector):
        result = 0
        sum1 = 0
        sum2 = 0
        d = len(vector)
        for i in range(d):
            sum1 += vector[i] ** 2
        for i in range(d):
            sum2 += 0.5 * i * vector[i] ##same as next
        result = sum1 + pow(sum2, 2) + pow(sum2, 4)
        return result
