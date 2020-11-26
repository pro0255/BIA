from algorithms.AbstractGenetic import AbstractGeneticAlgorithm
import numpy as np
import copy
from solution.Solution import Solution


class ParticleSwarmOptimizationAlgorithm(AbstractGeneticAlgorithm):
    def __init__(self, c1=2, c2=2, v_min=-1, v_max=1, **kwds):
        """pop_size = size_of_population [number of individuals]
        M_max = max_generation [number of migration cycles]
        c_1, c_2 = new parametr, [learning constants]
        v_mini, v_maxi = new parametr, [minimal and maximal velocity]

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
        """Creates random uniform velocity vector for particle.
            This method is used only in the beginning of algorithm. We can call it init velocity vector.
        Args:
            solution (Solution): Individual (particle).
        """
        solution.velocity_vector = np.random.uniform(
            low=self.v_min, high=self.v_max, size=solution.dimension
        )

    def generate_velocity_vectors_for_particles(self, swarm):
        """Using generate_velocity_vector to create velocity vector for every particle from swarm.
            This method is used only in the beginning of algorithm. It helps to generate first generation (swarm), where every particle has random values affected by algorithm parameters like v_max, v_min..
        Args:
            swarm (Solution[]): Vector populated with solutions (particles).
        """
        [self.generate_velocity_vector(individual) for individual in swarm]

    def generate_population(self, Function):
        """Generates population according to Function with help of method generate_individual.
        Args:
            Function (Function): One of the cost function. (Sphere, Ackley..)
        Returns:
            [Solution[]]: Returns whole population with particles.
        """
        return [
            self.generate_individual(Function) for i in range(self.size_of_population)
        ]

    def generate_individual(self, Function):
        """Method calculates in the beginning of alg individual. Also sets personal_best copy of generated (self).
        Args:
            Function (Function): One of the cost function. (Sphere, Ackley..)
        Returns:
            [Solution]: Returns individual from population. In PSO it is called particle.
        """
        solution = self.generate_random_solution(Function.left, Function.right)
        solution.personal_best = copy.deepcopy(solution)
        return solution

    def calculate_new_velocity(self, solution):
        """Calculated velocity vector moves individual according to 3 directions:
            -> Current
            -> My best
            -> Global best
        Args:
            solution (Solution): Individual (particle).
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
        """cze - [Setrvacnost]
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
        """Returns boolean according to condition
        Args:
            solution (Solution): Individual from population.
        Returns:
            boolean: Comparison of personal best and current solution.
        """
        return (
            solution.personal_best is None
            or solution.fitness_value < solution.personal_best.fitness_value
        )

    def is_better_then_global_best(self, solution):
        """Returns boolean according to condition
        Args:
            solution (Solution): Individual from population.
        Returns:
            boolean: Comparison of personal best from individual and global best individual.
        """
        return solution.personal_best.fitness_value < self.best_solution.fitness_value

    def check_state_of_particle(self, solution):
        """In the iteration every particle going to change state. Method take care of correct change. If current individual vector (solution) is better then his personal, then going to save (copy) this state of individual to property personal_best.

        Args:
            solution (Solution): Actual individual from population.
        """
        if self.is_better_then_personal_best(solution):
            solution.personal_best = copy.deepcopy(solution)
            if self.is_better_then_global_best(solution):
                self.best_solution = solution.personal_best

    def start(self, Function):
        """Runs DifferentialEvolution Algorithm on specified Function, with specified args.
        Args:
            Function (class Function): specific Function (Sphere || Ackley..)
        """
        super().start()
        swarm = self.generate_population(Function)
        self.evalute_population(swarm, Function)

        self.best_solution = self.select_best_solution(swarm)
        self.generate_velocity_vectors_for_particles(swarm)

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
