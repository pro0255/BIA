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
from algorithms.Algorithms import SimulatedAnnealingAlgorithm
from algorithms.Algorithms import GeneticAlgorithmTSP
from Graph import Graph
from Graph import TSPGraph
import matplotlib.pyplot as plt

INITIAL_FUNCTION_KEY = "Sphere"
INITIAL_ALGORITHM_KEY = "GeneticAlgorithmTSP"
GLOBAL_WIDTH = 600
GLOBAL_HEIGHT = 600
GLOBAL_INPUT_SIZE = 100
GLOBAL_OPTION_MENU_COLOR = "DodgerBlue2"


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
    "HillClimb": HillClimbAlgorithm(),
    "SimulatedAnnealing": SimulatedAnnealingAlgorithm(),
    "GeneticAlgorithmTSP": GeneticAlgorithmTSP()
}


blind_args = {
    "size_of_population": {
        "text": "Size of population",
        "convert": lambda a: int(a.get().strip()),
        "initial_value": 10,
    },
    "max_generation": {
        "text": "Max generation",
        "convert": lambda a: int(a.get().strip()),
        "initial_value": 30,
    },
}

hill_climb_args = {
    "sigma": {
        "text": "Sigma gaussian value",
        "convert": lambda a: float(a.get().strip()),
        "initial_value": 0.5,
    }
}

simulated_annealing_args = {
    "initial_temperature": {
        "text": "Initial temperature - T_0",
        "convert": lambda a: float(a.get().strip()),
        "initial_value": 100,
    },
    "minimal_temperature": {
        "text": "Minimal temperature - T_min",
        "convert": lambda a: float(a.get().strip()),
        "initial_value": 0.5,
    },
    "cooling_constant": {
        "text": "Cooling constant - alpha",
        "convert": lambda a: float(a.get().strip()),
        "initial_value": 0.95,
    },
}

traveling_salesman_problem_GA = {
    "number_of_cities": {
        "text": "Number of cities",
        "convert": lambda a: int(a.get().strip()),
        "initial_value": 20,
    },
    "low": {
        "text": "Low border",
        "convert": lambda a: int(a.get().strip()),
        "initial_value": 0,
    },
    "high": {
        "text": "High border",
        "convert": lambda a: int(a.get().strip()),
        "initial_value": 200,
    }
}


merged_args = {**blind_args, **hill_climb_args, **simulated_annealing_args, **traveling_salesman_problem_GA}

# TODO!: automatic generation of (label, input)
class Application:
    """Represents GUI"""

    def __init__(self):
        self.root = Tk()
        self.root.title("BIA course")
        self.root.geometry(f"{GLOBAL_WIDTH}x{GLOBAL_HEIGHT}")

        self.all_entries = {}
        self.create_run_button()
        self.create_combo_box_function()
        self.create_combo_box_algorithm()

        self.algorithms_args = {}
        self.create_entries_dynamic()

        self.run_disabled_entries_action()
        self.change_text_button_action()

    def create_run_button(self):
        self.run_button = Button(
            self.root,
            text="START ANIMATION",
            bg="brown",
            fg="white",
            font=("helvetica", 9, "bold"),
            command=self.run_action,
            width=GLOBAL_WIDTH,
        )
        self.run_button.pack()

    def select_function_action(self, value):
        """Action binded to selection of Test function
        Args:
            value (string): Key of Test function which targets to functions object defined in global scope
        """
        self.selected_function = functions[value]
        self.change_text_button_action()

    def select_algorithm_action(self, value):
        """Action binded to selection of Algorithm
        Args:
            value (string): Key of Algortihm which targets to algorithms object defined in global scope
        """
        self.selected_algorithm = algorithms[value]
        self.run_disabled_entries_action()
        self.change_text_button_action()

    def create_combo_box_function(self):
        """Creation of combo box with Test functions"""
        choices = list(functions.keys())
        variable = StringVar(self.root)
        init_function = INITIAL_FUNCTION_KEY
        variable.set(init_function)
        self.select_function_action(init_function)
        menu = OptionMenu(
            self.root, variable, *choices, command=self.select_function_action
        )
        menu.configure(width=GLOBAL_WIDTH, bg=GLOBAL_OPTION_MENU_COLOR)

        menu.pack()

    def create_combo_box_algorithm(self):
        """Creation of combo box with Algorithms"""
        choices = list(algorithms.keys())
        variable = StringVar(self.root)
        init_algorithm = INITIAL_ALGORITHM_KEY
        variable.set(init_algorithm)
        self.selected_algorithm = algorithms[init_algorithm]
        menu = OptionMenu(
            self.root, variable, *choices, command=self.select_algorithm_action
        )
        menu.configure(width=GLOBAL_WIDTH, bg=GLOBAL_OPTION_MENU_COLOR)

        menu.pack()

    def create_input_dynamic(self, algorithm_tuple_arg):
        """Creation of special gui tuple (label, entry)

        Args:
            algorithm_tuple_arg ((key, {"test": string, "convert": lambda})): tuple which contains specific information linked to gui tuple
        """
        key = algorithm_tuple_arg[0]
        value = algorithm_tuple_arg[1]
        self.algorithms_args[key] = StringVar()
        self.algorithms_args[key].set(value["initial_value"])

        label = Label(self.root, text=value["text"])
        label.pack()

        entry = Entry(self.root, textvariable=self.algorithms_args[key])
        entry.configure(width=50)
        entry.pack()

        self.all_entries[key] = (label, entry)

    def create_entries_dynamic(self):
        """Dynamic creation of tuples (label, entry) according to global dictionary"""
        for dic_tuple in merged_args.items():
            self.create_input_dynamic(dic_tuple)

    def toggle_entry(self, entry_tuple, enable=True):
        """Toggle state of entry

        Args:
            entry ((class Entry, class Label)): input
            enable (bool, optional): state of Entry. Defaults to True.
        """
        if enable:
            for item in entry_tuple:
                item.pack()
            # entry["state"] = "normal"
        else:
            for item in entry_tuple:
                item.pack_forget()
            # entry["state"] = "disabled"

    def change_text_button_action(self):
        """Action triggers change of run_button text according to selected algorithm"""
        constant_text = "Start Animation"
        var_text_function = ""
        var_text_algorithm = ""
        try:
            var_text_function = type(self.selected_function).__name__
        except:
            print("no selected function")

        try:
            var_text_algorithm = type(self.selected_algorithm).__name__
        except:
            print("no selected algorithm")
        try:
            self.run_button[
                "text"
            ] = f"{constant_text} on {var_text_function} with {var_text_algorithm}"
        except:
            print("no button now")

    def run_disabled_entries_action(self):
        """According to selected algorithm disable || enable GUI entries"""
        for key in merged_args:
            if self.selected_algorithm.has_attribute(key):
                self.toggle_entry(self.all_entries[key])
            else:
                self.toggle_entry(self.all_entries[key], False)

    def run_action(self):
        """Actions binded to click on start algorithm with specified args"""
        if type(self.selected_algorithm).__name__ == 'GeneticAlgorithmTSP':
            graph = TSPGraph(0, 200)
            algorithm = self.build_algorithm(graph)
            algorithm.start()
        else:
            graph = Graph(
                self.selected_function.left,
                self.selected_function.right,
                self.selected_function,
            )
            algorithm = self.build_algorithm(graph)
            algorithm.start(self.selected_function)

        # PRODUCTION crash
        # try:
        #     algorithm.start(self.selected_function)
        # except Exception as e:
        #     print("Oops!", e.__class__, "occurred.")
        #     plt.close()

    def build_algorithm(self, graph):
        """Function which sets all args to selected algorithm

        Args:
            graph (class Graph)

        Returns:
            class Algorithm: builded Algorithm with all args according to GUI inputs
        """
        algorithm = self.selected_algorithm
        algorithm.graph = graph

        for key, value in merged_args.items():
            if algorithm.has_attribute(key):
                try:
                    converter = value["convert"]
                    converted_value = converter(self.algorithms_args[key])
                    algorithm[key] = converted_value
                except:
                    print(f"wrong input for {key}")

        return algorithm

    def start(self):
        """Starts GUI"""
        self.root.mainloop()

    def stop(self):
        """Stops GUI"""
        self.root.destroy()
