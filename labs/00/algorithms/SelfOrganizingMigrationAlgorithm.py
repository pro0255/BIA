from algorithms.AbstractGenetic import AbstractGeneticAlgorithm
import numpy as np
import copy


class SelfOrganizingMigrationAlgorithm(AbstractGeneticAlgorithm):
    def __init__(self, path_length=3, step=0.11, PRT=0.1, min_div=0, **kwds):
        self.path_length = path_length
        self.step = step
        self.PRT = PRT
        self.min_div = min_div
        super().__init__(**kwds)

    def generate_population(self, Function):
        """Generates init population for alg. Individuals rand from random uniform.
        Args:
            Function (Function): Sphere Ackley..
        Returns:
            [Solution[]]: Generated population as array of Solutin class.
        """
        return [
            self.generate_individual(Function) for i in range(self.size_of_population)
        ]

    def generate_individual(self, Function):
        """Generates single individual. Method is used in generated population.
        Args:
            Function (Function): Sphere Ackley..
        Returns:
            [Solution]: Generated Solution class, where vector of parameters is populated with random uniform values in bounderies.
        """
        return self.generate_random_solution(Function.left, Function.right)

    def generate_PRTVector(self, d=2):
        """It is kind of mutation.
        Args:
            d (int, optional): Dimension. Defaults to 2.
        Returns:
            [int[]]: Perturbation vector.
        """
        PRTVector = np.random.uniform(size=d)
        return np.where(PRTVector < self.PRT, 0, 1)

    def calculate_position(self, a, b, PRTVector, step):
        """Generates new positon according to formula.
        Args:
            a (float[]): Start position.
            b (float[]): Directional vector. B - A formula.
            PRTVector (float[]): Generated PRTVector accroding to formula. Populated with [0, 1].
            step ([float): Current step.
        Returns:
            [float[]]: New position.
        """
        return a + (b - a) * step * PRTVector

    def get_pair_all_to_one(self):
        """Returns vector when is used AllToOne strategy.
        Returns:
            [float[]]: Vector with best fitness value. It is selected from population.
        """
        return self.best_solution.vector

    def individual_path_all_to_one(self, solution, get_pair):
        """Runs step logic. Where for individual is generated set of new positions. Tries to find global extrem.
        Args:
            solution (Solution): Current individual.
            get_pair (func): Method which returns vector. It can be used in implementation fo more strategies. [AllToAllAdaptive, AllToOneRand..]
        Returns:
            [Solution[]]: Populated vector with solutions.
        """
        path_solutions = []
        t = 0
        first_vector = solution.vector
        while t < self.path_length:
            second_vector = get_pair()
            new_position = self.calculate_position(
                first_vector,
                second_vector,
                self.generate_PRTVector(solution.dimension),
                t,
            )
            new_position = np.clip(
                new_position, solution.lower_bound, solution.upper_bound
            )
            new_solution = copy.deepcopy(solution)
            new_solution.vector = new_position
            path_solutions.append(new_solution)
            t += self.step
        return path_solutions

    def crossover(self, solution, Function):
        """Method which selects for current input individual solution with best fitness. New one || old is returned according this selection.
            Also draw search to graph a replaces values from graph.
        Args:
            solution (Solution): Current individual.
            Function (Function): Sphere, Ackley..
        Returns:
            [Solution]: Best solution on all generated solutions for specific individual.
        """
        possible_solutions = self.individual_path_all_to_one(
            solution, self.get_pair_all_to_one
        )
        self.evalute_population(possible_solutions, Function)
        best = self.select_best_solution(possible_solutions)
        if self.graph:
            self.graph.draw_extra_population(best, possible_solutions)
        return best

    def terminate_parameters_check(self, population):
        """At the of algorithm checks parameters which can terminate algorithm earlier.
            Selects best and worst, makes diff, abs and check (textbooks error??).
        Args:
            population (Solution[]): Current population.=
        Returns:
            [boolean]: According to condition return boolean. If true then terminate.
        """
        best = self.select_best_solution(population)
        worst = self.select_worst_solution(population)
        diff = abs(best.fitness_value - worst.fitness_value)
        return diff < self.min_div

    def start(self, Function):
        """Runs ______ Algorithm on specified Function, with specified args.
        Args:
            Function (class Function): specific Function (Sphere || Ackley..)
        """
        super().start()
        population = self.generate_population(Function)
        self.evalute_population(population, Function)

        while self.index_of_generation < self.max_generation:
            new_population = copy.deepcopy(population)
            self.best_solution = self.select_best_solution(population)

            if self.graph:
                self.graph.draw(self.best_solution, population)

            for individual_index, individual in enumerate(population):
                migrated_individual = None
                if individual.key == self.best_solution.key:
                    migrated_individual = (
                        self.best_solution
                    )  # leader should stay on his position
                else:
                    migrated_individual = self.crossover(individual, Function)
                new_population[individual_index] = migrated_individual
            population = new_population

            if self.terminate_parameters_check(population):
                print("Found best enough!!")
                break

            self.index_of_generation += 1
        self.close_plot()
