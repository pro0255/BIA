import matplotlib.pyplot as plt
from matplotlib import cm
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
from Application import Application
import math
from tkinter import *

SIZE_OF_GENERATION_GLOBAL = 10
NUMBER_OF_INTERATIONS_GLOBAL = 100 



def draw_fig(Func):
    x = np.linspace(Func.left, Func.right, 30)
    y = np.linspace(Func.left, Func.right, 30)
    X, Y = np.meshgrid(x, y)
    Z = run_func(X, Y, Func)

    ax = plt.axes(projection="3d", title=type(Func).__name__)
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, alpha=0.4)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    return ax


def run_func(X, Y, Func):
    flat_X = X.reshape(X.shape[0] * X.shape[1], -1)
    flat_Y = Y.reshape(Y.shape[0] * Y.shape[1], -1)
    flat_Z = []
    for i in range(len(flat_X)):
        z = Func.run([flat_X[i][0], flat_Y[i][0]])
        flat_Z.append(z)

    numpyArray = np.array(flat_Z)
    return numpyArray.reshape(X.shape[0], -1)




def draw_alg_iteration_MIN(min_vector, ax):
    return ax.scatter(
            min_vector[0],
            min_vector[1],
            min_vector[2],
            s=10,
            alpha=1,
            c="red",
            marker="^",
    )


def draw_generation(generation, ax):
    return ax.scatter(
        generation[0],
        generation[1],
        generation[2],
        s=2,
        alpha=1,
        c="green",
        marker="o",
    )


def run_blind_in_iterations(ax, Func,size_of_generation = SIZE_OF_GENERATION_GLOBAL, number_of_iterations = NUMBER_OF_INTERATIONS_GLOBAL):
    blind_alg = BlindAgorithm()
    min_vector = None
    iteration_state = None
    generation_state = None
    for i in range(number_of_iterations):
        if iteration_state:
            iteration_state.remove()
        [min_vector, all_points_generation] = blind_alg.run(
            size_of_generation, Func, min_vector
        )
        iteration_state = draw_alg_iteration_MIN(min_vector, ax)
        generation_state = draw_generation(all_points_generation, ax)

        plt.pause(0.07)
        plt.draw()

        if generation_state:
            generation_state.remove()


app = Application()


def run():
    try:
        size_generation = 0
        size_generation = int(app.size_generation.get().strip())
        number_of_iterations = int(app.number_of_iterations.get().strip())
        ax = draw_fig(app.selected_function)
        run_blind_in_iterations(ax, app.selected_function, size_generation, number_of_iterations)
    except:
        print('Cannot start animation - args are not as expected')




run_button = Button(app.root, text="START ANIMATION", bg='brown', fg='white', font=('helvetica', 9, 'bold'), command=run)
run_button.pack()

app.start()
