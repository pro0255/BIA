import numpy as np

class Solution:
    def __init__(self, dimension, lower_bound, upper_bound):
        self.dimension = dimension
        self.lower_bound = lower_bound  # we will use the same bounds for all parameters
        self.upper_bound = upper_bound
        self.vector = np.zeros(dimension) #solution parameters
        self.fitness_value = np.inf  # objective function evaluation
