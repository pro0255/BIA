import random
import numpy as np
import matplotlib.pyplot as plt


class Solution:
    def __init__(self, dimension=2, lower_bound=0, upper_bound=0):
        self.dimension = dimension
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.vector = np.zeros(dimension)  # x,y..
        self.fitness_value = np.inf  # z..

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
        print()
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


class AbstractAlgorithm:
    def __init__(self, graph=None, size_of_population=1000, max_generation=20):
        self.size_of_population = size_of_population
        self.max_generation = max_generation
        self.graph = graph
        self.index_of_generation = 0
        self.best_solution = Solution()

    def has_attribute(self, attribute):
        if hasattr(self, attribute):
            return True
        return False

    def evaluate(self, solution, Function):
        """Sets z (fitness) value according to Function

        Args:
            solution (class Solution): input with specified vector as prop
            Function (class Function): specific Function (Sphere || Ackley..)
        """
        solution.fitness_value = Function.run(solution.vector)

    def evalute_population(self, population, Function):
        """Runs over population and evaluate every solution

        Args:
            population (Solution[])
            Function (class Function): specific Function (Sphere || Ackley..)
        """
        for solution in population:
            self.evaluate(solution, Function)

    def select_best_solution(self, population):
        """Runs over whole population and returns one with best fitness

        Args:
            population (Solution[]): whole population len(population)=self.size_of_population

        Returns:
            Solution: Solution with best fitness value
        """
        best_in_population = Solution()
        for solution in population:
            if solution.fitness_value < best_in_population.fitness_value:
                best_in_population = solution
        return best_in_population

    def generate_random_solution(self, lower_bound, upper_bound, dimension=2):
        """Generates random solution according to bounds

        Args:
            lower_bound (float)
            upper_bound (float)
            dimension (int, optional) Defaults to 2.

        Returns:
            Solution: generated Solution with inicialized random vector
        """
        random_solution = Solution(dimension, lower_bound, upper_bound)
        random_solution.fill_vector_with_random()
        return random_solution

    def generate_population(self):
        """Adds 1 to prop index_of_generation. It is used in alg as condition."""
        self.index_of_generation += 1


class BlindAgorithm(AbstractAlgorithm):
    """Blind algorithm tries to find global min/max.

    In n generated records tries to find min/max. Also takes to consideration min/max founded in last run. If current generation founded better results replace old one.

    For every record get Z value and after tries to find min/max.
    As return value is returned min/max vector with vectors of all generation values.

    Generation does not optimizes move.
    It remembers previous state.
    """

    def __init__(self, **kwds):
        super().__init__(**kwds)

    def generate_population(self, Function, dimension=2):
        """Generates population for BlindAlgorithm with random individuals

        Args:
            Function (class Function): specific Function (Sphere || Ackley..)
            dimension (int, optional): Defaults to 2.

        Returns:
            [Solution[]]: generated population as specific generation
        """
        super().generate_population()
        population = []
        for _ in range(self.size_of_population):
            population.append(
                self.generate_random_solution(Function.left, Function.right, dimension)
            )
        return population

    def start(self, Function):
        """Runs Blind Algorithm on specified Function

        Args:
            Function (class Function): specific Function (Sphere || Ackley..)
        """
        first_solution = self.generate_random_solution(Function.left, Function.right)
        self.evaluate(first_solution, Function)
        self.best_solution = first_solution

        while self.index_of_generation < self.max_generation:
            population = self.generate_population(Function)
            self.evalute_population(population, Function)
            best_in_population = self.select_best_solution(population)
            if best_in_population.fitness_value < self.best_solution.fitness_value:
                self.best_solution = best_in_population

            if self.graph:
                self.graph.draw(self.best_solution, population)


class HillClimbAlgorithm(AbstractAlgorithm):
    def __init__(self, sigma=1, **kwds):
        self.sigma = sigma
        super().__init__(**kwds)

    def generate_population(self, Function, dimension=2):
        """Generates population for HillClimbAlgorithm with np.random.normal

        Args:
            Function (class Function): specific Function (Sphere || Ackley..)
            dimension (int, optional): Defaults to 2.

        Returns:
            [Solution[]]: generated population as specific generation
        """
        super().generate_population()
        population = []
        for _ in range(self.size_of_population):
            neighbor = Solution(lower_bound=Function.left, upper_bound=Function.right)
            neighbor.fill_vector_with_gaussian(self.best_solution, self.sigma)
            population.append(neighbor)
        return population

    def start(self, Function):
        """Runs HillClimb Algorithm on specified Function, with specified args.

        Args:
            Function (class Function): specific Function (Sphere || Ackley..)
        """
        first_solution = self.generate_random_solution(Function.left, Function.right)
        self.evaluate(first_solution, Function)
        self.best_solution = first_solution

        while self.index_of_generation < self.max_generation:
            neighborhood = self.generate_population(Function)
            self.evalute_population(neighborhood, Function)
            best_in_neighborhood = self.select_best_solution(neighborhood)
            if best_in_neighborhood.fitness_value < self.best_solution.fitness_value:
                self.best_solution = best_in_neighborhood

            if self.graph:
                self.graph.draw(self.best_solution, neighborhood)



class SimulatedAnnealingAlgorithm(AbstractAlgorithm):
    def __init__(self, sigma = 1, initial_temperature=100, minimal_temperature = 0, cooling_constant = 0.9, **kwds):
        super().__init__(**kwds)
        self.initial_temperature = initial_temperature
        self.minimal_temperature = minimal_temperature
        self.cooling_constant = cooling_constant
        self.sigma = sigma

        ##cause of gui :]
        delattr(self, 'size_of_population')
        delattr(self, 'max_generation')

    def generate_population(self, Function, dimension = 2):
        super().generate_population()
        population = []
        neighbor = Solution(lower_bound=Function.left, upper_bound=Function.right)
        neighbor.fill_vector_with_gaussian(self.best_solution, self.sigma)
        population.append(neighbor)
        return population

    def start(self, Function):
        """Runs Simulated Annealing Algorithm on specified Function, with specified args.

        Args:
            Function (class Function): specific Function (Sphere || Ackley..)
        """
        print('running algorithm')
        first_solution = self.generate_random_solution(Function.left, Function.right)
        self.evaluate(first_solution, Function)
        self.best_solution = first_solution
        print(self.initial_temperature, self.minimal_temperature)
        while self.initial_temperature > self.minimal_temperature:
            neighbour = self.generate_population(Function)
            self.evaluate(neighbour[0], Function)
            if neighbour[0].fitness_value < self.best_solution.fitness_value:
                self.best_solution = neighbour[0]
            else:
                r = np.random.uniform(Function.left, Function.right)
                if r < np.exp(-((neighbour[0].fitness_value - self.best_solution.fitness_value)/self.initial_temperature)):
                    self.best_solution = neighbour[0]
            self.initial_temperature = self.initial_temperature * self.cooling_constant

            print(self.initial_temperature)
            if self.graph:
                self.graph.draw(self.best_solution, neighbour)
