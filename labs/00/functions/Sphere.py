#https://www.sfu.ca/~ssurjano/spheref.html

class Sphere():
    def __init__(self):
        self.left = -5.12
        self.right = 5.12

    def run(self, vector):
        sum = 0
        for i in range(len(vector)):
            sum += pow(vector[i], 2)
        return sum

