
from algorithms.AbstractGenetic import AbstractGeneticAlgorithm
import numpy as np
import copy

class SelfOrganizingMigrationAlgorithm(AbstractGeneticAlgorithm):
    def __init__(self, path_length=3,step=0.11, PRT=0.1, min_div=0.001, **kwds):
        self.path_length = path_length
        self.step = step
        self.PRT = PRT
        self.min_div = min_div
        super().__init__(**kwds)

    def generate_population(self, Function):
        return [
            self.generate_individual(Function) for i in range(self.size_of_population)
        ]

    def generate_individual(self, Function):
        return self.generate_random_solution(Function.left, Function.right)

    def generate_PRTVector(self, d=2):
        """ It is kind of mutation.
        Args:
            d (int, optional): Dimension. Defaults to 2.
        Returns:
            [int[]]: Perturbation vector.
        """
        PRTVector = np.random.uniform(size=d)
        return np.where(PRTVector < self.PRT, 0, 1)

    def calculate_position(self, a, b, PRTVector, step):
        return a + (b - a)*step*PRTVector

    def get_pair_all_to_one(self):
        return self.best_solution.vector

    def individual_path_all_to_one(self, solution, get_pair):
        path_solutions = []
        t = 0
        first_vector = solution.vector
        while t < self.path_length:
            second_vector = self.best_solution.vector
            new_position = self.calculate_position(first_vector, second_vector, self.generate_PRTVector(solution.dimension), t)
            new_position = np.clip(new_position, solution.lower_bound, solution.upper_bound) 
            new_solution = copy.deepcopy(solution)
            new_solution.vector = new_position
            path_solutions.append(new_solution)
            t += self.step
        return path_solutions


    def crossover(self, solution, Function):    
        possible_solutions = self.individual_path_all_to_one(solution, self.get_pair_all_to_one)
        self.evalute_population(possible_solutions, Function)
        best = self.select_best_solution(possible_solutions)
        if self.graph:
            self.graph.draw_extra_population(possible_solutions)        
        return best 
    
    def terminate_parameters_check(self, population):
        return False

    def start(self, Function):
        """Runs ______ Algorithm on specified Function, with specified args.
        Args:
            Function (class Function): specific Function (Sphere || Ackley..)
        """
        super().start()
        population = self.generate_population(Function)
        self.evalute_population(population, Function)

        while self.index_of_generation < self.max_generation:
            print(self.index_of_generation)
            new_population = copy.deepcopy(population)
            self.best_solution = self.select_best_solution(population)

            if self.graph:
                self.graph.draw(self.best_solution, population)

            for individual_index, individual in enumerate(population):
                migrated_individual = self.crossover(individual, Function)                
                new_population[individual_index] = migrated_individual
            population = new_population
            if(self.terminate_parameters_check(population)):
                break

            self.index_of_generation += 1
        self.close_plot()
            
