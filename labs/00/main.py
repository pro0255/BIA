from Application import Application
from experiments.ExperimentsRunner import ExperimentsRunner


"""
Starts GUI with selection of alg, function and hyperparameters.
"""
app = Application()
app.start(True)


"""
Class which start experiments and save them to file. It is possible to start it again with specified constants value. These are situated in experiments/EXPERIMENTS_CONSTANTS.py
"""
# exp = ExperimentsRunner()
# exp.start_experiments_for_functions()
