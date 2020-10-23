blind_args = {
    "size_of_population": {
        "text": "Size of population",
        "convert": lambda a: int(a.get().strip()),
        "initial_value": 10,
    },
    "max_generation": {
        "text": "Max generation",
        "convert": lambda a: int(a.get().strip()),
        "initial_value": 50,
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
    },
}

differential_evolution_alg = {
    "crossover_range": {
        "text": "Crossover Range",
        "convert": lambda a: float(a.get().strip()),
        "initial_value": 0.5,
    },
    "mutation_constant": {
        "text": "Mutation Constant",
        "convert": lambda a: float(a.get().strip()),
        "initial_value": 0.5,
    },
}

particle_swarm_optimization = {
    "c1": {
        "text": "Learning constant c1",
        "convert": lambda a: float(a.get().strip()),
        "initial_value": 2,
    },
    "c2": {
        "text": "Learning constant c1",
        "convert": lambda a: float(a.get().strip()),
        "initial_value": 2,
    },
    "v_min": {
        "text": "Minimal velocity",
        "convert": lambda a: float(a.get().strip()),
        "initial_value": -1,
    },
    "v_max": {
        "text": "Maximal velocity",
        "convert": lambda a: float(a.get().strip()),
        "initial_value": 1,
    },
}
