import math


def getWi(xi):
    return 1 + ((xi - 1) / 4)


class Levy:
    def __init__(self):
        self.left = -10
        self.right = 10

    def run(self, vector):
        result = 0
        d = len(vector)
        sum = 0

        wi = 0
        for i in range(d - 1):
            wi += getWi(vector[i])

        for i in range(d - 1):
            sum += pow((wi - 1), 2) * (1 + 10 * pow(math.sin(math.pi * wi + 1), 2))

        partOne = pow(math.sin(math.pi * vector[0]), 2)
        partTwo = pow(vector[d - 1] - 1, 2) * (
            1 + pow(math.sin(2 * math.pi * vector[d - 1]), 2)
        )
        result = partOne + sum + partTwo
        return result
