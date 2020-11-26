from algorithms.AbstractGenetic import AbstractGeneticAlgorithm
import numpy as np
import random
import copy
from solution.Solution import Solution


class DifferentialEvolutionAlgorithm(AbstractGeneticAlgorithm):
    def __init__(self, crossover_range=0.5, mutation_constant=0.5, **kwds):
        """
        NP = size_of_population
        G = max_generation
        F = new parametr, [mutation constant]
        CR = new parametr, [crossover range]
        """
        self.crossover_range = crossover_range
        self.mutation_constant = mutation_constant
        super().__init__(**kwds)

    def generate_population(self, Function):
        return [
            self.generate_individual(Function) for i in range(self.size_of_population)
        ]

    def generate_individual(self, Function):
        return self.generate_random_solution(Function.left, Function.right)

    def get_random_indicies(self, black_list):
        r = random.randint(0, self.size_of_population - 1)
        if r not in black_list:
            return r
        else:
            return self.get_random_indicies(black_list)

    def get_n_random_indicies(self, number_of_indicies, default_black_list):
        indicies = []
        scope_black_list = copy.copy(default_black_list)
        while len(indicies) != number_of_indicies:
            i = self.get_random_indicies(scope_black_list)
            scope_black_list.append(i)
            indicies.append(i)
        return indicies

    def mutate(self, indicies, population, Function):
        mutation_vector = (
            population[indicies[1]].vector - population[indicies[2]].vector
        ) * self.mutation_constant + population[indicies[3]].vector
        return np.clip(mutation_vector, Function.left, Function.right)
        # TODO!: take care for boundaries!

    def crossover(self, iteration_individual, mutation_vector):
        trial_solution = Solution()  # trial_vector
        dimension = len(trial_solution.vector)
        random_position_j = np.random.randint(0, dimension)

        for j in range(dimension):
            if np.random.uniform() < self.crossover_range or j == random_position_j:
                trial_solution.vector[j] = mutation_vector[j]
            else:
                trial_solution.vector[j] = iteration_individual.vector[j]

        return trial_solution

    def start(self, Function):
        """Runs DifferentialEvolution Algorithm on specified Function, with specified args.
        Args:
            Function (class Function): specific Function (Sphere || Ackley..)
        """
        super().start()
        self.index_of_generation = 0
        pop = self.generate_population(Function)
        self.evalute_population(pop, Function)

        while self.index_of_generation < self.max_generation:
            new_population = self.copy(
                pop
            )  # class scoped function.., actually it is deepcopy
            self.best_solution = self.select_best_solution(new_population)
            if self.graph:
                self.graph.draw(self.best_solution, new_population)
            for i, individual in enumerate(new_population):
                trial_solution = self.crossover(
                    individual,
                    self.mutate(
                        [i] + self.get_n_random_indicies(3, [i]), pop, Function
                    ),
                )
                self.evaluate(trial_solution, Function)

                if trial_solution.fitness_value <= individual.fitness_value:
                    new_population[i] = trial_solution
            self.print_best_solution()
            self.index_of_generation += 1
            pop = new_population
        self.close_plot()
