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
        ax.plot_surface(X, Y, Z, cmap=varidis, linewidth=0, alpha=0.4)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")

        self.plot = ax
