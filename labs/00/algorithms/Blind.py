from algorithms.Abstract import AbstractAlgorithm


class BlindAgorithm(AbstractAlgorithm):
    """Blind algorithm tries to find global min/max.

    In n generated records tries to find min/max. Also takes to consideration min/max founded in last run. If current generation founded better results replace old one.

    For every record get Z value and after tries to find min/max.
    As return value is returned min/max vector with vectors of all generation values.

    Generation does not optimizes move.
    It remembers previous state.
    """

    def __init__(self, **kwds):
        super().__init__(**kwds)

    def generate_population(self, Function, dimension=2):
        """Generates population for BlindAlgorithm with random individuals

        Args:
            Function (class Function): specific Function (Sphere || Ackley..)
            dimension (int, optional): Defaults to 2.

        Returns:
            [Solution[]]: generated population as specific generation
        """
        super().generate_population()
        population = []
        for _ in range(self.size_of_population):
            population.append(
                self.generate_random_solution(Function.left, Function.right, dimension)
            )
        return population

    def start(self, Function):
        """Runs Blind Algorithm on specified Function

        Args:
            Function (class Function): specific Function (Sphere || Ackley..)
        """
        super().start()
        first_solution = self.generate_random_solution(Function.left, Function.right)
        self.evaluate(first_solution, Function)
        self.best_solution = first_solution

        while self.index_of_generation < self.max_generation:
            population = self.generate_population(Function)
            self.evalute_population(population, Function)
            best_in_population = self.select_best_solution(population)
            if best_in_population.fitness_value < self.best_solution.fitness_value:
                self.best_solution = best_in_population

            if self.graph:
                self.graph.draw(self.best_solution, population)
