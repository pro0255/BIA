from experiments import EXPERIMENT_CONSTANTS
from experiments.DELIMITER import DELIMITER, DELIMITER_README, READ_ME_HEADER
from experiments.EXPERIMENTS_OUTPUT import EXPERIMENTS_PATH, EXPERIMENTS_FILE_NAME
import os
import time
import pandas as pd
import numpy as np
from STAR import get_my_info

SAVE = True

def THANKS(seconds):
    return f'Run whole experiments took {seconds} seconds.\nThanks for your time again.\n{get_my_info()}'

 


class ExperimentsRunner():
    """Class which takes care of running experiments with specified parameters.
    """
    def __init__(self, D=EXPERIMENT_CONSTANTS.D, NP=EXPERIMENT_CONSTANTS.NP, MAX_G=EXPERIMENT_CONSTANTS.Max_OFE, NUMBER_OF_EXPERIMENTS=EXPERIMENT_CONSTANTS.NUMBER_OF_EXPERIMENTS):
        self.D = D
        self.NP = NP
        self.MAX_G = MAX_G
        self.N_O_G = NUMBER_OF_EXPERIMENTS
        self.results = {}

    def set_properties(self, algorithms):
        for a in algorithms:
            a.size_of_population = self.NP
            a.max_generation = self.MAX_G
            a.D = self.D

    def build(self, algs = EXPERIMENT_CONSTANTS.ALGORITHMS_TO_RUN):
        self.set_properties(algs)
        return algs


    def create_index(self, l):
        return [f'Experiment {i+1}' for i in range(l)]

    def make_df_calculations(self):
        for k, v in self.results.items():
            means = {}
            std_devs = {}
            for column in v:
                values = v[column].values
                mean = np.mean(v[column].values)
                std_dev = np.std(v[column].values)
                means[column] = mean
                std_devs[column] = std_dev
            new_df = v.copy()
            new_df.loc['mean'] = list(means.values())
            new_df.loc['std_dev'] = list(std_devs.values()) 
            self.results[k] = new_df


    def save_to_xls(self, name):
        self.check_save()
        file_name = f'{EXPERIMENTS_PATH}//{name}.xlsx'
        print(f'Saving to {file_name}..')
        with pd.ExcelWriter(file_name, mode='w') as writer:
            for k,v in self.results.items():
                v.to_excel(writer, sheet_name=k)


    def save_data_frame(self, df, func):
        self.results[func] = df

    def create_experiment_dataframe(self, dic, func):
        df = pd.DataFrame(dic)
        df.index = self.create_index(len(df))
        self.save_data_frame(df, func)
        # df.index.names = self.create_index(len(df))

    def save_read_me(self):
        output = [f'{DELIMITER_README}{str(alg)}{DELIMITER_README}' for alg in EXPERIMENT_CONSTANTS.ALGORITHMS_TO_RUN]
        output_algorithms = f'\n'.join(output)
        read_me = f'{READ_ME_HEADER}\n{output_algorithms}'
        self.save_to_file(read_me, "README", '.txt')

    def start_experiments_for_functions(self, functions=EXPERIMENT_CONSTANTS.FUNCTION_TO_RUN):
        self.results = {}
        start = time.time()

        print('Starting experiments for specified functions.')
        for f in functions:
            output_dic = self.start_experiments(f)
            self.create_experiment_dataframe(output_dic, type(f).__name__)
        print('Thanks for your time experiments finished :-].')
        print(get_my_info())

        end = time.time()
        how_many = str(end - start)

        self.make_df_calculations()
        if SAVE:
            self.save_to_file(THANKS(how_many), "INFO", ".txt")
            self.save_to_xls(EXPERIMENTS_FILE_NAME)
            self.save_read_me()
            

    def start_experiments(self, function):
        dic = {self.get_algorithm_key(alg):[] for alg in EXPERIMENT_CONSTANTS.ALGORITHMS_TO_RUN}
        FUNCTION_NAME = type(function).__name__
        print(f'Starting for objective function *{FUNCTION_NAME}* ')
        for i in range(self.N_O_G):
            transformed_index = i + 1 #lol
            self.start_experiment(function, dic)
        return dic


    def get_algorithm_key(self, algorithm):
        return type(algorithm).__name__

    def start_experiment(self, function, dic):
        for algorithm in self.build():
            fV, description = algorithm.start(function)
            dic[self.get_algorithm_key(algorithm)].append(fV)

    def check_save(self, path=EXPERIMENTS_PATH):
        path = f'{EXPERIMENTS_PATH}'
        if not os.path.exists(path):
            os.makedirs(path)



    def save_to_file(self, text, name, suffix='-experiments.csv', directory="experiments"):
        self.check_save()
        with open(f'{EXPERIMENTS_PATH}//{name}{suffix}', 'w') as f:
            f.write(text)

        



