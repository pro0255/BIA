from algorithms.AbstractGenetic import AbstractGeneticAlgorithm
import numpy as np
import copy
from solution.Solution import Solution



class FireflyAlgorithm(AbstractGeneticAlgorithm):
    def __init__(self, **kwds):
        super().__init__(**kwds)

    def generate_population(self, Function):
        pass

    def generate_individual(self, Function):
        pass

    def start(self, Function):
        """Runs ______ Algorithm on specified Function, with specified args.
        Args:
            Function (class Function): specific Function (Sphere || Ackley..)
        """
        super().start()
        print('firefly algorithm')
