from experiments import EXPERIMENT_CONSTANTS
from algorithms.DifferentialEvolution import DifferentialEvolutionAlgorithm
from algorithms.ParticleSwarmOptimization import ParticleSwarmOptimizationAlgorithm
from algorithms.SelfOrganizingMigrationAlgorithm import SelfOrganizingMigrationAlgorithm
from algorithms.FireflyAlgorithm import FireflyAlgorithm
from algorithms.TeachingLearningBasedOptimization import TeachingLearningBasedAlgorithm
from Graph import Graph
from experiments.DELIMITER import DELIMITER
from experiments.EXPERIMENTS_OUTPUT import EXPERIMENTS_PATH
import os
import time

#TODO: can save in same file? as other tab in excel? :D

SAVE = True

class ExperimentsRunner():
    """Class which takes care of running experiments with specified parameters.
    """
    def __init__(self, D=EXPERIMENT_CONSTANTS.D, NP=EXPERIMENT_CONSTANTS.NP, MAX_G=EXPERIMENT_CONSTANTS.Max_OFE, NUMBER_OF_EXPERIMENTS=EXPERIMENT_CONSTANTS.NUMBER_OF_EXPERIMENTS):
        self.D = D
        self.NP = NP
        self.MAX_G = MAX_G
        self.N_O_G = NUMBER_OF_EXPERIMENTS

    def set_properties(self, algorithms):
        for a in algorithms:
            a.size_of_population = self.NP
            a.max_generation = self.MAX_G
            a.D = self.D

    def build(self, algs = EXPERIMENT_CONSTANTS.ALGORITHMS_TO_RUN):
        self.set_properties(algs)
        return algs

    def start_experiments_for_functions(self, functions=EXPERIMENT_CONSTANTS.FUNCTION_TO_RUN):
        save_read_me = True
        start = time.time()
        print('Starting experiments for specified functions.')
        for f in functions:
            self.start_experiments(f, save_read_me)
            save_read_me = False
        print('Thanks for your time experiments finished :-].')
        end = time.time()
        how_many = str(end - start)
        self.save_experiment(f"Time to calculate {how_many}", "INFO", ".txt")
        

    def start_experiments(self, function, save_read_me):
        read_me = ""
        csv = ""
        FUNCTION_NAME = type(function).__name__
        print(f'Starting for objective function *{FUNCTION_NAME}* ')
        for i in range(self.N_O_G):
            transformed_index = i + 1 #lol
            fV, desription = self.start_experiment(function)
            if not i:
                read_me = DELIMITER.join(desription)
            csv += f'Experiment {transformed_index}{DELIMITER}{DELIMITER.join([str(f) for f in fV])}\n'
        if SAVE:
            self.save_experiment(csv, FUNCTION_NAME.lower())
            if save_read_me:
                self.save_experiment(read_me, 'README', '.txt')

    def start_experiment(self, function):
        description_algorithms = []
        fV_algoritms = []
        for algorithm in self.build():
            fV, description = algorithm.start(function)
            description_algorithms.append(description)
            fV_algoritms.append(fV)
        return (fV_algoritms, description_algorithms)


    def save_experiment(self, text, name, suffix='-experiments.csv', directory="experiments"):
        path = f'{EXPERIMENTS_PATH}'
        if not os.path.exists(path):
            os.makedirs(path)
        with open(f'{path}//{name}{suffix}', 'w') as f:
            f.write(text)

        



