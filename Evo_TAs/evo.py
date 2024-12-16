import numpy as np
import pandas as pd
import random as rnd
import copy
from functools import reduce
import time


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
            else:
                print("Warning: Attempted to add a non-NumPy array solution. Skipping.")
        else:
            print("Warning: Attempted to add a None solution. Skipping.")

    def generate_random_solution(self):
        num_sections = len(sections_df)
        num_tas = len(tas_df)
        # Generate a random solution where each cell represents whether a TA is assigned to a section
        random_solution = np.random.randint(2, size=(num_sections, num_tas))
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
            if time.time() - start_time >= time_limit:
                print("Time limit reached. Exiting evolution process.")
                break

            # Ensure at least two solutions are available for crossover
            if self.size() >= 2:
                self.run_agent("crossover")  # Only run crossover if there are at least two solutions

        # cleaning up the population on the last iteration
        self.remove_dominated()
