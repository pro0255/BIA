
from algorithms.GeneticTSP import GeneticAlgorithmTSP 

class AntColonyOptimizationAlgorithm(GeneticAlgorithmTSP):
    def __init__(self, **kwds):
        super().__init__(**kwds)

    def generate_population(self, Function):
        pass

    def generate_individual(self, Function):
        pass

    def start(self, EucladianDistance):
        print('info')