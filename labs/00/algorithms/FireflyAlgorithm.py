from algorithms.AbstractGenetic import AbstractGeneticAlgorithm
import numpy as np
import copy
from solution.Solution import Solution
import pandas as pd
import math



class FireflyAlgorithm(AbstractGeneticAlgorithm):
    def __init__(self, absorption_coefficient=1, attractivness_coefficient=1, alpha=1, **kwds):
        self.absorption_coefficient = absorption_coefficient
        self.attractivness_coefficient = attractivness_coefficient
        self.alpha = alpha
        super().__init__(**kwds)

    def generate_population(self, Function):
        """Generates population according to Function with help of method generate_individual.
        Args:
            Function (Function): One of the cost function. (Sphere, Ackley..)
        Returns:
            [Solution[]]: Returns whole population with particles.
        """
        return [
            self.generate_individual(Function) for i in range(self.size_of_population)
        ]

    def generate_random_distribution_vector(self):
        return np.random.normal(0,1,size=self.dimension)

    def generate_random_movement(self): 
        return self.alpha*self.generate_random_distribution_vector()

    def generate_individual(self, Function):
        """ TODO: 
            Function (Function): One of the cost function. (Sphere, Ackley..)
        Returns:
            [Solution]: Returns individual from population. In PSO it is called particle.
        """
        solution = self.generate_random_solution(Function.left, Function.right)
        return solution

    def calculate_light_intensity(self, individual, distance=1):
        new_light_intensity = individual.fitness_value * math.exp(-self.absorption_coefficient*distance)
        return new_light_intensity

    def calculate_attractivness(self, a, b, distance):
        return self.attractivness_coefficient/(1+distance)

    def calculate_new_random_position(self, individual, Function):
        new_position = individual.vector + self.generate_random_movement()
        new_position = np.clip(new_position, Function.left, Function.right)
        possible_fitness = Function.run(new_position)
        if individual.fitness_value > possible_fitness:
            individual.vector = new_position
            individual.fitness_value = possible_fitness  
        

    def calculate_new_position(self, individual, towards_individual, distance, Function):
        new_position = individual.vector + self.calculate_attractivness(individual, towards_individual, distance) * (towards_individual.vector - individual.vector) + self.generate_random_movement()
        new_position = np.clip(new_position, Function.left, Function.right)
        individual.vector = new_position

    def start(self, Function):
        """Runs ______ Algorithm on specified Function, with specified args.
        Args:
            Function (class Function): specific Function (Sphere || Ackley..)
        """
        super().start()
        self.index_of_generation = 0
        fireflies = self.generate_population(Function)
        self.dimension = fireflies[0].dimension
        self.evalute_population(fireflies, Function)
        self.best_solution = self.select_best_solution(fireflies)

        while self.index_of_generation < self.max_generation:
            for i in range(self.size_of_population):
                fireflyI = fireflies[i]

                if fireflyI.key == self.best_solution.key:
                    beforeMoveSolution = copy.deepcopy(fireflyI)
                    self.calculate_new_random_position(fireflyI, Function)
                    if self.graph:
                        self.graph.draw_with_vector(fireflyI, beforeMoveSolution, None, False)
                        self.graph.draw(self.best_solution, fireflies)
                    continue

                savedfireflyI = copy.deepcopy(fireflyI)
                if self.graph:
                    self.graph.refresh_path()
                    self.graph.draw_extra_population(savedfireflyI, None, "black", "start_position")
                    
                for j in range(self.size_of_population):
                    fireflyJ = fireflies[j]
                    distance = np.linalg.norm(fireflyI.vector-fireflyJ.vector)
                    if self.calculate_light_intensity(fireflyI, distance) > self.calculate_light_intensity(fireflyJ, distance):
                        beforeMoveSolution = copy.deepcopy(fireflyI)
                        self.calculate_new_position(fireflyI, fireflyJ, distance, Function)
                        self.best_solution = self.select_best_solution(fireflies)
                        if self.graph:
                            self.graph.draw_with_vector(fireflyI, beforeMoveSolution, fireflyJ, True)
                            self.graph.draw(self.best_solution, fireflies)
                    self.evaluate(fireflyI, Function)
        self.close_plot()
