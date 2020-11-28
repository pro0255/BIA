from solution.Solution import Solution
import time
import matplotlib.pyplot as plt
import inspect
import random
import pandas as pd

VERBOSE = False


class AbstractAlgorithm:
    def __init__(self, graph=None, size_of_population=1000, max_generation=20, D=2):
        self.size_of_population = size_of_population
        self.max_generation = max_generation
        self.graph = graph
        self.index_of_generation = 0
        self.best_solution = Solution()
        self.D = D
        self.max_OFE = None
        self.current_OFE = 0

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def has_attribute(self, attribute):
        if hasattr(self, attribute):
            return True
        return False

    def close_plot(self):
        if VERBOSE and self.graph is not None:
            counter = 5
            for i in range(counter):
                time.sleep(1)
                print(f"Closing in {i+1}-{counter}")

            if self.graph:
                print("Closing!!")
                plt.close("all")

    def print_best_solution(self):
        if VERBOSE:
            print(self.current_OFE)
            # print(f"{self.index_of_generation}-\t{self.best_solution.vector}")

    def return_after_at_the_end(self, population):
        self.best_solution = self.select_best_solution(population)
        if VERBOSE:
            print(f"\nAlgorithm {type(self).__name__} {self.current_OFE}\n")
        return (self.best_solution.fitness_value, self.__str__())

    def ofe_check(self):
        if self.max_OFE is None:
            return True
        return self.current_OFE <= self.max_OFE

    def reset_alg(self):
        self.index_of_generation = 0
        self.current_OFE = 0

    def evaluate(self, solution, Function):
        """Sets z (fitness) value according to Function

        Args:
            solution (class Solution): input with specified vector as prop
            Function (class Function): specific Function (Sphere || Ackley..)
        """
        self.current_OFE += 1
        solution.fitness_value = Function.run(solution.vector)

    def evalute_population(self, population, Function):
        """Runs over population and evaluate every solution

        Args:
            population (Solution[])
            Function (class Function): specific Function (Sphere || Ackley..)
        """
        for solution in population:
            self.evaluate(solution, Function)

    def sort_population(self, population):
        return sorted(
            population, key=lambda solution: solution.fitness_value, reverse=True
        )

    def print_population(self, population):
        [print(individual) for individual in population]

    def select_worst_solution(self, population):
        """Runs over whole population and returns one with worst fitness
        Args:
            population (Solution[]): whole population len(population)=self.size_of_population

        Returns:
            Solution: Solution with best fitness value
        """
        pop = self.sort_population(population)
        worst = pop[0]
        return worst

        return pop[0]

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

    def select_random_individual(self, population, actual_individual):
        selected = random.choice(population)
        return selected

    def print_population(self, population):
        vectors = [individual.vector for individual in population]
        print(pd.DataFrame(vectors))

    def print_population_fitness(self, population):
        f = [individual.fitness_value for individual in population]
        print(pd.DataFrame(f))

    def start(self):
        self.index_of_generation = 0
        if VERBOSE:
            print(self)

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

    def __str__(self):
        output = f"Starts algorithm {type(self).__name__} with attributes:"
        for key, value in dict(self).items():
            if not inspect.isclass(value) and not isinstance(value, Solution):
                output += f"\n\t{key} -- {value}"
        return output
