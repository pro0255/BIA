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
from algorithms.Algorithms import BlindAgorithm
from algorithms.Algorithms import HillClimbAlgorithm
from Graph import Graph

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

algorithms = {
    "Blind": BlindAgorithm(),
    "HillClimb": HillClimbAlgorithm()
}






class Application:
    """Represents GUI
    """

    def __init__(self):
        self.root = Tk()
        self.root.title("BIA course")
        self.root.geometry("400x600")


        self.all_entries = {}

        self.create_combo_box_function()
        self.create_combo_box_algorithm()
        self.create_input_size_generation()
        self.create_input_number_of_iterations()
        self.create_input_sigma()        
        

        self.create_run_button()

        self.run_disabled_entries_action()

    def create_run_button(self):
        self.run_button = Button(
            self.root,
            text="START ANIMATION",
            bg="brown",
            fg="white",
            font=("helvetica", 9, "bold"),
            command=self.run_action,
        )
        self.run_button.pack()

    def select_function_action(self, value):
        """Action binded to selection of Test function
        Args:
            value (string): Key of Test function which targets to functions object defined in global scope
        """
        self.selected_function = functions[value]

    def select_algorithm_action(self, value):
        """Action binded to selection of Algorithm
        Args:
            value (string): Key of Algortihm which targets to algorithms object defined in global scope
        """
        self.selected_algorithm = algorithms[value]
        self.run_disabled_entries_action()

    def create_combo_box_function(self):
        """Creation of combo box with Test functions
        """
        choices = list(functions.keys())
        variable = StringVar(self.root)
        init_function = choices[0]
        variable.set(init_function)
        self.select_function_action(init_function)
        menu = OptionMenu(self.root, variable, *choices, command=self.select_function_action)
        menu.pack()

    def create_combo_box_algorithm(self):
        """Creation of combo box with Algorithms
        """
        choices = list(algorithms.keys())
        variable = StringVar(self.root)
        init_algorithm = choices[0]
        variable.set(init_algorithm)
        self.selected_algorithm = algorithms[init_algorithm]
        menu = OptionMenu(self.root, variable, *choices, command=self.select_algorithm_action)
        menu.pack()


    def create_input_size_generation(self):
        """Creation of GUI tuple (label, input) for size generation
        """
        self.size_generation = StringVar()
        size_generation_label = Label(self.root, text="Size generation")
        size_generation_label.pack()
        size_generation = Entry(self.root, textvariable=self.size_generation)
        self.all_entries['size_of_population'] = size_generation 
        size_generation.pack()

    def create_input_number_of_iterations(self):
        """Creation of GUI tuple (label, input) for number of iterations
        """
        self.number_of_iterations = StringVar()
        number_of_iterations_label = Label(self.root, text="Number of iterations")
        number_of_iterations_label.pack()
        number_of_iterations = Entry(self.root, textvariable=self.number_of_iterations)
        self.all_entries['max_generation'] = number_of_iterations 
        number_of_iterations.pack()

    def create_input_sigma(self):  
        """Creation of GUI tuple (label, input) for sigma [HillClimbAlgorithm]
        """
        self.sigma = StringVar()
        sigma_label = Label(self.root, text="Sigma")
        sigma_label.pack()
        sigma = Entry(self.root, textvariable=self.sigma)
        self.all_entries['sigma'] = sigma
        sigma.pack()
    

    def toggle_entry(self, entry, enable = True):
        """Toggle state of entry

        Args:
            entry (class Entry): input
            enable (bool, optional): state of Entry. Defaults to True.
        """
        if enable:
            entry['state'] = 'normal'
        else:
            entry['state'] = 'disabled'

    def run_disabled_entries_action(self):
        """According to selected algorithm disable || enable GUI entries
        """
        if self.selected_algorithm.has_attribute('size_of_population'):
            self.toggle_entry(self.all_entries['size_of_population'])
        else:
            self.toggle_entry(self.all_entries['size_of_population'], False)

        if self.selected_algorithm.has_attribute('max_generation'):
            self.toggle_entry(self.all_entries['max_generation'])
        else:
            self.toggle_entry(self.all_entries['max_generation'], False)

        if self.selected_algorithm.has_attribute('sigma'):
            self.toggle_entry(self.all_entries['sigma'])
        else:
            self.toggle_entry(self.all_entries['sigma'], False)


    def run_action(self):
        graph = Graph(self.selected_function.left, self.selected_function.right, self.selected_function)
        algorithm = self.build_algorithm(graph)
        algorithm.start(self.selected_function)

    def build_algorithm(self, graph):
        algorithm = self.selected_algorithm
        algorithm.graph = graph

        if algorithm.has_attribute('size_of_population'):
            size_of_population = int(self.size_generation.get().strip())
            algorithm.size_of_population = size_of_population 

        if algorithm.has_attribute('max_generation'):
            max_generation = int(self.number_of_iterations.get().strip())
            algorithm.max_generation = max_generation 

        if algorithm.has_attribute('sigma'):
            sigma = float(self.sigma.get().strip())
            algorithm.sigma = sigma 


        return algorithm


    def start(self):
        """Starts GUI
        """
        self.root.mainloop()

    def stop(self):
        """Stops GUI
        """
        self.root.destroy()
