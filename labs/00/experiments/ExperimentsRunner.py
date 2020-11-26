from experiments import EXPERIMENT_CONSTANTS
from algorithms.DifferentialEvolution import DifferentialEvolutionAlgorithm
from algorithms.ParticleSwarmOptimization import ParticleSwarmOptimizationAlgorithm
from algorithms.SelfOrganizingMigrationAlgorithm import SelfOrganizingMigrationAlgorithm
from algorithms.FireflyAlgorithm import FireflyAlgorithm
from algorithms.TeachingLearningBasedOptimization import TeachingLearningBasedAlgorithm
from Graph import Graph
from experiments.DELIMITER import DELIMITER


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
        # g = Graph(self.oF.left, self.oF.right, self.oF)
        for a in algorithms:
            a.size_of_population = self.NP
            a.max_generation = self.MAX_G
            a.D = self.D
            # a.graph = g

    def build(self):
        de = DifferentialEvolutionAlgorithm() #it is ok
        pso = ParticleSwarmOptimizationAlgorithm() #it is ok
        fa = FireflyAlgorithm() #it is ok
        soma = SelfOrganizingMigrationAlgorithm() #it is ok
        tlbo = TeachingLearningBasedAlgorithm()
        tmp = tlbo
        algorithms = [tmp]
        self.set_properties(algorithms)
        return algorithms

    def start_experiments(self):
        read_me = ""
        csv = ""
        for i in range(self.N_O_G):
            fV, desription = self.start_experiment()
            if not i:
                read_me = DELIMITER.join(desription)
            csv += f'Experiment {i}{DELIMITER}{DELIMITER.join([str(f) for f in fV])}'

    def start_experiment(self):
        description_algorithms = []
        fV_algoritms = []
        for algorithm in self.build():
            fV, description = algorithm.start(self.oF)
            description_algorithms.append(description)
            fV_algoritms.append(fV)
        return (fV_algoritms, description_algorithms)


    def save_experiment(self, path):
        pass
        



