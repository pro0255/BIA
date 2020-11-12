
from algorithms.GeneticTSP import GeneticAlgorithmTSP 
import numpy as np
class AntColonyOptimizationAlgorithm(GeneticAlgorithmTSP):
    def __init__(self, importance_pheromone=1, importance_distance=1, **kwds):
        self.importance_pheromone = importance_pheromone
        self.importance_distance = importance_distance
        super().__init__(**kwds)
        delattr(self, "size_of_population") # ants = number of cities
        
 
    def prob_node_to_node(self):
        #TODO!: update p
        print('update_pheromones')

    def create_init_pheromone_matrix(self):
        return np.ones(shape=(self.number_of_cities, self.number_of_cities))

    def create_inverse_distance_matrix(self):
        print('inverse distance matrix')


    def update_pheromone(self, colony):
        #TODO!: update p
        print('update_pheromones')

    def build_distance_matrix(self, cities):
        distance_matrix = np.zeros(shape=((len(cities), len(cities))))
        for i in range(distance_matrix.shape[0]):
            for j in range(distance_matrix.shape[1]):
                if i == j:
                    continue
                start = cities[i]
                end = cities[j]
                distance_matrix[i][j] = np.linalg.norm(start - end)
        return distance_matrix

    def build_inverse_distance_matrix(self, distance_matrix):
        return np.reciprocal(np.copy(distance_matrix))
 
    def start(self, EucladianDistance):
        self.size_of_population = self.number_of_cities # :()
        self.distance_matrix = self.build_distance_matrix(self.cities)
        self.inverse_distance_matrix = self.build_inverse_distance_matrix(self.distance_matrix)
        exit()
        colony = self.generate_population(self.cities)
        print(self.create_init_pheromone_matrix())
        self.create_inverse_distance_matrix()
        
        print(self.cities)

        exit()
        while self.index_of_generation < self.max_generation:
            for k, ant in enumerate(pop):
                print(k)

            print(self.index_of_generation)
            self.update_pheromone(colony)
            self.index_of_generation += 1






"""
    Popis:
        Mravenční kolonie:
            Tento algoritmus vychází z mravenců.
            

"""