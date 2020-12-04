from algorithms.AbstractGenetic import AbstractGeneticAlgorithm
from selection.ParetoRank import dominated_sorting
from solution.MultiSolution import MultiSolution
from constants import HEIGHT, RADIUS
from constants.MULTI_OPTIMIZATION_OBJECTIVE import TASK_APPROACHES
import numpy as np
import copy


class NonDominatedGeneticAlgorithm(AbstractGeneticAlgorithm):
    def __init__(self, **kwds):
        super().__init__(**kwds)

    def generate_population(self, Functions):
        return [
            self.generate_individual_for_specific_task(Functions)
            for _ in range(self.size_of_population)
        ]

    def evalute_population(self, population, Functions):
        for individual in population:
            for index, func in enumerate(Functions):
                individual.fitness_value[index] = func.run(individual.vector)

    def generate_individual_for_specific_task(self, Functions):
        individual = MultiSolution(len(Functions), dimension=2)
        r = np.random.uniform(low=RADIUS.RADIUS_LOW, high=RADIUS.RADIUS_HIGH)
        h = np.random.uniform(low=HEIGHT.HEIGHT_LOW, high=HEIGHT.HEIGHT_HIGH)
        individual.vector = np.array([r, h])
        return individual

    def make_specific_clip(self, cross):
        # if not (cross[0] > RADIUS.RADIUS_LOW and cross[0] <  RADIUS.RADIUS_HIGH):
        #     cross[0] =  np.random.uniform(low=RADIUS.RADIUS_LOW, high=RADIUS.RADIUS_HIGH)
        # if not (cross[1] > HEIGHT.HEIGHT_LOW and cross[0] <  HEIGHT.HEIGHT_HIGH):
        #     cross[0] = np.random.uniform(low=HEIGHT.HEIGHT_LOW, high=HEIGHT.HEIGHT_HIGH)
        cross[0] = np.clip(cross[0], RADIUS.RADIUS_LOW, RADIUS.RADIUS_HIGH)
        cross[1] = np.clip(cross[1], HEIGHT.HEIGHT_LOW, HEIGHT.HEIGHT_HIGH)
        return cross

    def crossover(self, a, b):
        r = np.random.uniform()
        if r < 0.5:
            return (a.vector + b.vector) / 2
        else:
            return (a.vector - b.vector) / 2

    def mutate(self, cross):
        r = np.random.uniform()
        if r < 0.5:
            return cross + np.random.uniform(0, 1, self.D)
        else:
            return cross

    def construct_solution(self, cross, Functions):
        individual = MultiSolution(len(Functions))
        individual.vector = cross
        return individual

    def start(self, Functions):
        """Runs ______ Algorithm on specified Function, with specified args.
        Args:
            Function (class Function): specific Function (Sphere || Ackley..)
        """
        super().start()
        population = self.generate_population(Functions)
        # self.print_population(population)
        self.evalute_population(population, Functions)

        for _ in range(self.max_generation):
            new_population = copy.deepcopy(population)
            new_generated = []
            for j in range(len(population)):
                a = population[j]
                b = self.get_different_individual_then_input(population, a)
                vector = self.make_specific_clip(self.mutate(self.crossover(a, b)))
                child = self.construct_solution(vector, Functions)
                new_generated.append(child)

            new_population += new_generated
            self.evalute_population(new_generated, Functions)
            Qs, new_population_selected = dominated_sorting(
                new_population, Functions, TASK_APPROACHES, self.size_of_population
            )
            population = new_population_selected
            if self.graph:
                self.graph.draw(new_population, Qs[0])
# 