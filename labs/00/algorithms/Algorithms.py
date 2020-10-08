import random
import numpy as np
import matplotlib.pyplot as plt
import time
import traceback

class Solution:
    def __init__(self, dimension=2, lower_bound=0, upper_bound=0, key=0):
        self.dimension = dimension
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.vector = np.zeros(dimension)  # x,y..
        self.fitness_value = np.inf  # z..
        self.key = Solution.key
        Solution.key += 1
    
    key = 0


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
        if self.graph:
            time.sleep(0.5)
            plt.close('all')


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
                ##TODO?: random with bound or without?
                # r = np.random.uniform(Function.left, Function.right)
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




#TODO!: make abstract genetic algorithm, mutate etc..
class GeneticAlgorithmTSP(AbstractAlgorithm):
    def __init__(self, number_of_cities=20, low =0, high=200, **kwds):
        """
            NP = size of population
            G = max_generation

        Args:
            number_of_cities (int): D, it will be a number of cities
        """
        super().__init__(**kwds)
        self.number_of_cities = number_of_cities
        self.low =low
        self.high=high
        self.generate_cities()

    def generate_cities(self):
        self.cities = np.random.uniform(size=(self.number_of_cities, 2), low=self.low,high=self.high)

    def generate_individual(self, cities):
        """Generating single individual according to input
        Shuffle cities

        Returns:
            []: [description]
        """
        individual = Solution()
        individual.vector = np.array(random.sample(list(self.cities), len(self.cities)))
        return individual
        
    def generate_population(self, cities):
        """Generating NP random individuals
        """
        population = [self.generate_individual(cities) for _ in range(self.size_of_population)]
        return population

    def copy(self, population):
        return population.copy()

    def crossover(self, parent_A, parent_B):
        half_A = int((len(parent_A.vector)/2))+1
        part_A = parent_A.vector[0:half_A, :]
        # full_size_B = int(len(parent_B.vector))
        # part_B = parent_B.vector[half_A:full_size_B, :]

        rest = []
        for city in parent_B.vector:
            is_there = np.any(part_A == city)
            if not is_there:
                rest.append(list(city))

        crossover_vector = np.concatenate((part_A, np.array(rest)), axis=0) 
        offspring_AB = Solution()
        offspring_AB.vector = crossover_vector
        return offspring_AB
    



    def mutate(self, offspring_AB):
        first_index = int(np.random.uniform(0, len(offspring_AB.vector)))
        second_index = int(np.random.uniform(0, len(offspring_AB.vector)))
        if first_index != second_index:
            offspring_AB.vector[[first_index, second_index], :] = offspring_AB.vector[[second_index, first_index] , :] 
            return offspring_AB
        else:
            return self.mutate(offspring_AB)

    def get_individual(self, population, parent_A):
        selected = self.select_random_individual(population, parent_A)
        if selected.key != parent_A.key:
            return selected
        return self.get_individual(population, parent_A)




    def start(self):
        self.generate_cities()
        ed = EucladianDistance()
        population = self.generate_population(self.cities)
        self.evalute_population(population, ed)
        new_population = self.copy(population)
        for _ in range(self.max_generation): #how many times will i try
            self.best_solution = self.select_best_solution(population)
            if self.graph:
                self.graph.draw(self.best_solution)
            for j in range(len(population)): #try to get new one in new generation for every individual
                parent_A = population[j] ##is here j or i?
                parent_B = self.get_individual(population, parent_A) #here is drop down cause he is trying to find 10 uin len 10..
                try: 
                    offspring_AB = self.crossover(parent_A, parent_B)
                    offspring_AB = self.mutate(offspring_AB)                    
                    self.evaluate(offspring_AB, ed)
                

                    if offspring_AB.fitness_value < parent_A.fitness_value: ##if is better then his parent
                        new_population[j] = offspring_AB ##is here j or i?

                except Exception as error:
                    print(f'something wrong {error}')
                    print(traceback.print_exc())
                    continue            

            population = new_population


    

class EucladianDistance():
    def __init__(self):
        pass

    def run(self, vector):
        distance = 0
        rows = len(vector)
        for i in range(rows):
            current_index = i
            next_index = ((i + 1) % rows)

            current_vector = vector[current_index]
            next_vector = vector[next_index]

            dist = np.linalg.norm(next_vector - current_vector)
            distance += dist

        return distance