"""
Evolutionary Computing
Homework 6
Janav Sama and Jacob Jawharjian
"""

from evo import Environment
from function_agents import overallocation, conflicts, undersupport, unwilling, unpreferred, Agents
import numpy as np
import pandas as pd
import time

sections_df = pd.read_csv("sections.csv")


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
