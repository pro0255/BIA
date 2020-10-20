from tkinter import *
from functions.EucladianDistance import EucladianDistance
from init_algorithms import algorithms
from init_functions import functions
from Graph import Graph
from Graph import TSPGraph
import matplotlib.pyplot as plt
import converters.Converters as converters
import WINDOW_VALUES as WV

algorithms_functions_blacklist = ["GeneticAlgorithmTSP"]
merged_args = {**converters.blind_args, **converters.hill_climb_args, **converters.simulated_annealing_args, **converters.traveling_salesman_problem_GA, **converters.differential_evolution_alg}


class Application:
    """Represents GUI"""

    def __init__(self):
        self.root = Tk()
        self.root.title("BIA course")
        self.root.geometry(f"{WV.GLOBAL_WIDTH}x{WV.GLOBAL_HEIGHT}")

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
            width=WV.GLOBAL_WIDTH,
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
        init_function = WV.INITIAL_FUNCTION_KEY
        variable.set(init_function)
        self.select_function_action(init_function)
        menu = OptionMenu(
            self.root, variable, *choices, command=self.select_function_action
        )
        menu.configure(width=WV.GLOBAL_WIDTH, bg=WV.GLOBAL_OPTION_MENU_COLOR)

        menu.pack()
        self.menu_function = menu

    def create_combo_box_algorithm(self):
        """Creation of combo box with Algorithms"""
        choices = list(algorithms.keys())
        variable = StringVar(self.root)
        init_algorithm = WV.INITIAL_ALGORITHM_KEY
        variable.set(init_algorithm)
        self.selected_algorithm = algorithms[init_algorithm]
        menu = OptionMenu(
            self.root, variable, *choices, command=self.select_algorithm_action
        )
        menu.configure(width=WV.GLOBAL_WIDTH, bg=WV.GLOBAL_OPTION_MENU_COLOR)

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

    def toggle_function(self):
        if type(self.selected_algorithm).__name__ in algorithms_functions_blacklist:
            self.menu_function.pack_forget()
        else:
            self.menu_function.pack()


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
            if type(self.selected_algorithm).__name__ not in algorithms_functions_blacklist:
                self.run_button[
                    "text"
                ] = f"{constant_text} on {var_text_function} with {var_text_algorithm}"
            else:
                self.run_button[
                    "text"
                ] = f"{constant_text} with {var_text_algorithm}"

        except:
            print("no button now")

    def run_disabled_entries_action(self):
        """According to selected algorithm disable || enable GUI entries"""
        self.toggle_function()
        for key in merged_args:
            if self.selected_algorithm.has_attribute(key):
                self.toggle_entry(self.all_entries[key])
            else:
                self.toggle_entry(self.all_entries[key], False)

    def run_action(self):
        """Actions binded to click on start algorithm with specified args"""
        if type(self.selected_algorithm).__name__ == 'GeneticAlgorithmTSP':
            ed = EucladianDistance()
            graph = TSPGraph(0, 200)
            algorithm = self.build_algorithm(graph)
            algorithm.start(ed)
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
