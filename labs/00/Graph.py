import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

class Graph():
    def __init__(self, start, stop, Function):
        x = np.linspace(start, stop, 100)
        y = np.linspace(start, stop, 100)
        X, Y = np.meshgrid(x, y)

        ax = plt.axes(projection="3d", title=type(Function).__name__)
        ax.plot_surface(X, Y, X, cmap=cm.varidis, linewidth=0, alpha=0.4)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")

        self.plot = ax
