from algorithms.AbstractGenetic import AbstractGeneticAlgorithm
from solution.Solution import Solution
import numpy as np
import random


class GeneticAlgorithmTSP(AbstractGeneticAlgorithm):
    def __init__(self, number_of_cities=20, low=0, high=200, **kwds):
        """
            NP = size_of_population
            G = max_generation

            If can starts from different citis then need to be fixed_first_index set to False :]

            CONVENCTION!!! but here is renamed cause consistency
        Args:
            number_of_cities (int): D, it will be a number of cities
        """
        super().__init__(**kwds)
        self.number_of_cities = number_of_cities
        self.low = low
        self.high = high
        self.generate_cities()
        self.fixed_first_index = True  # first city will be not moved

    def generate_cities(self):
        self.cities = np.random.uniform(
            size=(self.number_of_cities, 2), low=self.low, high=self.high
        )

    def generate_individual(self, cities):
        """Generating single individual according to input
        Shuffle cities

        If fixed_first_index then always starts from one point and this will be not moved when alg moves forward

        Returns:
            []: [description]
        """
        individual = Solution()
        if self.fixed_first_index:
            first = list(self.cities)[0]
            without_first = list(self.cities)[1:]
            shuffled = random.sample(without_first, len(without_first))
            result = [first] + shuffled
            individual.vector = np.array(result)
        else:
            individual.vector = np.array(
                random.sample(list(self.cities), len(self.cities))
            )

        return individual

    def generate_population(self, cities):
        """Generating NP random individuals"""
        super().generate_population()
        population = [
            self.generate_individual(cities) for _ in range(self.size_of_population)
        ]

        return population

    def start(self, EucladianDistance):
        super().start()
        self.generate_cities()
        population = self.generate_population(self.cities)
        self.evalute_population(population, EucladianDistance)

        for _ in range(self.max_generation):
            new_population = self.copy(population)
            self.best_solution = self.select_best_solution(population)
            if self.graph:
                self.graph.draw(self.best_solution)

            for j in range(len(population)):
                parent_A = population[j]
                parent_B = self.get_different_individual_then_input(
                    population, parent_A
                )
                try:
                    offspring_AB = self.crossover(parent_A, parent_B)
                    if self.gonna_mutate():
                        offspring_AB = self.mutate(
                            offspring_AB, 1 if self.fixed_first_index else 0
                        )
                    self.evaluate(offspring_AB, EucladianDistance)

                    if (
                        offspring_AB.fitness_value < parent_A.fitness_value
                    ):  ##if is better then his parent
                        new_population[j] = offspring_AB

                except Exception as error:
                    print(f"something wrong {error}")
                    print(traceback.print_exc())
                    continue
            population = new_population

        self.close_plot()
