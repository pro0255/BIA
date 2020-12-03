from algorithms.Blind import BlindAgorithm
from algorithms.HillClimb import HillClimbAlgorithm
from algorithms.SimulatedAnnealing import SimulatedAnnealingAlgorithm
from algorithms.GeneticTSP import GeneticAlgorithmTSP
from algorithms.DifferentialEvolution import DifferentialEvolutionAlgorithm
from algorithms.ParticleSwarmOptimization import ParticleSwarmOptimizationAlgorithm
from algorithms.SelfOrganizingMigrationAlgorithm import SelfOrganizingMigrationAlgorithm
from algorithms.AntColonyOptimization import AntColonyOptimizationAlgorithm
from algorithms.FireflyAlgorithm import FireflyAlgorithm
from algorithms.TeachingLearningBasedOptimization import TeachingLearningBasedAlgorithm
from algorithms.NonDominatedSortingGeneticAlgorithm import NonDominatedGeneticAlgorithm

algs = {
    "Blind": BlindAgorithm(),  # * cv1
    "HillClimb": HillClimbAlgorithm(),  # * cv2
    "SimulatedAnnealing": SimulatedAnnealingAlgorithm(),  # * cv3
    "GeneticAlgorithmTSP": GeneticAlgorithmTSP(),  # * cv4
    "DifferentialEvolution": DifferentialEvolutionAlgorithm(),  # * cv5
    "ParticleSwarmOptimization": ParticleSwarmOptimizationAlgorithm(),  # * cv6
    "SelfOrganizingMigration": SelfOrganizingMigrationAlgorithm(),  # * cv7
    "AntColonyOptimization": AntColonyOptimizationAlgorithm(),  # * cv8
    "FireflyAlgorithm": FireflyAlgorithm(),  # * cv9,
    "TeachingLearningBased": TeachingLearningBasedAlgorithm(),  # * cv10
    "NonDominatedGeneticAlgorithm": NonDominatedGeneticAlgorithm(),  # * cv11
}

algorithms_functions_blacklist = [
    GeneticAlgorithmTSP.__name__,
    AntColonyOptimizationAlgorithm.__name__,
    NonDominatedGeneticAlgorithm.__name__,
]
