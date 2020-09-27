import matplotlib.pyplot as plt
import numpy as np
from functions.Sphere import Sphere
from functions.Schwefel import Schwefel
from functions.Rosenbrock import Rosenbrock
from functions.Rastrigin import Rastrigin
from functions.Griewangk import Griewangk
from functions.Levy import Levy
from functions.Michalewicz import Michalewicz
from functions.Zakharov import Zakharov
from functions.Ackley import Ackley
from algorithms.Blind import BlindAgorithm
from algorithms.Blind import HillClimbAlgorithm
from Application import Application
import math
from tkinter import *
from Graph import Graph

def run_action():
    """
    Action binded to GUI button which starts Algorithm in selected Test function

    Firstly tries to get values from GUI inputs
    """
    try:
        size_of_population = 0
        size_of_population = int(app.size_generation.get().strip())
        max_generation = int(app.number_of_iterations.get().strip())
        active_function = app.selected_function
        graph = Graph(active_function.left, active_function.right, active_function)
        algorithm = BlindAgorithm(graph=graph, size_of_population=size_of_population, max_generation=max_generation)
        algorithm.start(active_function)

    except:
        app.stop()
        print("Cannot start animation - args are not as expected")



app = Application(run_action)
app.start()



