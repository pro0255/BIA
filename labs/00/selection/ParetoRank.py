import pandas as pd
from selection.CompareEnum import Compare
from selection.MaxMinEnum import Approach
import math
import numpy as np


def naive_check(Functions, approaches):
    """Naive which determines if input is ok.

    Args:
        Functions (Objective functions): Function correlated with approach.
        approaches (Approaches): Approach which will be applicated for Function xi.

    Returns:
        [boolean]: Result of check.
    """
    return len(Functions) == len(approaches)


def compare(current, other, approach):
    """Comparison of xi and xj.
    Args:
        current (float): Fitness xi.
        other (float): Fitness xj.
        approach (enum Approach): Apporach which determines logic.
    Returns:
        [enum Compare]: Represents result of comparsion.
    """
    if current == other:
        return Compare.Balance
    if approach == Approach.Minimazation:
        return Compare.Better if other < current else Compare.Worse
    else:
        return Compare.Better if other > current else Compare.Worse


def get_result_according_to_dd(dominating, dominated):
    """Helper method which determines what kind of result is it.
    Args:
        dominating (int): Number of dominating.
        dominated (int): Number of dominated.
    Returns:
        [enum Compare]: Result of calculation.
    """
    if dominated == dominating:
        return Compare.Balance
    return Compare.Better if dominating > dominated else Compare.Worse


def check_fitness_according_to_approach(current, other, approaches):
    """Method calculates how many fitness values are dominated and dominating.
    Args:
        current (float[]): Solution fitness vector.
        other (float[]): Solution fitness vector.
        approaches (enum Approach): Approaches applicated of specific fi.
    Returns:
        [enum Compare]: Result of comparison.
    """
    dominated = 0  # worse
    dominating = 0  # better
    for fI, approach in enumerate(approaches):
        result = compare(current.fitness_value[fI], other.fitness_value[fI], approach)

        if result == Compare.Better:
            dominating += 1
        elif result == Compare.Worse:
            dominated += 1
    res = get_result_according_to_dd(dominating, dominated)
    return res


def create_array_to_indicies(pop, indicies):
    """Helper method which return desired result with populated array.
    """
    res = []
    try:
        for i in indicies:
            res.append(pop[i])
    except:
        res.append(pop[indicies])
    return res


def according_to_n_get_Qn_indicies(n, ignore_indicies):
    """Filter indicies according to black list.
    Args:
        n (int[]): Vector n.
        ignore_indicies (int[]): Indicies which will be ignored.
    Returns:
        [int[]]: Vector of filtered indicies.
    """
    tranformed = np.squeeze(np.argwhere(np.array(n) == 0))
    try:
        return list(filter(lambda x: x not in ignore_indicies, tranformed))
    except:
        return tranformed


def dominate_n_according_to_Qn_indicies(n, Q_inidicies, S):
    """Correct subtraction of n of indicies.
    """
    dominated_lists = create_array_to_indicies(S, Q_inidicies)
    try:
        for l in dominated_lists:
            for index in l:
                n[index] -= 1
    except:
        for index in dominated_lists:
            n[index] -= 1
    return n


def create_Qs(n, S, population):
    """Method make soring Q1..Qn, with n ranks.
    """
    Q = []
    merged = []
    ignore_indicies = []
    while True:
        if len(ignore_indicies) == len(population):
            break
        indicies = according_to_n_get_Qn_indicies(n, ignore_indicies)
        Qn = create_array_to_indicies(population, indicies)
        try:
            ignore_indicies += list(indicies)
        except:
            ignore_indicies.append(indicies)
        merged += Qn
        Q.append(np.array(Qn))
        dominate_n_according_to_Qn_indicies(n, indicies, S)
    return (Q, merged)


def dominated_sorting(population, Functions, approaches, NP):
    """Method check if input of correct and then calculates pareto sets and from 2NP make NP.
    """
    if not naive_check(Functions, approaches):
        raise Exception(
            "Oops u should probably use same number of approaches as Functions :-)"
        )
    S = []  # dominated
    n = []  # dominating,
    size = len(population)
    for i in range(size):
        current = population[i]
        S_i = []
        n_i = 0
        for j in range(size):
            other = population[j]
            if current.key == other.key:
                continue
            result = check_fitness_according_to_approach(current, other, approaches)
            if result == Compare.Better:
                n_i += 1
            elif result == Compare.Worse:
                S_i.append(j)
        S.append(S_i)
        n.append(n_i)

    Qs, merged = create_Qs(n, S, population)
    return (Qs, merged[0:NP])
