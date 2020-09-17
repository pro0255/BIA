import math

#https://www.sfu.ca/~ssurjano/rastr.html
class Rastrigin():
    def __init__(self):
        self.left = -5.12
        self.right = 5.12

    def run(self, vector):
        sum = 0
        d = len(vector)
        for i in range(d):
            sum += pow(vector[i], 2) - 10*math.cos(2*math.pi*vector[i])
        return 10*d + sum
