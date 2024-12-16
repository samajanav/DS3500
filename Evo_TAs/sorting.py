"""
File: sorting.py
Description: A demo of the evo framework
We'll sort a list of numbers using evolutionary computing
"""

import evo
import random as rnd


def stepsdown(L):
    """ Total the step downs in the numeric sequence """
    return sum([x - y for x, y in zip(L, L[1:]) if y < x])


def swapper(solutions):
    """ An agent that swaps two random values """
    L = solutions[0]
    i = rnd.randrange(0, len(L))
    j = rnd.randrange(0, len(L))
    L[i], L[j] = L[j], L[i]
    return L

def main():

    # create the environment
    E = evo.Environment()

    # register the fitness functions
    E.add_fitness_criteria("stepsdown", stepsdown)

    # register the agents
    E.add_agent("swapper", swapper, 1)

    # Adding 1 or more initial solution
    L = [rnd.randrange(1, 99) for _ in range(30)]
    E.add_solution(L)

    # Run the evolver
    E.evolve(1000000, 100, 100)

    # Print the final result
    print(E)


if __name__ == '__main__':
    main()