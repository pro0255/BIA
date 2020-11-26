from functions.Sphere import Sphere

"""Comparasion of implemented algorithms [DE, PSO, SOMA, FA, TLBO]
    Run experiment for every objective function ala test function.
    Saved in excel.
    In excel calculated mean.
    Minimal is 30 experiments.
"""

D = 30 #number of dimensions
NP = 30 #size of populaiton
Max_OFE = 100 #maximal number of objectiive function evaluations #TODO!: HERE 3000 
NUMBER_OF_EXPERIMENTS = 30 #number of experiments was specified as constant value 30
FUNCTION_TO_RUN = Sphere()

