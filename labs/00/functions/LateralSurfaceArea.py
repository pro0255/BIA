import math
from functions.ConeFunc import ConeFunc


class LateralSurfaceArea(ConeFunc):
    def __init__(self):
        pass

    def run(self, vector):
        return math.pi * vector[0] * self.sub_calculation(vector)
