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
from blind.Blind import BlindAgorithm
import math


def draw_fig(Func):
    x = np.linspace(Func.left, Func.right, 30)
    y = np.linspace(Func.left, Func.right, 30)
    X, Y = np.meshgrid(x, y)
    Z = run_func(X, Y, Func)

    ax = plt.axes(projection="3d")
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap="viridis", edgecolor="none", alpha=0.1)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    return ax


def run_func(X, Y, Func):
    flat_X = X.reshape(X.shape[0] * X.shape[1], -1)
    flat_Y = Y.reshape(Y.shape[0] * Y.shape[1], -1)
    flat_Z = []
    for i in range(len(flat_X)):
        # here method
        z = Func.run([flat_X[i][0], flat_Y[i][0]])
        flat_Z.append(z)

    numpyArray = np.array(flat_Z)
    return numpyArray.reshape(X.shape[0], -1)


sphere = Sphere()
schwefel = Schwefel()
rosenbrock = Rosenbrock()
rastrigin = Rastrigin()
griewangk = Griewangk()
levy = Levy()
michalewicz = Michalewicz()
zakharov = Zakharov()
ackley = Ackley()
##



function_global = michalewicz
number_of_records_global = 3
number_of_iterations_global = 100


def run_blind_in_iterations(number_of_iterations, ax):
    blind_alg = BlindAgorithm()
    min_vector = None
    lst_point = None
    for i in range(number_of_iterations):
        if lst_point != None:
            lst_point.remove()
        min_vector = blind_alg.run(number_of_records_global, function_global, min_vector)
        lst_point = ax.scatter(min_vector[0], min_vector[1], min_vector[2], s=40, alpha=1, c='red', marker='o')
        print(f'Drawing min in generation number -> {i}')
        plt.draw() 
        plt.pause(0.08) #is necessary for the plot to update for some reason






ax = draw_fig(function_global)
run_blind_in_iterations(number_of_iterations_global, ax)




# plt.show()







