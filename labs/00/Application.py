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
        self.create_input_size_generation()
        self.create_input_number_of_iterations()
        self.create_combo_box()
    

    def select_function(self, value):
        print(value)
        self.selected_function = functions[value]

    def create_combo_box(self):
        choices = list(functions.keys())
        variable = StringVar(self.root)
        init_function = choices[0]
        variable.set(init_function)
        self.select_function(init_function)
        menu = OptionMenu(self.root, variable, *choices, command=self.select_function)
        menu.pack()

    def idk(self, value):
        print(value)


    def create_input_size_generation(self):
        self.size_generation = StringVar()
        size_generation_label = Label(self.root, text="Size generation")
        size_generation_label.pack()
        size_generation = Entry(self.root, textvariable=self.size_generation)
        size_generation.pack()

    def create_input_number_of_iterations(self):
        self.number_of_iterations = StringVar()
        number_of_iterations_label = Label(self.root, text="Number of iterations")
        number_of_iterations_label.pack()
        number_of_iterations = Entry(self.root, textvariable=self.number_of_iterations)
        number_of_iterations.pack()


    def start(self):
        self.root.mainloop()
