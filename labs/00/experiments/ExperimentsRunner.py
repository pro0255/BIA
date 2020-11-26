from experiments import EXPERIMENT_CONSTANTS
from algorithms.DifferentialEvolution import DifferentialEvolutionAlgorithm
from algorithms.ParticleSwarmOptimization import ParticleSwarmOptimizationAlgorithm
from algorithms.SelfOrganizingMigrationAlgorithm import SelfOrganizingMigrationAlgorithm
from algorithms.FireflyAlgorithm import FireflyAlgorithm
from algorithms.TeachingLearningBasedOptimization import TeachingLearningBasedAlgorithm
from Graph import Graph


#TODO!: dimension check
#TODO!: return best_solution and description
#TODO!: save to excel#

 

#DE, PSO, SOMA, FA, TLBO

class ExperimentsRunner():
    """Class which takes care of running experiments with specified parameters.
    """
    def __init__(self, D=EXPERIMENT_CONSTANTS.D, NP=EXPERIMENT_CONSTANTS.NP, MAX_G=EXPERIMENT_CONSTANTS.Max_OFE, NUMBER_OF_EXPERIMENTS=EXPERIMENT_CONSTANTS.NUMBER_OF_EXPERIMENTS, Function=EXPERIMENT_CONSTANTS.FUNCTION_TO_RUN):
        self.D = D
        self.NP = NP
        self.MAX_G = MAX_G
        self.N_O_G = NUMBER_OF_EXPERIMENTS
        self.oF = Function


    def set_properties(self, algorithms):
        g = Graph(self.oF.left, self.oF.right, self.oF)

        for a in algorithms:
            a.size_of_population = self.NP
            a.max_generation = self.MAX_G
            a.graph = g

    def build(self):
        de = DifferentialEvolutionAlgorithm() #it is ok
        # pso = ParticleSwarmOptimizationAlgorithm() #it is ok
        # fa = FireflyAlgorithm() #it is ok
        # soma = SelfOrganizingMigrationAlgorithm() #it is ok
        # tlbo = TeachingLearningBasedAlgorithm()
        tmp = de

        algorithms = [tmp]
        self.set_properties(algorithms)
        return algorithms

        


    def start_experiments(self):
        print('Starting experiments')
        
        
        for algorithm in self.build():
            algorithm.start(self.oF)


