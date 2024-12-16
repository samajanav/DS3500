"""
Evolutionary Computing
Homework 6
Janav Sama and Jacob Jawharjian
"""

import numpy as np
import pandas as pd
import random as rnd
import copy
from functools import reduce
import time

# Load sections and TAs data
sections_df = pd.read_csv("sections.csv")
tas_df = pd.read_csv("tas.csv")


class Environment:
    def __init__(self):
        """ Environment constructor """
        self.pop = {}  # evaluation -> solution e.g.,  ((conflicts, 5), (undersupport, 3), ...) --> TA assignments
        self.fitness = {}  # objectives / fitness functions:   name->f
        self.agents = {}  # agents:   name -> (operator/function, num_solutions_input)

    def size(self):
        """ The size of the current population """
        return len(self.pop)

    def add_fitness_criteria(self, name, f):
        """ Add or declare an objective to the framework """
        self.fitness[name] = f

    def add_agent(self, name, op, k=1):
        """ Register a named agent with the framework
        The operator (op) function defines what the agent does.
        k defines the number of input solutions that the agent operates on """
        self.agents[name] = (op, k)

    def add_solution(self, sol):
        """ Evaluate and Add a solution to the population """
        if sol is not None:
            if isinstance(sol, np.ndarray):
                eval = tuple([(name, f(sol)) for name, f in self.fitness.items()])
                self.pop[eval] = sol
                print("Added solution to population:", sol)
                print("Population after adding solution:", self.pop)
            else:
                print("Warning: Attempted to add a non-NumPy array solution. Skipping.")
        else:
            print("Warning: Attempted to add a None solution. Skipping.")

    def generate_random_solution(self):
        num_sections = len(sections_df)
        num_tas = len(tas_df)
        # Generate a random solution where each cell represents whether a TA is assigned to a section
        random_solution = np.random.randint(2, size=(num_sections, num_tas))
        print("Generated random solution:", random_solution)
        return random_solution

    def run_agent(self, name):
        """ Invoke an agent against the population """
        op, k = self.agents[name]
        pick = self.generate_random_solution()
        new_solution = op(pick)
        self.add_solution(new_solution)

    @staticmethod
    def _dominates(p, q):
        """ p, q are the evaluations of the solutions """
        pscores = [score for _, score in p]
        qscores = [score for _, score in q]
        score_diffs = list(map(lambda x, y: y - x, pscores, qscores))
        min_diff = min(score_diffs)
        max_diff = max(score_diffs)
        return min_diff >= 0.0 and max_diff > 0.0

    @staticmethod
    def _reduce_nds(S, p):
        return S - {q for q in S if Environment._dominates(p, q)}

    def remove_dominated(self):
        nds = reduce(Environment._reduce_nds, self.pop.keys(), self.pop.keys())
        self.pop = {k: self.pop[k] for k in nds}

    def evolve(self, n=1, dom=100, status=100, time_limit=600):
        agent_names = list(self.agents.keys())
        start_time = time.time()
        for i in range(n):
            pick = rnd.choice(agent_names)
            self.run_agent(pick)
            if i % dom == 0:
                self.remove_dominated()
            if i % status == 0:
                print("Iteration:", i)
                print("Population Size:", self.size())
                print(self)
            if time.time() - start_time >= time_limit:
                print("Time limit reached. Exiting evolution process.")
                break

            # Ensure at least two solutions are available for crossover
            if self.size() >= 2:
                print("Performing crossover")
                self.run_agent("crossover")  # Only run crossover if there are at least two solutions

        # cleaning up the population on the last iteration
        self.remove_dominated()


# Define objective functions
def overallocation(solution):
    max_assigned_tas = tas_df['max_assigned'].values
    num_assigned_labs = np.sum(solution, axis=1)
    overallocation_penalty = np.maximum(0, num_assigned_labs - max_assigned_tas)
    return np.sum(overallocation_penalty)


def conflicts(solution):
    return np.sum(np.sum(solution, axis=0) > 1)


def undersupport(solution):
    min_required_tas = sections_df['min_ta'].values  # Load 'min_ta' values from the 'sections_df' DataFrame
    num_assigned_tas = np.sum(solution, axis=1)
    penalty = np.maximum(0, min_required_tas - num_assigned_tas) * 2
    return np.sum(penalty)


def unwilling(solution):
    unwilling_fitness = [_unwilling_helper(solution, ta_index) for ta_index in range(18)]
    return np.sum(unwilling_fitness)


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
        if len(solutions) < 2 or not all(s is not None and s.size > 0 for s in solutions):
            return None

        valid_solutions = [sol for sol in solutions if sol is not None and sol.size > 0]

        if len(valid_solutions) < 2:
            return None

        min_length = min(len(valid_solutions[0]), len(valid_solutions[1]))
        parent1 = valid_solutions[0][:min_length]
        parent2 = valid_solutions[1][:min_length]


def main():

    E = Environment()

    # Define and register objective functions
    E.add_fitness_criteria("conflicts", conflicts)
    E.add_fitness_criteria("undersupport", undersupport)
    E.add_fitness_criteria("unwilling", unwilling)
    E.add_fitness_criteria("unpreferred", unpreferred)
    E.add_fitness_criteria("overallocation", overallocation)

    # Register agents
    E.add_agent("mutate", Agents.mutate, k=1)  # Register the mutate agent
    E.add_agent("crossover", Agents.crossover, k=2)  # Register the crossover agent

    # Print initial population size
    print("Initial Population Size:", E.size())

    # Run the evolver
    E.evolve(time_limit=600)

    # Print the final result
    print(E)


if __name__ == "__main__":
    main()
