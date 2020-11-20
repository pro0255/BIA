from algorithms.GeneticTSP import GeneticAlgorithmTSP
import numpy as np
from solution.Solution import Solution
import pandas as pd
import copy


class AntColonyOptimizationAlgorithm(GeneticAlgorithmTSP):
    def __init__(
        self, importance_pheromone=1, importance_distance=1, vaporization=0.5, **kwds
    ):
        self.importance_pheromone = importance_pheromone
        self.importance_distance = importance_distance
        self.vaporization = vaporization
        super().__init__(**kwds)
        delattr(self, "size_of_population")  # ants = number of cities
        self.start_index = 0 #if index then can every ant start from same city

    def create_init_pheromone_matrix(self):
        """Generates init pheromone matrix with values populated as 1.
        Returns:
            [float[][]]: Numpy arrary populated with ones.
        """
        return np.ones(shape=(self.number_of_cities, self.number_of_cities))

    def update_individual(self, individual):
        """Function order cities according to individual trajectory.
        Args:
            individual (Solution): Current individual to update.
        """
        individual.vector = individual.vector[individual.trajectory]


    def generate_population(self, cities):
        """Generates init inidviduals (ants).
        Args:
            cities (float[][]): Points in space.
        Returns:
            [Solution[]]: Generated population.
        """
        return np.array(
            [self.generate_individual(cities, i) for i in range(self.number_of_cities)]
        )

    def generate_individual(self, cities, i):
        """Generate individual. Where is actually only set cities as vector. During algorithm are these cities ordered by trajectory. Individual during alogrithn works with property trajectory. It is array of indicies and it is easy to make fast look up to cities.
        Args:
            cities (float[][]): Points in space.
        Returns:
            [Solution]: Generated solution.
        """
        individual = Solution()
        individual.vector = copy.deepcopy(cities)
        if self.start_index is not None:
            individual.trajectory = [self.start_index]
        else:
            individual.trajectory = [i if self.random else np.random.randint(0, len(cities))]
        return individual

    def create_value(self, fV, Q=1):
        """Create value with check of deviding with zero.
        Args:
            fV (float): Calculated fitness according to function.
            Q (int): Constant. Defaults to 1.
        Returns:
            [flaot]: Value which represents 1/(ant distance)
        """       
        return Q / fV

    def generate_edge_dic(self, colony):
        """Helper function to generate dictionary.
        Args:
            colony (Solution[]): Current ant colony.
        Returns:
            [dic<(int,int), float[]]: Dictionary populated with key as edges and values as Q/(fitness value)
        """
        dic = {}
        for ant in colony:
            edges = [
                (ant.trajectory[i], ant.trajectory[(i + 1) % len(ant.trajectory)])
                for i in range(len(ant.trajectory))
            ]
            for e in edges:
                value = self.create_value(ant.fitness_value)
                if e in dic:
                    dic[e].append(value)
                else:
                    dic[e] = [value]
        return dic

    def make_vaporization(self, e, dic):
        """Makes vaporization on edge.
        Args:
            e ((int, int)): Edge in graph.
            dic (dic<(int,int), float[]>):
        """
        i, j = e
        perc = 1 - self.vaporization
        dic_v = dic.get(e, 0)
        sum_update_value = dic_v if not dic_v else sum(dic_v)

        self.pheromone_matrix[i][j] = (
            perc * self.pheromone_matrix[i][j] + sum_update_value 
        )



    def update_pheromone(self, colony):
        """Updates pheromone matrix.
        Args:
            colony (Solution[]): Current ant colony.
        """
        dic = self.generate_edge_dic(colony)
        for i in range(self.pheromone_matrix.shape[0]):
            for j in range(self.pheromone_matrix.shape[1]):
                self.make_vaporization((i, j), dic)


    def create_distance_matrix(self, cities):
        """Creates init distance matrix.
        Args:
            cities (float[][]): Points in space.
        Returns:
            [float[][]]: Distance matrix.
        """
        distance_matrix = np.zeros(shape=((len(cities), len(cities))))
        for i in range(distance_matrix.shape[0]):
            for j in range(distance_matrix.shape[1]):
                if i == j:
                    continue
                start = cities[i]
                end = cities[j]
                distance_matrix[i][j] = np.linalg.norm(start - end)
        return distance_matrix

    def create_inverse_distance_matrix(self, distance_matrix):
        """1/distance matrix with check of reflexive points. inf -> 0.
        Args:
            distance_matrix (float[][]): Calculated distance matrix.
        Returns:
            [float[][]]: 1/(distance matrix)
        """
        r = np.reciprocal(copy.deepcopy(distance_matrix))
        for i in range(r.shape[0]):
            r[i][i] = 0
        return r

    def calc_cumulative_possibility(self, s, vis_matrix):
        """All important calculations in algorithm.
        Args:
            s (int): Current vertex.
            vis_matrix (float[][]): Visibility matrix.
        Returns:
            [float[]]: Cumulative probabilities populated array.
        """
        pheromone_row = np.power(self.pheromone_matrix[s], self.importance_pheromone)
        distance_row = np.power(vis_matrix[s], self.importance_distance)
        possibility = np.multiply(pheromone_row, distance_row)
        suma = np.sum(possibility)
        probabilities = np.divide(possibility, suma)
        cumulative = np.cumsum(probabilities)
        return cumulative

    def ant_step(self, s, vis_matrix):
        """Method finds index according to calculated cumulative probablities.
        Args:
            s (int): Current vertex.
            vis_matrix (float[][]): Visibility matrix.
        Returns:
            [int]: City to move.
        """
        p_cum = self.calc_cumulative_possibility(s, vis_matrix)
        r = np.random.uniform()
        return np.argmax(p_cum > r)


    def ant_move(self, ant, start_index, Function):
        """Method represents logic for ant move. Make step, update visibility matrix with column 0 until zero matrix.
        Args:
            ant (Solution): Current individual.
        """
        vis_matrix = copy.deepcopy(self.inverse_distance_matrix)
        trajectory = [start_index]
        vis_matrix[:, start_index] = 0
        for v in trajectory:
            index = self.ant_step(v, vis_matrix)
            trajectory.append(index)
            vis_matrix[:, index] = 0
            if not vis_matrix.any():
                break
        ant.trajectory = np.array(trajectory)
        self.update_individual(ant)
        self.evaluate(ant, Function)


    def construct_solution_according_to_pheromone_matrix(self, Function):
        sol = Solution()
        path = []
        print(pd.DataFrame(self.pheromone_matrix))
        for row in self.pheromone_matrix:
            max_index = np.argmax(row)
            path.append(max_index)
        print(path)
        sol.vector = copy.deepcopy(self.cities)
        sol.trajectory = np.array(path)
        sol.vector = sol.vector[sol.trajectory]
        self.evaluate(sol, Function)
        return sol

    def start(self, EucladianDistance):
        """Generates important variables.
            Moves colony, update trajectory for every ant, evaluates popultion, update pheromone according to evaluted fitness value of colony and draws graph with best solution.
        Args:
            EucladianDistance (Function): Fitness function.
        """
        self.index_of_generation = 0
        self.size_of_population = self.number_of_cities  # :()
        self.generate_cities()
        self.distance_matrix = self.create_distance_matrix(self.cities)

        self.inverse_distance_matrix = self.create_inverse_distance_matrix(
            self.distance_matrix
        )
        
        self.pheromone_matrix = self.create_init_pheromone_matrix()
        colony = self.generate_population(self.cities)

        while self.index_of_generation < self.max_generation:
            for k, ant in enumerate(colony):
                self.ant_move(ant, ant.trajectory[0], EucladianDistance)
            self.update_pheromone(colony)

            self.best_solution = self.select_best_solution(colony)
            if self.graph:
                self.graph.draw(self.construct_solution_according_to_pheromone_matrix(EucladianDistance))
            self.index_of_generation += 1

        if self.graph:
            self.graph.draw(self.best_solution, "g")

        self.close_plot()
