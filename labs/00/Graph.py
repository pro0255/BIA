import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns
import matplotlib.lines as mlines

"""
Classes which take care of vizualization

Graphs created for specific tasks [TSP{2d vizualization}, Other{3d vizualization}]
"""


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

        self.plot = ax
        self.heat_map = self.fig.add_subplot(122, title="Heat Map")
        self.heat_map.pcolormesh(X, Y, Z, shading="nearest")
        self.save = None

    def create_arrays(self, population):
        X = []
        Y = []
        Z = []
        for solution in population:
            X.append(solution.vector[0])
            Y.append(solution.vector[1])
            Z.append(solution.fitness_value)
        return (X, Y, Z)

    def scatter_population(self, values, plot, c="blue"):
        return plot.scatter(
            *values,
            s=5,
            alpha=1,
            c=c,
            marker="o",
        )

    def draw_best_solution(self, args, plot, c="red"):
        return plot.scatter(
            *args,
            s=40,
            alpha=1,
            c=c,
            marker="o",
        )

    def draw_extra_population(self, best, population):
        b_c = "yellow"
        p_c = "green"
        plots = self.common_draw(best, population, b_c, p_c)
        self.common_lib_middeware_draw()
        self.common_remove(plots)

    def common_lib_middeware_draw(self):
        plt.draw()
        plt.pause(0.2)

    def common_remove(self, plots):
        if plots:
            for plot in plots:
                if plot:
                    plot.remove()

    def common_draw(self, best_solution, population, b_c="red", p_c="blue"):
        best_3d = self.draw_best_solution(
            (
                best_solution.vector[0],
                best_solution.vector[1],
                best_solution.fitness_value,
            ),
            self.plot,
            b_c,
        )
        best_heatmap = self.draw_best_solution(
            (best_solution.vector[0], best_solution.vector[1]), self.heat_map, b_c
        )

        pop_3d = None
        pop_heatmap = None

        if population:
            values = self.create_arrays(population)
            pop_3d = self.scatter_population(values, self.plot, p_c)
            X, Y, Z = values
            pop_heatmap = self.scatter_population((X, Y), self.heat_map, p_c)

        return (best_3d, best_heatmap, pop_3d, pop_heatmap)

    def draw(self, best_solution, population=None):
        self.common_remove(self.save)
        plots = self.common_draw(best_solution, population)
        self.save = plots[0:2]
        self.common_lib_middeware_draw()
        self.common_remove(plots[2:])


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

    def draw_connections(self, cities, c):
        length = len(cities)
        for i in range(length):
            current = cities[i]
            next = cities[(i + 1) % length]
            self.plot.plot([current[0], next[0]], [current[1], next[1]], c, linewidth=2)

    def draw(self, best_solution, c="r"):
        self.plot.clear()
        plt.title(f"Traveling salesman problem {best_solution.fitness_value}")
        cities = best_solution.vector
        self.draw_cities(cities)
        self.draw_connections(cities, c)
        plt.draw()
        plt.pause(0.02)
