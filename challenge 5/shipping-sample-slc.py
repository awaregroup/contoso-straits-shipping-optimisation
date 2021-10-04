#!/usr/bin/env python
# coding: utf-8
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from azure.quantum import Workspace
from azure.quantum.optimization import ParallelTempering
import time



# Take an array of container weights and return a Problem object that represents the cost function
from typing import List
from azure.quantum.optimization import Problem, ProblemType, Term

def create_problem_for_container_weights(container_weights: List[int]) -> Problem:
    terms: List[Term] = []
    '''
    create your terms list here
    '''

    #
    return Problem(name="Ship Sample Problem", problem_type=ProblemType.ising, terms=terms)


# Print out a summary of the results:
def print_result_summary(result):
    # Print a summary of the result
    ship_a_weight = 0
    ship_b_weight = 0
    for container in result['configuration']:
        container_assignment = result['configuration'][container]
        container_weight = container_weights[int(container)]
        ship = ''
        if container_assignment == 1:
            ship = 'A'
            ship_a_weight += container_weight
        else:
            ship = 'B'
            ship_b_weight += container_weight

        print(f'Container {container} with weight {container_weight} was placed on Ship {ship}')

    print(f'\nTotal weights: \n\tShip A: {ship_a_weight} tonnes \n\tShip B: {ship_b_weight} tonnes\n')


def main(container_weights: List[int])-> None:
    # Copy the settings for your workspace below
    workspace = Workspace (
        subscription_id = "",
        resource_group = "",
        name = "",
        location = ""
    )
    # Create a problem for the list of containers:
    problem = create_problem_for_container_weights(container_weights)

    # Instantiate a solver to solve the problem.
    solver = ParallelTempering(workspace, timeout=100)

    # Optimize the problem
    print('Submitting problem...')
    start = time.time()
    result = solver.optimize(problem)
    timeElapsed = time.time() - start
    print(f'\nResult in {timeElapsed} seconds:\n{result}\n')
    
    print_result_summary(result)

    # Improving the Cost Function
    # The cost function we've built works well so far, but let's take a closer look at the `Problem` that was generated:
    print(f'\nThe original problem has {len(problem.terms)} terms for {len(container_weights)} containers:')
    print(problem.terms)

    #Uncomment below if you have implemented create_simplified_problem_for_container_weights
    #optimise_the_problem(container_weights, solver)


if __name__ == '__main__':
    # This array contains a list of the weights of the containers
    container_weights = [1, 5, 9, 21, 35, 5, 3, 5, 10, 11]
    main(container_weights)