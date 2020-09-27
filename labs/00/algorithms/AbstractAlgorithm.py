import random

class AbstractAlgorithm():
    def __init__(self):
        self.solution = []

    def evaluate(self, individual):
        self.solution = self.solution if self.solution[2] < individual[2] else individual   

    def get_generation(self, size_generation, Func):
        generation = [self.get_individial(Func) for _ in range(size_generation)]
        return generation

    def get_individial(self, Func):
        x = random.uniform(Func.left, Func.right)
        y = random.uniform(Func.left, Func.right)
        z = Func.run([x, y])
        return [x, y, z]
    
