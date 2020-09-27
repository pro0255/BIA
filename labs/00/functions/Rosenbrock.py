# https://www.sfu.ca/~ssurjano/rosen.html


class Rosenbrock:
    def __init__(self):
        # -5, 10
        self.left = -2.048
        self.right = 2.048

    def run(self, vector):
        sum = 0
        for i in range(len(vector) - 1):
            next_value = vector[i + 1]
            current_value = vector[i]
            sum += 100*pow(next_value - pow(current_value, 2), 2) + pow(current_value-1,2)
        return sum
