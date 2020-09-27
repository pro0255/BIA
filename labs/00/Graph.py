import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

class Graph():
    def __init__(self, start, stop, Function):
        x = np.linspace(start, stop, 30)
        y = np.linspace(start, stop, 30)
        X, Y = np.meshgrid(x, y)

        flat_X = X.reshape(X.shape[0] * X.shape[1], -1)
        flat_Y = Y.reshape(Y.shape[0] * Y.shape[1], -1)
        flat_Z = []
        for i in range(len(flat_X)):
            z = Function.run(np.array([flat_X[i][0], flat_Y[i][0]]))
            flat_Z.append(z)

        numpyArray = np.array(flat_Z)
        Z = numpyArray.reshape(X.shape[0], -1)

        varidis = cm.get_cmap('viridis', 12)
        ax = plt.axes(projection="3d", title=type(Function).__name__)
        ax.plot_surface(X, Y, Z, cmap=varidis,rstride=1, cstride=1, linewidth=0, alpha=0.1, antialiased=False)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")

        self.best = None
        self.population = None

        self.plot = ax

    def draw_population(self, population):
        X = []
        Y = []
        Z = []

        for solution in population:
            X.append(solution.vector[0])
            Y.append(solution.vector[1])
            Z.append(solution.fitness_value)

        self.population = self.plot.scatter(
            X,
            Y,
            Z,
            s=5,
            alpha=1,
            c="blue",
            marker="o",
        )

        plt.pause(0.1)
        plt.draw()

        if self.population:
            self.population.remove()



    def draw(self, best_solution, population = None):

        if self.best:
            self.best.remove()



        self.best = self.plot.scatter(
            best_solution.vector[0],
            best_solution.vector[1],
            best_solution.fitness_value,
            s=40,
            alpha=1,
            c="red",
            marker="o",
        )

        plt.pause(0.1)
        plt.draw()

        if population:
            self.draw_population(population)
