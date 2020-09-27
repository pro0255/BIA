import random
import numpy as np
import matplotlib.pyplot as plt


class Solution:
    def __init__(self, dimension = 2, lower_bound = 0, upper_bound = 0):
        self.dimension = dimension
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.vector = np.zeros(dimension) #x,y..
        self.fitness_value = np.inf #z..

    def fill_vector_with_random(self):
        self.vector = np.random.uniform(low=self.lower_bound, high=self.upper_bound, size=self.dimension)
    
    def fill_vector_with_gaussian(self, individual, sigma = 1):
        self.vector = np.random.normal(individual.vector, sigma)

    def __str__(self):
        return f'Solution with\n Vector ->> {self.vector}\n Fitness ->> {self.fitness_value}'



class AbstractAlgorithm():
    def __init__(self, graph, size_of_population = 1000, max_generation = 20):
        self.size_of_population = size_of_population
        self.max_generation = max_generation
        self.graph = graph
        self.index_of_generation = 0
        self.best_solution = Solution()

    def evaluate(self, solution, Function):
        solution.fitness_value = Function.run(solution.vector)

    def evalute_population(self, population, Function):
        for solution in population:
            self.evaluate(solution, Function)

    def select_best_solution(self, population):
        best_in_population = Solution()
        for solution in population:
            if solution.fitness_value < best_in_population.fitness_value:
                best_in_population = solution
        return best_in_population

    def generate_random_solution(self, lower_bound, upper_bound, dimension = 2):
        random_solution = Solution(dimension, lower_bound, upper_bound)
        random_solution.fill_vector_with_random()
        return random_solution

    def generate_population(self):
        self.index_of_generation += 1


class BlindAgorithm(AbstractAlgorithm):
    """
    Blind algorithm tries to find global min/max.

    In n generated records tries to find min/max. Also takes to consideration min/max founded in last run. If current generation founded better results replace old one.

    For every record get Z value and after tries to find min/max.
    As return value is returned min/max vector with vectors of all generation values.

    Generation does not optimizes move.
    It remembers previous state.
    """
    def __init__(self, **kwds):
         super().__init__(**kwds)

    def generate_population(self, Function, dimension = 2):
        super().generate_population()
        population = []
        for _ in range(self.size_of_population):
            population.append(self.generate_random_solution(Function.left, Function.right, dimension))
        return population

    def start(self, Function):
        first_solution = self.generate_random_solution(Function.left, Function.right)
        self.evaluate(first_solution, Function)
        self.best_solution = first_solution

        while self.index_of_generation < self.max_generation:
            population = self.generate_population(Function)
            self.evalute_population(population, Function)
            best_in_population = self.select_best_solution(population)
            if best_in_population.fitness_value < self.best_solution.fitness_value:
                self.best_solution = best_in_population
        
            print(self.index_of_generation)
            self.graph.draw(self.best_solution, population)


class HillClimbAlgorithm(AbstractAlgorithm):
    def __init__(self, sigma, **kwds):
        self.sigma = sigma
        super().__init__(**kwds)


    def generate_population(self, Function, dimension = 2):
        super().generate_population()
        population = []
        for _ in range(self.size_of_population):
            neighbor = Solution()
            neighbor.fill_vector_with_gaussian(self.best_solution, self.sigma)
            population.append(neighbor)
        return population

    def start(self, Function):
        first_solution = self.generate_random_solution(Function.left, Function.right)
        self.evaluate(first_solution, Function)
        self.best_solution = first_solution


        while self.index_of_generation < self.max_generation:
            neighborhood = self.generate_population(Function)
            self.evalute_population(neighborhood, Function)
            best_in_neighborhood = self.select_best_solution(neighborhood)
            if best_in_neighborhood.fitness_value < self.best_solution.fitness_value:
                self.best_solution = best_in_neighborhood

            print(self.index_of_generation)

            self.graph.draw(self.best_solution, neighborhood)