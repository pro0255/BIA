import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns
import matplotlib.lines as mlines
import pandas as pd

"""
Classes which take care of vizualization

Graphs created for specific tasks [TSP{2d vizualization}, Other{3d vizualization}]
"""
GLOBAL_PAUSE_TIME = 0.02


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
        self.delayed_remove = {}
        self.path = []

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

    def draw_with_vector(
        self, solution, old_solution, target=None, memorize_path=False, b_c="yellow"
    ):
        move = solution.vector - old_solution.vector
        self.path.append(
            self.heat_map.arrow(
                x=old_solution.vector[0],
                y=old_solution.vector[1],
                dx=move[0],
                dy=move[1],
                head_width=0.05,
                color=b_c,
            )
        )
        plots = self.common_draw(solution, None, b_c)
        if target is not None:
            plots_target = self.common_draw(target, None, "green")
        self.common_lib_middeware_draw()
        if not memorize_path:
            self.path[0].remove()
        self.common_remove(plots)
        if target is not None:
            self.common_remove(plots_target)

    def refresh_path(self):
        for arrow in self.path:
            try:
                arrow.remove()
            except:
                pass
        self.path = []

    def draw_extra_population(
        self, best, population=None, b_c="yellow", delayed_remove=None
    ):
        if delayed_remove is not None and delayed_remove in self.delayed_remove:
            self.common_remove(self.delayed_remove[delayed_remove])
        p_c = "green"
        plots = self.common_draw(best, population, b_c, p_c)
        self.common_lib_middeware_draw()
        if delayed_remove is None:
            self.common_remove(plots)
        else:
            self.delayed_remove[delayed_remove] = plots

    def common_lib_middeware_draw(self):
        plt.draw()
        plt.pause(GLOBAL_PAUSE_TIME)

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
        self.save = plots
        self.common_lib_middeware_draw()
        # self.common_remove(plots[2:])


class TSPGraph(AbstractGraph):
    def __init__(self, low, high):
        super().__init__()
        self.plot = self.fig.add_subplot(111, title="Traveling salesman problem")

    def draw_cities(self, cities, trajectory=None):
        for index, city in enumerate(cities):
            x = city[0]
            y = city[1]

            if index == 0:
                self.plot.plot(x, y, "bo", markersize=20)
            else:
                self.plot.plot(x, y, "go-", markersize=15)
            text = ""
            if trajectory is not None:
                text = trajectory[index]
            else:
                text = index
            self.plot.text(x, y, s=text, fontsize=30)

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
        self.draw_cities(cities, best_solution.trajectory)
        self.draw_connections(cities, c)
        plt.draw()
        plt.pause(GLOBAL_PAUSE_TIME)


class ParetoRankGraph(AbstractGraph):
    def __init__(self):
        super().__init__()
        self.plot = self.fig.add_subplot(111, title="Pareto rank")

    def plot_batch(self, solutions, c="blue", s=5, a=0.5):
        try:
            fV = [s.fitness_value for s in solutions]
            fV_squeezed = np.squeeze(fV)
            X = fV_squeezed[:, 0]
            Y = fV_squeezed[:, 1]
            self.plot.scatter(
                X,
                Y,
                s=s,
                alpha=a,
                c=c,
                marker="o",
            )
        except:
            pass



    def draw(self, solutions, paretoQ1):
        # plt.xlim(0, 5)
        # plt.ylim(0, 10)
        plt.xlabel('Lateral')
        plt.ylabel('Total')
        self.plot_batch(solutions)
        if paretoQ1 is not None:
            self.plot_batch(paretoQ1, "red", 100, 1)
        plt.draw()
        plt.pause(GLOBAL_PAUSE_TIME)
