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

    # Choose the appropriate problem_type
    return Problem(name="Ship Sample Problem", problem_type='', terms=terms)


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


# We can reduce the number of terms by removing duplicates (see associated Jupyter notebook for details)
# In code, this means a small modification to the create_problem_for_container_weights function:
def create_simplified_problem_for_container_weights(container_weights: List[int]) -> Problem:
    terms: List[Term] = []

    # implement a simplified term set here

    # Return an Ising-type problem
    return Problem(name="Ship Sample Problem (Simplified)", problem_type='', terms=terms)

def optimise_the_problem(container_weights : List[int], solver) -> None:
    simplified_problem = create_simplified_problem_for_container_weights(container_weights)
    print(f'\nThe simplified problem has {len(simplified_problem.terms)} terms')

    # Optimize the problem
    print('\nSubmitting simplified problem...')
    start = time.time()
    simplified_result = solver.optimize(simplified_problem)
    time_elapsed_simplified = time.time() - start
    print(f'\nResult in {time_elapsed_simplified} seconds:\n{simplified_result}\n')
    print_result_summary(simplified_result)



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