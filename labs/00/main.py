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
from blind.Blind import blind
import math



def draw_fig(Func):
    x = np.linspace(Func.left, Func.right, 30)
    y = np.linspace(Func.left, Func.right, 30)
    X, Y = np.meshgrid(x, y)
    Z = run_func(X, Y, Func)

    ax = plt.axes(projection='3d')
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    cmap='viridis', edgecolor='none')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    plt.show()

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
michalewicz =  Michalewicz()
zakharov = Zakharov()
ackley = Ackley()
##


blind()
draw_fig(ackley)

