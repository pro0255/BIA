
from algorithms.GeneticTSP import GeneticAlgorithmTSP 
import numpy as np
from solution.Solution import Solution

class AntColonyOptimizationAlgorithm(GeneticAlgorithmTSP):
    def __init__(self, importance_pheromone=1, importance_distance=1, vaporization=.5, **kwds):
        self.importance_pheromone = importance_pheromone
        self.importance_distance = importance_distance
        self.vaporization = vaporization
        super().__init__(**kwds)
        delattr(self, "size_of_population") # ants = number of cities
        self.start_index = 0
 
    def prob_node_to_node(self):
        #TODO!: update p
        print('update_pheromones')

    def create_init_pheromone_matrix(self):
        return np.ones(shape=(self.number_of_cities, self.number_of_cities))

    def update_individual(self, individual):
        individual.vector = individual.vector[individual.trajectory]

    def generate_population(self, cities):
        return np.array([self.generate_individual(cities) for _ in range(self.number_of_cities)])

    def generate_individual(self, cities):
        individual = Solution()
        individual.vector = np.copy(cities)
        return individual


    def create_value(self, fV, Q=1):
        if fV != 0:
            return Q/fV
        else:
            return fV

    def generate_edge_dic(self, colony):
        dic = {}
        for ant in colony:
            edges = [(ant.trajectory[i], ant.trajectory[(i+1)%len(ant.trajectory)]) for i in range(len(ant.trajectory))]
            for e in edges:
                value = self.create_value(ant.fitness_value)
                if e in dic:
                    dic[e].append(value)
                else:
                    dic[e] = [value]
        return dic


    def make_vaporization(self, e, dic):
        i, j = e
        perc = (1 - self.vaporization)
        dic_v = dic.get(e, 0)
        self.pheromone_matrix[i][j] = perc*self.pheromone_matrix[i][j] + dic_v if not dic_v else sum(dic_v)

    def update_pheromone(self, colony):
        dic = self.generate_edge_dic(colony)
        for i in range(self.pheromone_matrix.shape[0]):
            for j in range(self.pheromone_matrix.shape[1]):
                self.make_vaporization((i,j), dic)

    def create_distance_matrix(self, cities):
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
        r = np.reciprocal(np.copy(distance_matrix))
        for i in range(r.shape[0]):
            r[i][i] = 0
        return r
 

    def calc_cumulative_possibility(self, s, vis_matrix):
        pheromone_row = np.power(self.pheromone_matrix[s], self.importance_pheromone)
        distance_row = np.power(vis_matrix[s], self.importance_distance)
        possibility = pheromone_row * distance_row
        suma = np.sum(possibility)
        probabilities = possibility / suma
        cumulative = np.array([sum(probabilities[0:i+1]) for i in range(len(probabilities))])
        return cumulative

    def ant_step(self, s, vis_matrix):
        p_cum = self.calc_cumulative_possibility(s, vis_matrix)
        r = np.random.uniform()
        for i, p in enumerate(p_cum):
            if r < p:
                return i 

    def ant_move(self, ant):
        vis_matrix = np.copy(self.inverse_distance_matrix)
        trajectory = [self.start_index]
        vis_matrix[:, self.start_index] = 0
        for v in trajectory:
            index = self.ant_step(v, vis_matrix)
            trajectory.append(index)
            vis_matrix[:, index] = 0
            if not vis_matrix.any():
                break
        ant.trajectory = np.array(trajectory)
        self.update_individual(ant)

    def start(self, EucladianDistance):
        self.size_of_population = self.number_of_cities # :()
        self.generate_cities()
        self.distance_matrix = self.create_distance_matrix(self.cities)
        self.inverse_distance_matrix = self.create_inverse_distance_matrix(self.distance_matrix)
        self.pheromone_matrix = self.create_init_pheromone_matrix()
        colony = self.generate_population(self.cities)

        while self.index_of_generation < self.max_generation:
            for k, ant in enumerate(colony):
                self.ant_move(ant)
            self.evalute_population(colony, EucladianDistance)
            self.update_pheromone(colony)
            self.best_solution = self.select_best_solution(colony)
            if self.graph:
                self.graph.draw(self.best_solution)
            self.index_of_generation += 1

        if self.graph:
            self.graph.draw(self.best_solution, 'g')

        self.close_plot()
