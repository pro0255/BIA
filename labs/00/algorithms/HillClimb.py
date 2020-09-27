
import random
import matplotlib.pyplot as plt

class AbstractAlgorithm():
    def __init__(self, graph, max_iterations = 1000, max_generation = 20):
        self.solution = []
        self.max_iterations = max_iterations
        self.max_generation = max_generation
        self.graph = graph

    def fitness(self, individual):
        return individual[2]

    def evaluate(self, individual):
        if self.fitness(self.solution) < self.fitness(individual):
            return False
        else:
            self.solution = individual
            return True


        self.solution = self.solution if self.fitness(self.solution) < self.fitness(individual) else individual   

    def get_generation(self, size_generation, left_bound, right_bound, Func):
        generation = []
        for _ in range(size_generation):
            generation.append(self.get_individial(left_bound, right_bound, Func))
        return generation

    def get_individial(self, left_bound, right_bound, Func):
        x = random.uniform(left_bound, right_bound)
        y = random.uniform(left_bound, right_bound)
        z = Func.run([x,y])
        return [x, y, z]

    def fitness_in_generation(self, generation):
        for item in generation:
            if not self.solution:
                self.solution = item
            self.evaluate(item)


class HillClimbAlgorithm(AbstractAlgorithm):
 
    def __init__(self, r, **kwds):
        self.r = r
        super().__init__(**kwds)

    def run(self, Func):
        individual = self.get_individial(Func.left, Func.left, Func)
        self.solution = individual

        iteration = 0
        while iteration < self.max_iterations:

            point = self.graph.scatter(
                self.solution[0],
                self.solution[1],
                self.solution[2],
                s=20,
                alpha=1,
                c="red",
                marker="o",
            )
            plt.pause(0.09)
            plt.draw()
            point.remove()
            generation = self.get_generation(self.max_generation, self.solution[0] - self.r, self.solution[0] + self.r, Func)
            self.fitness_in_generation(generation)
            iteration += 1


        