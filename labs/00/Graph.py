import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns
import matplotlib.lines as mlines


class AbstractGraph:
    def __init__(self):
        self.fig = plt.figure(
            num="Bia vizualization",
            figsize=(20, 10),
            dpi=80,
            facecolor="w",
            edgecolor="k",
        )


class Graph(AbstractGraph):
    def __init__(self, start, stop, Function):
        super().__init__()
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

        cmap = cm.get_cmap("jet", 12)
        ax = self.fig.add_subplot(121, projection="3d", title=type(Function).__name__)
        ax.plot_surface(
            X,
            Y,
            Z,
            cmap=cmap,
            rstride=1,
            cstride=1,
            linewidth=0,
            alpha=0.1,
            antialiased=False,
        )
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")

        self.best = None
        self.population = None
        ##TODO!: refactor to better solution
        self.best_heatmap = None

        self.plot = ax

        self.heat_map = self.fig.add_subplot(122, title="Heat Map")
        self.heat_map.pcolormesh(X, Y, Z, shading="nearest")

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

        plt.pause(0.5)
        plt.draw()

        if self.population:
            self.population.remove()

    def draw(self, best_solution, population=None):
        if self.best:
            self.best.remove()

        if self.best_heatmap:
            self.best_heatmap.remove()

        self.best = self.plot.scatter(
            best_solution.vector[0],
            best_solution.vector[1],
            best_solution.fitness_value,
            s=40,
            alpha=1,
            c="orangered",
            marker="o",
        )

        self.best_heatmap = self.heat_map.scatter(
            best_solution.vector[0],
            best_solution.vector[1],
            s=20,
            alpha=1,
            c="orangered",
            marker="o",
        )

        if population:
            self.draw_population(population)


class TSPGraph(AbstractGraph):
    def __init__(self, low, high):
        super().__init__()
        self.plot = self.fig.add_subplot(111, title="Traveling salesman problem")

    def draw_cities(self, cities):
        for index, city in enumerate(cities):
            x = city[0]
            y = city[1]

            if index == 0:
                self.plot.plot(x, y, "bo", markersize=20)
            else:
                self.plot.plot(x, y, "go-", markersize=15)
            self.plot.text(x, y, s=index, fontsize=30)

    def draw_connections(self, cities):
        length = len(cities)
        for i in range(length):
            current = cities[i]
            next = cities[(i + 1) % length]
            self.plot.plot(
                [current[0], next[0]], [current[1], next[1]], "r", linewidth=2
            )

    def draw(self, best_solution):
        self.plot.clear()
        plt.title(f"Traveling salesman problem {best_solution.fitness_value}")
        cities = best_solution.vector
        self.draw_cities(cities)
        self.draw_connections(cities)
        plt.draw()
        plt.pause(0.05)
