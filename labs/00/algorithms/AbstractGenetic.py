from algorithms.Abstract import AbstractAlgorithm
import numpy as np
from solution.Solution import Solution
import random
import copy


class AbstractGeneticAlgorithm(AbstractAlgorithm):
    def __init__(self, **kwds):
        super().__init__(**kwds)

    def copy(self, population):
        return copy.deepcopy(population)

    def crossover(self, parent_A, parent_B):
        length = len(parent_A.vector)
        random_position_in_range = random.randint(0, length - 1)
        part_A = parent_A.vector[0:random_position_in_range, :]

        rest = []
        for city in parent_B.vector:
            is_there = np.any(part_A == city)
            if not is_there:
                rest.append(list(city))

        crossover_vector = np.concatenate((part_A, np.array(rest)), axis=0)
        offspring_AB = Solution()
        offspring_AB.vector = crossover_vector
        return offspring_AB

    def mutate(self, offspring_AB, fixed=0):
        first_index = int(np.random.uniform(fixed, len(offspring_AB.vector)))
        second_index = int(np.random.uniform(fixed, len(offspring_AB.vector)))
        if first_index != second_index:
            offspring_AB.vector[[first_index, second_index], :] = offspring_AB.vector[
                [second_index, first_index], :
            ]
            return offspring_AB
        else:
            return self.mutate(offspring_AB)

    def get_different_individual_then_input(self, population, parent_A):
        selected = self.select_random_individual(population, parent_A)
        if selected.key != parent_A.key:
            return selected
        return self.get_different_individual_then_input(population, parent_A)

    def gonna_mutate(self):
        return 0.5 > np.random.uniform(0, 1)
