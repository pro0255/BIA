
from algorithms.AbstractGenetic import AbstractGeneticAlgorithm

class SelfOrganizingMigrationAlgorithm(AbstractGeneticAlgorithm):
    def __init__(self, path_length=3,step=0.11, PRT=0.33, min_div=0.001, **kwds):
        self.path_length = path_length
        self.step = step
        self.PRT = PRT
        self.min_div = min_div
        super().__init__(**kwds)

    def generate_population(self, Function):
        pass

    def generate_individual(self, Function):
        pass

    def start(self, Function):
        """Runs ______ Algorithm on specified Function, with specified args.
        Args:
            Function (class Function): specific Function (Sphere || Ackley..)
        """
        super().start()
