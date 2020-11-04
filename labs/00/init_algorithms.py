from algorithms.Blind import BlindAgorithm
from algorithms.HillClimb import HillClimbAlgorithm
from algorithms.SimulatedAnnealing import SimulatedAnnealingAlgorithm
from algorithms.GeneticTSP import GeneticAlgorithmTSP
from algorithms.DifferentialEvolution import DifferentialEvolutionAlgorithm
from algorithms.ParticleSwarmOptimization import ParticleSwarmOptimizationAlgorithm
from algorithms.SelfOrganizingMigrationAlgorithm import SelfOrganizingMigrationAlgorithm

algs = {
    "Blind": BlindAgorithm(),  # * cv1
    "HillClimb": HillClimbAlgorithm(),  # * cv2
    "SimulatedAnnealing": SimulatedAnnealingAlgorithm(),  # * cv3
    "GeneticAlgorithmTSP": GeneticAlgorithmTSP(),  # * cv4
    "DifferentialEvolution": DifferentialEvolutionAlgorithm(),  # * cv5
    "ParticleSwarmOptimization": ParticleSwarmOptimizationAlgorithm(),  # * cv6
    "SelfOrganizingMigration": SelfOrganizingMigrationAlgorithm() # * cv7 
}
