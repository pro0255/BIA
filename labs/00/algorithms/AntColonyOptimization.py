
from algorithms.GeneticTSP import GeneticAlgorithmTSP 
import numpy as np
from solution.Solution import Solution

class AntColonyOptimizationAlgorithm(GeneticAlgorithmTSP):
    def __init__(self, importance_pheromone=1, importance_distance=1, **kwds):
        self.importance_pheromone = importance_pheromone
        self.importance_distance = importance_distance
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
        individual = np.arange(0, len(cities))
        del_index = np.delete(individual, [self.start_index])
        np.random.shuffle(del_index)
        individual = Solution()
        individual.vector = np.copy(cities)
        individual.trajectory = np.insert(del_index, 0, self.start_index)
        self.update_individual(individual)
        return individual

    def update_pheromone(self, colony):
        #TODO!: update p
        print('update_pheromones')

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
 

    def calc_possibility(self, s, vis_matrix):
        pheromone_row = np.power(self.pheromone_matrix[s], self.importance_pheromone)
        distance_row = np.power(vis_matrix[s], self.importance_distance)
        possibility = pheromone_row * distance_row
        sum 

        print(possibility)
        print(pheromone_row)
        print(distance_row)
        exit()

    def ant_step(self, s, vis_matrix):
        self.calc_possibility(s, vis_matrix)

    def ant_move(self, ant):
        vis_matrix = np.copy(self.inverse_distance_matrix)
        for v in ant.trajectory:
            self.ant_step(v, vis_matrix)


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
                exit()
            print(self.index_of_generation)
            self.update_pheromone(colony)
            self.index_of_generation += 1






"""
    Popis:
        Mravenční kolonie:
            Tento algoritmus vychází z mravenců.
            

"""