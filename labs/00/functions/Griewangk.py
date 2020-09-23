import math

# https://www.sfu.ca/~ssurjano/griewank.html
class Griewangk:
    def __init__(self):
        self.left = -600
        self.right = 600

    def run(self, vector):
        result = 0
        d = len(vector)
        sum = 0
        product = 0
        for i in range(d):
            sum += pow(vector[i], 2) / 4000
            product_value = 0
            try:
                product_value = math.cos(vector[i] / math.sqrt(i))
            except:
                product_value = 0

            product += product_value
        result = sum - product + 1
        return result
