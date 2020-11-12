import numpy as np


class Solution:
    def __init__(self, dimension=2, lower_bound=0, upper_bound=0, key=0):
        self.dimension = dimension
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.vector = np.zeros(dimension)  # x,y..
        self.fitness_value = np.inf  # z..
        self.key = Solution.key
        self.personal_best = None  # PSO solution param
        self.velocity_vector = np.zeros(dimension)  # PSO solution param
        self.trajectory = np.zeros(dimension) #TSP solution param
        Solution.key += 1

    key = 0

    @staticmethod
    def is_in_bounderies(value, left, right):
        return value >= left and value <= right

    ##TODO!: create __eq__ for fintess_value
    def fill_vector_with_random(self):
        """Sets random vector with specified bounds"""
        self.vector = np.random.uniform(
            low=self.lower_bound, high=self.upper_bound, size=self.dimension
        )

    def fill_vector_with_gaussian(self, individual, sigma=1):
        """Sets vector using NORMAL (Gaussian) distribution with specified bounds

        Args:
            individual (class Solution): individual input
            sigma (int, optional): scale, Defaults to 1.
        """
        result = []
        for i in range(len(self.vector)):
            while True:
                generated_value = np.random.normal(individual.vector[i], sigma)
                if (
                    generated_value >= individual.lower_bound
                    and generated_value <= individual.upper_bound
                ):
                    result.append(generated_value)
                    break
        self.vector = np.array(result)

    def __str__(self):
        """ToString

        Returns:
            string: Solution.toString() --> print(Solution)
        """
        return f"Solution with\n Vector ->> {self.vector}\n Fitness ->> {self.fitness_value}"
