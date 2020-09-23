from tkinter import *
from functions.Sphere import Sphere
from functions.Schwefel import Schwefel
from functions.Rosenbrock import Rosenbrock
from functions.Rastrigin import Rastrigin
from functions.Griewangk import Griewangk
from functions.Levy import Levy
from functions.Michalewicz import Michalewicz
from functions.Zakharov import Zakharov
from functions.Ackley import Ackley


functions = {
    "Sphere": Sphere(),
    "Schwefel": Schwefel(),
    "Rosenbrock": Rosenbrock(),
    "Rastrigin": Rastrigin(),
    "Griewangk": Griewangk(),
    "Levy": Levy(),
    "Michalewicz": Michalewicz(),
    "Zakharov": Zakharov(),
    "Ackley": Ackley(),
}


class Application:
    def __init__(self):
        self.root = Tk()
        self.root.title("BIA course")
        self.root.geometry("400x200")
        self.create_combo_box()
        self.create_input()

    def select_function(self, value):
        print(value)
        self.selected_function = functions[value]

    def create_combo_box(self):
        choices = list(functions.keys())
        variable = StringVar(self.root)
        variable.set(choices[0])
        menu = OptionMenu(self.root, variable, *choices, command=self.select_function)
        menu.pack()

    def create_input(self):
        label = Label(self.root, text="Number of iterations")
        label.pack()


    def start(self):
        self.root.mainloop()
