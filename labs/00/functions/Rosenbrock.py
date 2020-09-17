# https://www.sfu.ca/~ssurjano/rosen.html


class Rosenbrock:
    def __init__(self):
        # -5, 10
        self.left = -2.048
        self.right = 2.048

    def run(self, vector):
        sum = 0
        for i in range(len(vector) - 1):
            sum += 100 * (pow(vector[i + 1] - vector[i], 2)) + (pow(vector[i] - 1, 2))
        return sum
