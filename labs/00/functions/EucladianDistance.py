import numpy as np


class EucladianDistance:
    def __init__(self):
        pass

    def run(self, vector):
        distance = 0
        rows = len(vector)
        for i in range(rows):
            current_index = i
            next_index = (i + 1) % rows

            current_vector = vector[current_index]
            next_vector = vector[next_index]

            dist = np.linalg.norm(next_vector - current_vector)
            distance += dist

        return distance
