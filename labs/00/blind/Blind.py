
import random
import numpy as np


def generate_in_bounderies(number_of_records, Func):
    records = []
    for _ in range(number_of_records):
        records.append([random.uniform(Func.left, Func.right), random.uniform(Func.left, Func.right)])
    return records



class BlindAgorithm():
    def __init__(self):
        pass

    def run(self, number_of_records, Func, min_vector_input = None):
        generation = generate_in_bounderies(number_of_records, Func)
        z_vector = []
        for value in generation:
            z = Func.run([value[0], value[1]])
            z_vector.append(z)
        
        min_index = np.argmin(z_vector)
        x = generation[min_index][0]
        y = generation[min_index][1]
        generation_min_vector = [x, y, z_vector[min_index]]

        if min_vector_input == None:
            return generation_min_vector
        else:
            return generation_min_vector if generation_min_vector[2] < min_vector_input[2] else min_vector_input  

