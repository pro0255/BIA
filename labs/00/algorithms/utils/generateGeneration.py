import random

def generate_in_bounderies(size_of_generation, Func):
    records = []
    for _ in range(size_of_generation):
        # records.append([random.uniform(-1000, 1000), random.uniform(-1000, 1000)])
        records.append(
            [
                random.uniform(Func.left, Func.right),
                random.uniform(Func.left, Func.right),
            ]
        )
    return records

