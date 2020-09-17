import math

# https://www.sfu.ca/~ssurjano/schwef.html


class Schwefel:
    def __init__(self):
        self.left = -500
        self.right = 500

    def run(self, vector):
        sum = 0
        d = len(vector)
        for i in range(d):
            sum += vector[i] * math.sin(math.sqrt(abs(vector[i])))
        return 418.9829 * d - sum
