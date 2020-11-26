from functions.Sphere import Sphere
from init_functions import functions
from algorithms.DifferentialEvolution import DifferentialEvolutionAlgorithm
from algorithms.ParticleSwarmOptimization import ParticleSwarmOptimizationAlgorithm
from algorithms.SelfOrganizingMigrationAlgorithm import SelfOrganizingMigrationAlgorithm
from algorithms.FireflyAlgorithm import FireflyAlgorithm
from algorithms.TeachingLearningBasedOptimization import TeachingLearningBasedAlgorithm

"""Comparasion of implemented algorithms [DE, PSO, SOMA, FA, TLBO]
    Run experiment for every objective function ala test function.
    Saved in excel.
    In excel calculated mean.
    Minimal is 30 experiments.
"""

D = 30 #number of dimensions
NP = 30 #size of populaiton
Max_OFE = 100 #maximal number of objectiive function evaluations #TODO!: HERE 3000 
NUMBER_OF_EXPERIMENTS = 5 #number of experiments was specified as constant value 30 #TODO!: HERE 30
FUNCTION_TO_RUN = functions.values()
ALGORITHMS_TO_RUN = [DifferentialEvolutionAlgorithm(), ParticleSwarmOptimizationAlgorithm(), FireflyAlgorithm(), SelfOrganizingMigrationAlgorithm(), TeachingLearningBasedAlgorithm()]

