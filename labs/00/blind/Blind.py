
import random
import numpy as np


def generate_in_bounderies(number_of_records, Func):
    records = []
    for _ in range(number_of_records):
        # records.append([random.uniform(-1000, 1000), random.uniform(-1000, 1000)])
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

        min_result_vector = []

        if min_vector_input == None:
            min_result_vector = generation_min_vector
        else:
            min_result_vector =  generation_min_vector if generation_min_vector[2] < min_vector_input[2] else min_vector_input  

        generation_all_vectors = [[value[0], value[1], z_vector[index]] for index, value in enumerate(generation) if min_result_vector[2] != z_vector[index]]
        x = []
        y = []
        z = []
        for vector in generation_all_vectors:
            x.append(vector[0])
            y.append(vector[1])
            z.append(vector[2])
        return [min_result_vector, [x, y, z]]

        

