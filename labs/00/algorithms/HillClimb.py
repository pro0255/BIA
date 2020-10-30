
from solution.Solution import Solution
from algorithms.Abstract import AbstractAlgorithm

class HillClimbAlgorithm(AbstractAlgorithm):
    def __init__(self, sigma=1, **kwds):
        self.sigma = sigma
        super().__init__(**kwds)

    def generate_population(self, Function, dimension=2):
        """Generates population for HillClimbAlgorithm with np.random.normal

        Args:
            Function (class Function): specific Function (Sphere || Ackley..)
            dimension (int, optional): Defaults to 2.

        Returns:
            [Solution[]]: generated population as specific generation
        """
        super().generate_population()
        population = []
        for _ in range(self.size_of_population):
            neighbor = Solution(lower_bound=Function.left, upper_bound=Function.right)
            neighbor.fill_vector_with_gaussian(self.best_solution, self.sigma)
            population.append(neighbor)

        return population

    def start(self, Function):
        """Runs HillClimb Algorithm on specified Function, with specified args.

        Args:
            Function (class Function): specific Function (Sphere || Ackley..)
        """
        super().start()
        first_solution = self.generate_random_solution(Function.left, Function.right)
        self.evaluate(first_solution, Function)
        self.best_solution = first_solution

        while self.index_of_generation < self.max_generation:
            neighborhood = self.generate_population(Function)
            self.evalute_population(neighborhood, Function)
            best_in_neighborhood = self.select_best_solution(neighborhood)
            if best_in_neighborhood.fitness_value < self.best_solution.fitness_value:
                self.best_solution = best_in_neighborhood

            if self.graph:
                self.graph.draw(self.best_solution, neighborhood)
        self.close_plot()