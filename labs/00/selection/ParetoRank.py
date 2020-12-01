def naive_check(Functions, approaches):
    return len(Functions) == len(approaches)

def dominated_sorting(population, Functions, approaches):
    if not naive_check(Functions, approaches):
        raise Exception('Oops u should probably use same number of approaches as Functions :-)')
    Q = []
    S = []
    n = []
    print('ed_sorting')