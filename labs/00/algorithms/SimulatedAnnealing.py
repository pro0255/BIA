
from algorithms.Abstract import AbstractAlgorithm
from solution.Solution import Solution
import numpy as np

class SimulatedAnnealingAlgorithm(AbstractAlgorithm):
    def __init__(
        self,
        sigma=1,
        initial_temperature=100,
        minimal_temperature=0,
        cooling_constant=0.9,
        **kwds,
    ):
        super().__init__(**kwds)
        self.initial_temperature = initial_temperature
        self.minimal_temperature = minimal_temperature
        self.cooling_constant = cooling_constant
        self.sigma = sigma

        ##cause of gui :]
        delattr(self, "size_of_population")
        delattr(self, "max_generation")

    def generate_population(self, Function, dimension=2):
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
        super().start()
        first_solution = self.generate_random_solution(Function.left, Function.right)
        self.evaluate(first_solution, Function)
        self.best_solution = first_solution
        while self.initial_temperature > self.minimal_temperature:
            neighbourhood = self.generate_population(Function)
            neighbour = neighbourhood[0]
            self.evaluate(neighbour, Function)
            if neighbour.fitness_value < self.best_solution.fitness_value:
                self.best_solution = neighbour
            else:
                r = np.random.uniform(0, 1)
                if r < np.exp(
                    -((neighbour.fitness_value - self.best_solution.fitness_value))
                    / self.initial_temperature
                ):
                    self.best_solution = neighbour
            self.initial_temperature = self.initial_temperature * self.cooling_constant

            print(self.initial_temperature)
            if self.graph:
                self.graph.draw(self.best_solution, neighbourhood)