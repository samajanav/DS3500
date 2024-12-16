import numpy as np
import pandas as pd
import random as rnd
import copy

tas_df = pd.read_csv("tas.csv")
sections_df = pd.read_csv("sections.csv")


# Define objective functions
def overallocation(solution):
    max_assigned_tas = tas_df['max_assigned'].values
    num_assigned_labs = np.sum(solution, axis=1)
    overallocation_penalty = np.maximum(0, num_assigned_labs - max_assigned_tas)
    return np.sum(overallocation_penalty)


def conflicts(solution):
    return np.sum(np.sum(solution, axis=0) > 1)


def undersupport(solution):
    min_required_tas = sections_df['min_ta'].values
    num_assigned_tas = np.sum(solution, axis=1)
    penalty = np.maximum(0, min_required_tas - num_assigned_tas) * 2
    return np.sum(penalty)

def unwilling(solution):
    unwilling_mask = (tas_df.iloc[:, 2:] == 'U').values
    return np.sum(solution & unwilling_mask)


def unpreferred(solution):
    willing_mask = (tas_df.iloc[:, 2:] == 'W').values
    preferred_mask = (tas_df.iloc[:, 2:] == 'P').values
    unpreferred_mask = willing_mask & ~preferred_mask
    return np.sum(solution & unpreferred_mask)


# Define agents for mutation and crossover
class Agents:
    @staticmethod
    def mutate(solution):
        """Mutate a solution by randomly changing one or more elements."""
        if solution is None or len(solution) == 0:
            return None

        mutated_solution = copy.deepcopy(solution)
        section_index = rnd.randint(0, len(mutated_solution) - 1)
        ta_index = rnd.randint(0, len(mutated_solution[section_index]) - 1)
        mutated_solution[section_index][ta_index] = 1 - mutated_solution[section_index][ta_index]  # Toggle assignment
        return mutated_solution

    @staticmethod
    def crossover(solutions):
        """Perform crossover operation on two solutions to create a new one."""
        if len(solutions) < 2 or not all(solutions):
            return None

        min_length = min(len(solutions[0]), len(solutions[1]))
        parent1 = solutions[0][:min_length]
        parent2 = solutions[1][:min_length]

        # Combine two solutions by taking half from each
        crossover_point = min_length // 2
        new_solution = parent1[:crossover_point] + parent2[crossover_point:]
        return new_solution
