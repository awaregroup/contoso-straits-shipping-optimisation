#!/usr/bin/env python
# coding: utf-8
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.



from typing import List
from azure.quantum.optimization import Problem, ProblemType, Term
import numpy as np
from itertools import combinations
from azure.quantum.optimization import ParallelTempering, SimulatedAnnealing, Tabu, QuantumMonteCarlo

# This allows you to connect to the Workspace you've previously deployed in Azure.
# Be sure to fill in the settings below which can be retrieved by running 'az quantum workspace show' in the terminal.
from azure.quantum import Workspace

# Copy the settings for your workspace below


def visualize_result(result, containers, ships, target):
    print("\rResult received from: ", target)
    nb_ships = len(ships)
    try:
        config = result['configuration']
        config = list(config.values())
        for ship, sub_config in enumerate(np.array_split(config, nb_ships)):
            shipWeight = 0
            for c,b in enumerate(sub_config):
                shipWeight = shipWeight + b*containers[c]
            print(f'Ship {ships[ship]}: \t' + ''.join(f'{b*containers[c]}' for c,b in enumerate(sub_config)) + ' - ' + str(shipWeight))
    except:
        print('No Configuration')
    try:
        print('Cost: {}'.format(result['cost']))
    except:
        print('No Cost')
    try:
        print('Parameters: {}'.format(result['parameters']))
    except:
        print('No Parameter')

def AddTermsWeightVarianceCost(start, end, containers, EqDistrib):
    terms: List[Term] = []
    

    return terms

def AddTermsDuplicateContainerCost(start, end, containers):
    terms: List[Term] = []

    return terms

def CalculateEqualDistribution(containerWeights, Ships):
    
    return 0,0

def createProblemForContainerWeights(containerWeights: List[int], Ships) -> List[Term]:

    terms: List[Term] = []
    containersWithinShip: List[int] = []
    containersAcrossShips: List[int, int] = []
 
    EqDistrib, totalWeight = CalculateEqualDistribution(containerWeights, Ships)
    

    print(Ships)
    print(containerWeights)
    print("Total Weight:", totalWeight)
    print("Equal weight distribution:", EqDistrib)

    # Create container weights in this format:
    # 1  5  9  7  3  - 1  5  9  7  3  - 1   5   9   7   3
    # W0 W1 W2 W3 W4   W5 W6 W7 W8 W9   W10 W11 W12 W13 W14 
    containersWithinShip = containerWeights*len(Ships)

    # Create container weights in this format:
    # 1  1  1  5  5  5  9  9  9  7  7  7  3  3  3
    for i in range(len(containerWeights)):
        for j in range(len(Ships)):
            k = i + j*len(containerWeights)
            containersAcrossShips.append([containersWithinShip[i], k])

    for split in np.array_split(range(len(containersWithinShip)), len(Ships)):
        terms = terms + AddTermsWeightVarianceCost(split[0], split[-1], containersWithinShip, EqDistrib)

    for split in np.array_split(range(len(containersAcrossShips)), len(containerWeights)):
        terms = terms + AddTermsDuplicateContainerCost(split[0], split[-1], containersAcrossShips)

    return terms


# Create the Terms for this list of containers:

def SolveMyProblem(problem, s):
    try:
        # Optimize the problem
        print("Optimizing with:", s.target)
        Job = s.submit(problem)
        Job.wait_until_completed()
        duration = Job.details.end_execution_time - Job.details.begin_execution_time
        if (Job.details.status == "Succeeded"):
            visualize_result(Job.get_results(), containerWeights*len(Ships), Ships, s.target)
            print("Execution duration: ", duration)
        else:
            print("\rJob ID", Job.id, "failed")
    except BaseException as e:
        print(e)

# Try to call a solver with different timeout value and see if it affects the results


def main(containerWeights: List[int], Ships: List[str], workspace ):
    terms = createProblemForContainerWeights(containerWeights,Ships)

    # Create the Problem to submit to the solver:
    nbTerms = len(terms)
    problemName = f'Balancing {str(len(containerWeights))} containers between {str(len(Ships))} Ships ({nbTerms:,} terms)'
    print(problemName)

    #Input your problem type here
    problem = Problem(name=problemName, problem_type=, terms=terms)
    jobid = SolveMyProblem(problem, SimulatedAnnealing(workspace, timeout=10))


# Try using the parameters returned by the parameter free versions and observe the significant performance improvement
    #SolveMyProblem(problem, SimulatedAnnealing(workspace, ))


if __name__ == '__main__':
    # This array contains a list of the weights of the containers:
    containerWeights = [3, 8, 3, 4, 1, 5, 2, 2, 7, 9, 5, 4, 8, 9, 4, 6, 8, 7, 6, 2, 2, 9, 4, 6, 3, 8, 5, 7, 2, 4, 9, 4]
    Ships = ["A", "B", "C", "D", "E"]
    workspace = Workspace (
    subscription_id = "",
    resource_group = "",
    name = "",
    location = ""
    )
    main(containerWeights, Ships, workspace)