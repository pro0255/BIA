from algorithms.AbstractGenetic import AbstractGeneticAlgorithm
import numpy as np
import copy
from solution.Solution import Solution
import pandas as pd



class FireflyAlgorithm(AbstractGeneticAlgorithm):
    def __init__(self, **kwds):
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

    def generate_individual(self, Function):
        """ TODO: 
            Function (Function): One of the cost function. (Sphere, Ackley..)
        Returns:
            [Solution]: Returns individual from population. In PSO it is called particle.
        """
        solution = self.generate_random_solution(Function.left, Function.right)
        return solution


    def start(self, Function):
        """Runs ______ Algorithm on specified Function, with specified args.
        Args:
            Function (class Function): specific Function (Sphere || Ackley..)
        """
        super().start()
        fireflies = self.generate_population(Function)
        self.print_population(fireflies)






        self.close_plot()
