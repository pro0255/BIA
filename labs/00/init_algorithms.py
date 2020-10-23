import algorithms.Algorithms as ALG


algs = {
    "Blind": ALG.BlindAgorithm(),  # * cv1
    "HillClimb": ALG.HillClimbAlgorithm(),  # * cv2
    "SimulatedAnnealing": ALG.SimulatedAnnealingAlgorithm(),  # * cv3
    "GeneticAlgorithmTSP": ALG.GeneticAlgorithmTSP(),  # * cv4
    "DifferentialEvolution": ALG.DifferentialEvolutionAlgorithm(),  # * cv5
    "ParticleSwarmOptimization": ALG.ParticleSwarmOptimizationAlgorithm(),  # * cv6
}
