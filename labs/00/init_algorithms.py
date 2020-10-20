from algorithms.Algorithms import BlindAgorithm
from algorithms.Algorithms import HillClimbAlgorithm
from algorithms.Algorithms import SimulatedAnnealingAlgorithm
from algorithms.Algorithms import GeneticAlgorithmTSP
from algorithms.Algorithms import DifferentialEvolutionAlgorithm

algorithms = {
    "Blind": BlindAgorithm(),
    "HillClimb": HillClimbAlgorithm(),
    "SimulatedAnnealing": SimulatedAnnealingAlgorithm(),
    "GeneticAlgorithmTSP": GeneticAlgorithmTSP(),
    'DifferentialEvolution': DifferentialEvolutionAlgorithm()
}