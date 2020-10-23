import random
import numpy as np
import matplotlib.pyplot as plt
import time
import traceback
import copy
import inspect

##TODO!: Kind of separation :]]]]


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


class AbstractAlgorithm:
    def __init__(self, graph=None, size_of_population=1000, max_generation=20):
        self.size_of_population = size_of_population
        self.max_generation = max_generation
        self.graph = graph
        self.index_of_generation = 0
        self.best_solution = Solution()

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def has_attribute(self, attribute):
        if hasattr(self, attribute):
            return True
        return False

    def close_plot(self):
        counter = 5
        for i in range(counter):
            time.sleep(1)
            print(f"Closing in {i+1}-{counter}")

        if self.graph:
            print("Closing!!")
            plt.close("all")

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

    def select_random_individual(self, population, actual_individual):
        selected = random.choice(population)
        return selected

    def start(self):
        self.index_of_generation = 0
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
        super().start()
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
        super().start()
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
        self.close_plot()


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

            self.index_of_generation += 1
            pop = new_population
        self.close_plot()


class ParticleSwarmOptimizationAlgorithm(AbstractGeneticAlgorithm):
    def __init__(self, c1=0, c2=0, v_min=0, v_max=0, **kwds):
        """
        𝑝𝑜𝑝_𝑠𝑖𝑧𝑒 = size_of_population [number of individuals]
        𝑀_𝑚𝑎𝑥 = max_generation [number of migration cycles]
        𝑐_1, 𝑐_2 = new parametr, [learning constants]
        𝑣_𝑚𝑖𝑛𝑖, 𝑣_𝑚𝑎𝑥𝑖 = new parametr, [minimal and maximal velocity]

        #! v-max according to textbooks is vmax generated as 1/20 space scope of p[i]
        #! c_1 c_2 by user, common interval = [0, 4] - common value = 2
        #! pop_size - normally 10 - 20, max 40-50, it is possible value like 100 but computation time takes to long

        """
        self.v_min = v_min
        self.v_max = v_max
        self.c1 = c1
        self.c2 = c2
        super().__init__(**kwds)

    def generate_velocity_vector(self, solution):
        solution.velocity_vector = np.random.uniform(
            low=self.v_min, high=self.v_max, size=solution.dimension
        )

    def generate_velocity_vectors_for_paricles(self, swarm):
        [self.generate_velocity_vector(individual) for individual in swarm]

    def generate_population(self, Function):
        return [
            self.generate_individual(Function) for i in range(self.size_of_population)
        ]

    def generate_individual(self, Function):
        solution = self.generate_random_solution(Function.left, Function.right)
        solution.personal_best = copy.deepcopy(solution)
        return solution

    def calculate_new_velocity(self, solution):
        """Calculated velocity vector moves individual according to 3 directions:
            -> current
            -> my best
            -> gloval best

        Args:
            solution ([type]): [description]
        """
        r1 = np.random.uniform()
        r2 = np.random.uniform()
        new_velocity_vector = (
            self.calculate_inertia_weight() * solution.velocity_vector
            + r1 * self.c1 * (solution.personal_best.vector - solution.vector)
            + r2 * self.c2 * (self.best_solution.vector - solution.vector)
        )
        solution.velocity_vector = np.clip(new_velocity_vector, self.v_min, self.v_max)

    def calculate_new_position(self, solution):
        """Calculates new positon of particle

            According to textbooks when value is out of bounderies then is generated new random position

        Args:
            solution ([type]): [description]
        """
        new_position = solution.vector + solution.velocity_vector
        # solution.vector = np.clip(new_position, solution.lower_bound, solution.upper_bound) #!old one
        #! new one
        for index, param in enumerate(new_position):
            if not Solution.is_in_bounderies(
                param, solution.lower_bound, solution.upper_bound
            ):
                new_position[index] = np.random.uniform(
                    low=solution.lower_bound, high=solution.upper_bound
                )

        solution.vector = new_position

    def calculate_inertia_weight(self, w_start=0.9, w_end=0.4):
        """CZ - [Setrvacnost]

            It is used cause in the beginning of alg is searched large space then at the end..-> global optimum
            ..with time -> local optimum

            Default values - [Xiaodong, 2007]
        Args:
            w_start (float, optional): Sometimes is specified by user. Defaults to 0.9.
            w_end (float, optional): Sometimes is specified by user. Defaults to 0.4.



        Returns:
            int: calculated value according to iteration and max generation value
        """
        return w_start - (
            ((w_start - w_end) * self.index_of_generation) / self.max_generation
        )

    def is_better_then_personal_best(self, solution):
        return (
            solution.personal_best is None
            or solution.fitness_value < solution.personal_best.fitness_value
        )

    def is_better_then_global_best(self, solution):
        return solution.personal_best.fitness_value < self.best_solution.fitness_value

    def check_state_of_particle(self, solution):
        if self.is_better_then_personal_best(solution):
            solution.personal_best = copy.deepcopy(solution)
            if self.is_better_then_global_best(solution):
                self.best_solution = solution.personal_best

    def start(self, Function):
        super().start()
        swarm = self.generate_population(Function)
        self.evalute_population(swarm, Function)

        self.best_solution = self.select_best_solution(swarm)
        self.generate_velocity_vectors_for_paricles(swarm)

        while self.index_of_generation < self.max_generation:
            if self.graph:
                self.graph.draw(self.best_solution, swarm)
            for particle in swarm:
                self.calculate_new_velocity(particle)
                self.calculate_new_position(particle)
                self.evaluate(particle, Function)
                self.check_state_of_particle(particle)

            self.index_of_generation += 1

        self.close_plot()
