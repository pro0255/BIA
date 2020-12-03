import math
import numpy as np
from functions.ConeFunc import ConeFunc

class TotalArea(ConeFunc):
    def __init__(self):
        pass
    
    def run(self, vector):
        return math.pi*vector[0]*(vector[0]+self.sub_calculation(vector))
