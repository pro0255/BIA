

import numpy as np
from solution.Solution import Solution

class MultiSolution(Solution):
    def __init__(self, number_of_functions, **kwds):
        super().__init__(**kwds)
        self.fitness_value = np.full(number_of_functions, np.inf)
